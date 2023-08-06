# Author: MetariumProject

# Standard libraries
import asyncio
import json
import os
from pathlib import Path
import shutil
# Third party libraries
from ipfshttpclient.exceptions import (
    TimeoutError,
)
from substrateinterface import SubstrateInterface, Keypair
# Metarium libraries
from py_metarium import (
    FUTURE,
)
# local libraries
from ..utils import (
    StorageError,
    SwarmKeyDoesNotExistError,
)
from ..storage import (
    KuriSyncBase,
)

from ..pubsub import (
    IPFSPubSub,
)

from ..storage import (
    StorageBase,
    HasherBase,
    IPFSClient,
)


class TopicListener(KuriSyncBase, IPFSPubSub, StorageBase, HasherBase, IPFSClient):

    """
        A Yettagam TopicListener can perform the following functions:
        [x] Publish it's own status via IPFS Pub/sub
        [x] Listen to a Topic's kuris on a Metarium chain
        [x] Sync with a Topic Committer via IPFS Pub/sub
    """

    def __init__(self, node_url:str=None, chain_swarm_key_path:str=None, listener_swarm_key_path:str=None, path:str=None, **encoder_kwargs) -> None:
        
        assert node_url is not None
        assert chain_swarm_key_path is not None and os.path.exists(chain_swarm_key_path)
        assert listener_swarm_key_path is not None and os.path.exists(listener_swarm_key_path)
        assert "mnemonic" in encoder_kwargs or "uri" in encoder_kwargs
        
        # initialize the KuriSyncBase class
        KuriSyncBase.__init__(self, metarium_node_url=node_url)
        # initialize the IPFSPubSub class
        IPFSPubSub.__init__(self)
        # initialize the StorageBase class
        StorageBase.__init__(self)
        # initialize the IPFSClient class
        IPFSClient.__init__(self)
        if "mnemonic" in encoder_kwargs:
            self.key_pair = Keypair.create_from_mnemonic(encoder_kwargs["mnemonic"])
        elif "uri" in encoder_kwargs:
            self.key_pair = Keypair.create_from_uri(encoder_kwargs["uri"])
        
        self.swarm_file_set = set()

        self.__setup(
            node_url=node_url,
            path=path or f"{Path().resolve()}",
            chain_swarm_key_path=chain_swarm_key_path,
            listener_swarm_key_path=listener_swarm_key_path
        )

    def __setup(self, node_url:str=None, path:str=None, chain_swarm_key_path:str=None, listener_swarm_key_path:str=None):
        assert node_url is not None
        assert path is not None
        # IPFS
        self._setup_ipfs_client()
        # directories
        self.topic_set = set()
        substrate = SubstrateInterface(url=node_url)
        # set "~/.ipfs/"" as self.ipfs_directory
        self.ipfs_directory = f"{Path.home()}/.ipfs"
        self.directory = f"{path}/{self.key_pair.ss58_address}/{substrate.chain}"
        self.data_directory = f"{self.directory}/data"
        self.swarm_directory = f"{self.directory}/swarm"
        self.sync_directory = f"{self.directory}/sync"
        # create directories if they don't exist
        self._set_or_create_directory(self.data_directory)
        self._set_or_create_directory(self.swarm_directory)
        self._set_or_create_directory(self.sync_directory)
        # create mappings.json in data if it doesn't exist
        self._set_or_create_file(path=f"{self.data_directory}/mappings", extension="json")
        # create mappings.json in swarm if it doesn't exist
        self._set_or_create_file(path=f"{self.swarm_directory}/mappings", extension="json")
        # create status.txt in sync if it doesn't exist
        self._set_or_create_file(path=f"{self.sync_directory}/status", extension="txt")
        # create rff.txt in sync if it doesn't exist
        self._set_or_create_file(path=f"{self.sync_directory}/rff", extension="txt")
        # setup chain swarm key mapping
        self.chain_swarm_key_hash = self._setup_swarm_key_mapping(
            swarm_key_file_name="chain.key",
            swarm_key_path=chain_swarm_key_path
        )
        # setup listener swarm key mapping
        self.listener_swarm_key_hash = self._setup_swarm_key_mapping(
            swarm_key_file_name="listener.key",
            swarm_key_path=listener_swarm_key_path
        )

    def __update_swarm_mappings(self, data:dict=None, return_file_hash:bool=False):
        assert data is not None
        return_file_hash = return_file_hash or False
        with open(f"{self.swarm_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
        swarm_key_hash = self._blake3_hash(data=data)
        if swarm_key_hash not in mappings:
            mappings[swarm_key_hash] = data["content"]
            with open(f"{self.swarm_directory}/mappings.json", "w") as f:
                json.dump(mappings, f)
        if return_file_hash:
            return swarm_key_hash

    def _setup_swarm_key_mapping(self, swarm_key_file_name:str=None, swarm_key_path:str=None):
        assert swarm_key_file_name is not None
        assert swarm_key_path is not None and os.path.exists(swarm_key_path)
        # copy swarm key from swarm key path to self.swarm_directory
        shutil.copyfile(
            src=swarm_key_path,
            dst=f"{self.swarm_directory}/{swarm_key_file_name}"
        )
        # add swarm key to self.swarm_file_set
        self.swarm_file_set.add(swarm_key_file_name)
        # add swarm key to swarm mappings
        swarm_key_data = {
            "type": "file",
            "content": os.path.join(self.swarm_directory, swarm_key_file_name)
        }
        return self.__update_swarm_mappings(data=swarm_key_data, return_file_hash=True)

    def _set_ipfs_swarm_key(self):
        assert self.swarm_key_path is not None
        shutil.copy(self.swarm_key_path, f"{self.ipfs_directory}/swarm.key")

    def _set_chain_swarm_key(self):
        with open(f"{self.swarm_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
        self.swarm_key_path = None
        for key, value in mappings.items():
            if key == self.chain_swarm_key_hash:
                self.swarm_key_path = value
                break
        if self.swarm_key_path is None:
            raise SwarmKeyDoesNotExistError(f"Swarm key for listening to the chain does not exist: {self.swarm_directory}/chain.key")

    def _set_listener_swarm_key(self, listener_swarm_key_hash:str=None):
        with open(f"{self.swarm_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
        self.swarm_key_path = None
        for key, value in mappings.items():
            if key == listener_swarm_key_hash:
                self.swarm_key_path = value
                break
        if self.swarm_key_path is None:
            raise SwarmKeyDoesNotExistError(f"Swarm key for connecting to the listener does not exist: {listener_swarm_key_hash}")

    def switch_to_chain_swarm(self):
        self._set_chain_swarm_key()
        self._set_ipfs_swarm_key()
    
    def switch_to_listener_swarm(self, listener_swarm_key_hash:str=None):
        assert listener_swarm_key_hash is not None
        self._set_listener_swarm_key(listener_swarm_key_hash=listener_swarm_key_hash)
        self._set_ipfs_swarm_key()

    async def publish_status(self, topic_id:int=None) -> str:
        assert topic_id is not None

        try:
            # switch current swarm to chain swarm
            self.switch_to_chain_swarm()
            listener_data = {
                "caller": self.key_pair.ss58_address,
                "topic_id": topic_id,
                "status": self._ipfs_client.add(f"{self.sync_directory}/status.txt")["Hash"],
                "rff": self._ipfs_client.add(f"{self.sync_directory}/rff.txt")["Hash"],
                "swarm_key": self.listener_swarm_key_hash
            }
            # publish message(listener_data) for topic(topic_id) via pubsub within the chain swarm
            self._ipfs_pubsub_publish(topic=topic_id, message=json.dumps(listener_data))
        except Exception as error:
            print(f"IPFS pubsub publish error: {error}")
            raise error
        finally:
            # switch current swarm to listener swarm
            self.switch_to_listener_swarm(listener_swarm_key_hash=self.listener_swarm_key_hash)
    
    async def periodic_publish_status(self, topic_id:int=None, interval:int=10):
        assert topic_id is not None
        while True:
            await self.publish_status(topic_id=topic_id)
            await asyncio.sleep(interval)

    def kuri_registry_file_name(self, topic_id:str=None) -> str:
        assert topic_id is not None
        return f"{self.sync_directory}/{topic_id}/kuris.json"

    def get_sync_location(self, filters:dict={}) -> str:
        return self.kuri_registry_file_name(topic_id=filters["topic_id"][1:-1])

    def __handle_subscription_topic_arikuris_from_committer(self, data, seqno, topic_ids, cid, subscription):
        print(f"\n\nSUBSCRIBED MESSAGE RECIEVED!")
        print(f"Data: {data}")
        print(f"Seqno: {seqno}")
        print(f"Topic IDs: {topic_ids}")
        print(f"Message CID: {cid}")
        print(f"\n\n")
        kuri = topic_ids[0].decode("utf-8")
        data = json.loads(data.decode("utf-8"))
        kuri_cid = data["cid"]
        kuri_file_name = data["file_name"]
        # check if kuri exists in data/mappings.json
        with open(f"{self.data_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
            if kuri not in mappings:
                print(f"\nKURI NOT FOUND IN MAPPINGS : {kuri}")
                try:
                    # pin the file
                    print(f"Pinning file CID ({kuri_cid}) for kuri {kuri} ...")
                    res = self._ipfs_client.pin.add(kuri_cid)
                    print(f"pin response : {res}")
                except TimeoutError:
                    raise StorageError(
                        f"\n\n\n\nEncountered an error while saving kuri {kuri}\n\nIs the CID {kuri_cid} visible on your IPFS client?\n\n"
                    )
                # add the file from cid to data directory
                print(f"Adding file CID ({kuri_cid}) for kuri {kuri} to data directory ...")
                with open(f"{self.data_directory}/{kuri_file_name}", "wb") as f:
                    f.write(self._ipfs_client.cat(kuri_cid))
                # add the kuri to mappings
                mappings[kuri] = f"{self.data_directory}/{kuri_file_name}"
                with open(f"{self.data_directory}/mappings.json", "w") as f:
                    json.dump(mappings, f)
                print(f"KURI {kuri} added to mappings")
                # remove the kuri from sync/rff.txt if it exists
                kuris_in_rff = []
                with open(f"{self.sync_directory}/rff.txt", "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            kuris_in_rff.append(line)
                print(f"{kuris_in_rff = }")
                if kuri in kuris_in_rff:
                    kuris_in_rff.remove(kuri)
                    with open(f"{self.sync_directory}/rff.txt", "w") as f:
                        for kuri in kuris_in_rff:
                            f.write(f"{kuri}")
                # unsubscribe from the kuri
                self._ipfs_pubsub_unsubscribe(topic=kuri)

    def save_kuri(self, kuri, filters:dict={}):
        # save kuri to status.txt if it doesn't exist
        kuris_in_status = []
        with open(f"{self.sync_directory}/status.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    kuris_in_status.append(line)
        print(f"{kuris_in_status = }")
        if kuri not in kuris_in_status:
            kuris_in_status.append(kuri)
            with open(f"{self.sync_directory}/status.txt", "a") as f:
                f.write(f"\n{kuri}")
        # check if kuri exists in data/mappings.json
        with open(f"{self.data_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
            if kuri not in mappings:
                print(f"\nKURI NOT FOUND IN MAPPINGS : {kuri}")
                # if not, add it to sync/rff.txt if it doesn't exist
                kuris_in_rff = []
                with open(f"{self.sync_directory}/rff.txt", "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            kuris_in_rff.append(line)
                print(f"{kuris_in_rff = }")
                if kuri not in kuris_in_rff:
                    with open(f"{self.sync_directory}/rff.txt", "a") as f:
                        f.write(f"\n{kuri}")
                print(f"SUBSCRIBING TO KURI: {kuri}")
                # subscribe to kuri via pubsub within listener swarm
                try:
                    # switch current swarm to listener swarm
                    self.switch_to_listener_swarm(listener_swarm_key_hash=self.listener_swarm_key_hash)
                    self._ipfs_pubsub_subscribe(topic=kuri, handler=self.__handle_subscription_topic_arikuris_from_committer)
                except Exception as error:
                    print(f"Error subscribing to {kuri}: {error}")

    def sync_with_topic(self,
            topic_id:int=None,
            direction:str=None, start_block_number:any=None, block_count:any=None, finalized_only:bool=False
        ) -> None:
        assert topic_id is not None
        topic_id = str(topic_id)
        direction = direction or FUTURE
        self.topic_set.add(topic_id)
        # create sync/topic_id if it doesn't exist
        self._set_or_create_directory(f"{self.sync_directory}/{topic_id}")
        # create kuris.json in sync/topic_id if it doesn't exist
        self._set_or_create_file(path=f"{self.sync_directory}/{topic_id}/kuris", extension="json")
        filters = {
            "topic_id": f"^{topic_id}$"
        }
        self.sync(direction, start_block_number, block_count, finalized_only, filters=filters)
