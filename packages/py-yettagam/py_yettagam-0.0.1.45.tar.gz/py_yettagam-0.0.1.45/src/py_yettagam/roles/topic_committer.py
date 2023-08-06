# Author: MetariumProject

# Standard libraries
import json
import os
from pathlib import Path
import shutil
import time
# Third party libraries
from ipfshttpclient.exceptions import (
    ConnectionError,
    TimeoutError,
    StatusError,
    TimeoutError,
)
from substrateinterface import SubstrateInterface, Keypair
# Metarium libraries
from py_metarium import (
    FUTURE,
)
from py_metarium_listener import (
    QueryParameter,
)
from py_metarium_encoder import (
    SubstrateAriKuriAdderAsTopicCommitterNode,
    AriKuriAlreadyExistsError,
)
# local libraries
from ..utils import (
    TopicDoesNotExistError,
    TopicInactiveError,
    SwarmKeyDoesNotExistError,
    ListenerDoesNotExistError,
    ListenerDeletedError,
    MaliciousListenerError,
)

from ..pubsub import (
    IPFSPubSub,
)

from ..storage import (
    StorageBase,
    HasherBase,
    IPFSClient,
)


class TopicCommitter(IPFSPubSub, StorageBase, HasherBase, IPFSClient):
    """
        A Yettagam Scribe can perform the following functions:
        [x] Add Arikuris, aka, Kuris to a Topic
        [x] Listen to Topic updates from a Topic Listener via Chain-swarm
        [#] Connect to a Topic Listener via Listener-swarm
        [x] Sync with a Topic Listener via Listener-swarm
    """

    SUBSTRATE_EXTRINSIC = "Metarium"

    BLAKE3 = "blake3"

    def __init__(self, node_url:str=None, chain_swarm_key_path:str=None, path:str=None, **encoder_kwargs) -> None:

        assert node_url is not None
        assert chain_swarm_key_path is not None and os.path.exists(chain_swarm_key_path)
        assert "mnemonic" in encoder_kwargs or "uri" in encoder_kwargs

        # initialize IPFSPubSub class
        IPFSPubSub.__init__(self)
        # initialize StorageBase class
        StorageBase.__init__(self)
        # initialize HasherBase class
        HasherBase.__init__(self)
        # initialize IPFSClient class
        IPFSClient.__init__(self)

        if "mnemonic" in encoder_kwargs:
            self.key_pair = Keypair.create_from_mnemonic(encoder_kwargs["mnemonic"])
        elif "uri" in encoder_kwargs:
            self.key_pair = Keypair.create_from_uri(encoder_kwargs["uri"])

        self.metarium_node_url = node_url

        self.kuri_creator = SubstrateAriKuriAdderAsTopicCommitterNode(url=node_url, **encoder_kwargs)

        self.data_file_set = set()
        self.swarm_file_set = set()

        self.__setup(node_url=node_url, path=path or f"{Path().resolve()}", chain_swarm_key_path=chain_swarm_key_path)

    def __setup(self, node_url:str=None, path:str=None, chain_swarm_key_path:str=None):
        assert node_url is not None
        assert path is not None
        # IPFS
        self._setup_ipfs_client()
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
        # setup swarm key mapping
        self.chain_swarm_key_hash = self._setup_swarm_key_mapping(
            swarm_key_file_name="chain.key",
            swarm_key_path=chain_swarm_key_path
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

    def watch_swarm_data(self, topic_id:int=None, interval:int=2):
        assert topic_id is not None
        while True:
            time.sleep(interval)
            self.watch_swarm_directory()
            self.watch_data_directory(topic_id=topic_id)

    def watch_swarm_directory(self):
        for file in os.listdir(self.swarm_directory):
            # ignore mappings.json and hidden files
            if (
                (file == "mappings.json") or (file.startswith(".")) or (file in self.swarm_file_set)
                ):
                continue
            self.swarm_file_set.add(file)
            swarm_key_data = {
                "type": "file",
                "content": os.path.join(self.swarm_directory, file)
            }
            self.__update_swarm_mappings(data=swarm_key_data, return_file_hash=False)

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
        print(f"Switched to chain swarm key: {self.chain_swarm_key_hash}")
    
    def switch_to_listener_swarm(self, listener_swarm_key_hash:str=None):
        assert listener_swarm_key_hash is not None
        self._set_listener_swarm_key(listener_swarm_key_hash=listener_swarm_key_hash)
        self._set_ipfs_swarm_key()
        print(f"Switched to listener swarm key: {listener_swarm_key_hash}")

    def connect_to_listener_node(self, listener_ip_address:str=None, listener_ipfs_id:str=None):
        assert listener_ip_address is not None
        assert listener_ipfs_id is not None
        if listener_ip_address != "127.0.0.1":
            # add listener to ipfs swarm peers list
            print(f"Adding listener node to swarm peers: {listener_ip_address}")
            self._ipfs_client.swarm.filters.add(f"/ip4/{listener_ip_address}/udp/4001/quic/p2p/{listener_ipfs_id}")
            # connect to listener as ipfs swarm peer
            print(f"Connecting to listener node: {listener_ip_address}")
            self._ipfs_client.swarm.connect(f"/ip4/{listener_ip_address}/tcp/4001/p2p/{listener_ipfs_id}")
    
    def disconnect_from_listener_node(self, listener_ip_address:str=None, listener_ipfs_id:str=None):
        assert listener_ip_address is not None
        assert listener_ipfs_id is not None
        if listener_ip_address != "127.0.0.1":
            # remove listener from ipfs swarm peers list
            print(f"Removing listener node from swarm peers: {listener_ip_address}")
            self._ipfs_client.swarm.filters.rm(f"/ip4/{listener_ip_address}/udp/4001/quic/p2p/{listener_ipfs_id}")
            # disconnect from listener as ipfs swarm peer
            print(f"Disconnecting from listener node: {listener_ip_address}")
            self._ipfs_client.swarm.disconnect(f"/ip4/{listener_ip_address}/tcp/4001/p2p/{listener_ipfs_id}")


    def watch_data_directory(self, topic_id:int=None):
        assert topic_id is not None
        for file in os.listdir(self.data_directory):
            # ignore mappings.json and hidden files
            if file == "mappings.json" or file.startswith("."):
                continue
            if file not in self.data_file_set:
                self.data_file_set.add(file)
                kuri_data = {
                    "topic_id": topic_id,
                    "type": "file",
                    "content": os.path.join(self.data_directory, file)
                }
                try:
                    transaction_hash = self.create_kuri(data=kuri_data)
                    if transaction_hash:
                        print(f"New file uploaded: {file}")
                except AriKuriAlreadyExistsError:
                    pass
                self.__update_data_mappings(data=kuri_data)
    
    def _arikuri_hash(self, data:dict=None) -> str:        
        return f"|>{self.__class__.BLAKE3}|{self._blake3_hash(data=data)}"

    def __update_data_mappings(self, data:dict=None):
        assert data is not None
        with open(f"{self.data_directory}/mappings.json", "r") as f:
            mappings = json.load(f)
        arikuri_hash = self._arikuri_hash(data=data)
        if arikuri_hash not in mappings:
            mappings[arikuri_hash] = data["content"]
            with open(f"{self.data_directory}/mappings.json", "w") as f:
                json.dump(mappings, f)

    def create_kuri(self, data:dict=None) -> str:
        assert data is not None
        transaction_hash = self.kuri_creator.encode(
            data=data,
            wait_for_inclusion=True,
            wait_for_finalization=False
        )
        
        return transaction_hash

    def create_query(self, filters:dict={}) -> list:
        query = []
        for field, value in filters.items():
            query.append(
                QueryParameter(field, f"^{value}$")
            )
        return query

    def __get_listener_info(self, listener_address:str=None, topic_id:int=None) -> tuple:
        assert topic_id is not None
        assert listener_address is not None
        # get the listener info
        query_result = SubstrateInterface(url=self.metarium_node_url).query(
            module=self.__class__.SUBSTRATE_EXTRINSIC,
            storage_function="TopicListenerNodes",
            params=[str(topic_id), listener_address],
        )
        listener = query_result.serialize()
        print(f"{listener = }")
        # check if the listener is active (aka, not deleted), and is a valid listener for the topic
        if listener is None:
            raise ListenerDoesNotExistError(f"Listener does not exist: {listener_address}")
        else:
            if listener["deleted"]:
                raise ListenerDeletedError(f"Listener has been deleted: {listener_address}")
        # get the listener's ipfs id, ip address, and swarm key hash
        return listener["ip_address"], listener["id"], listener["swarm_key"]

    def __handle_subscription_topic_updates_from_listener(self, data, seqno, topic_ids, cid, subscription):
        print(f"\n\nSUBSCRIBED MESSAGE RECIEVED!")
        print(f"Data: {data}")
        print(f"Seqno: {seqno}")
        print(f"Topic IDs: {topic_ids}")
        print(f"Message CID: {cid}")
        print(f"\n\n")
        topic_id = topic_ids[0].decode("utf-8")
        data = json.loads(data.decode("utf-8"))

        listener_address = data["caller"]
        # check if the listener_address is a valid listener for the topic
        ip_address, ipfs_id, swarm_key_hash = self.__get_listener_info(listener_address=listener_address, topic_id=topic_id)
        # check if the listener's swarm key hash is the same as the one in the message
        if swarm_key_hash != data["swarm_key"]:
            raise MaliciousListenerError(f"Swarm keys do not match!\nFrom chain  : {swarm_key_hash}\nFrom message: {data['swarm_key_hash']}")
        # get the status and rff from the listener
        status = data["status"]
        rff = data["rff"]
        # create directory for listener of the topic if it doesn't exist
        listener_directory = f"{self.sync_directory}/{topic_id}/{listener_address}"
        self._set_or_create_directory(f"{listener_directory}")
        # create status.txt in listener_directory if it doesn't exist
        self._set_or_create_file(path=f"{listener_directory}/status", extension="txt")
        # create rff.txt in listener_directory if it doesn't exist
        self._set_or_create_file(path=f"{listener_directory}/rff", extension="txt")
        with open(f"{listener_directory}/status.txt", "w") as f:
            f.write(status)
        with open(f"{listener_directory}/rff.txt", "w") as f:
            f.write(rff)
        print(f"Topic Listener status updated: {status}")
        print(f"Topic Listener rff updated: {rff}")
        # switch current swarm to listeners swarm
        self.switch_to_listener_swarm(listener_swarm_key_hash=swarm_key_hash)
        self.connect_to_listener_node(listener_ip_address=ip_address, listener_ipfs_id=ipfs_id)

        # open rff as IPFS CID
        try:
            rff_file = self._ipfs_client.cat(rff)
            print(f"\n\nRFF FILE CONTENTS:\n{rff_file}\n\n")
            kuris_to_pubish = [decoded for decoded in rff_file.decode("utf-8").split("\n") if decoded != ""]
            print(f"KURIS TO PUBLISH:\n{kuris_to_pubish}\n")
            with open(f"{self.data_directory}/mappings.json", "r") as f:
                mappings = json.load(f)
                print(f"MAPPINGS:\n{mappings}\n")
                for kuri in kuris_to_pubish:
                    print(f"\n\nKURI TO PUBLISH: {kuri}")
                    # check if kuri exists in mappings.json
                    print(f"KURI IN MAPPINGS: {kuri in mappings}")
                    if kuri in mappings:
                        content = mappings[kuri]
                        print(f"\nKURI FOUND IN MAPPINGS : {content}")
                        # get file name from the content
                        file_name = content.split("/")[-1]
                        # create IPFS CID from content
                        ipfs_cid = self._ipfs_client.add(content)
                        print(f"IPFS CID CREATED : {ipfs_cid['Hash']}")
                        # publish IPFS CID to IPFS pubsub
                        try:
                            message = {"cid": ipfs_cid['Hash'], "file_name": file_name}
                            self._ipfs_pubsub_publish(topic=kuri, message=json.dumps(message))
                        except Exception as error:
                            print(f"IPFS pubsub publish error: {error}")
        except TimeoutError:
            print(f"IPFS timeout error. Is your IPFS client connected to the Listener's IPFS client?\n{TimeoutError}")
        # disconnect from listener node
        self.disconnect_from_listener_node(listener_ip_address=ip_address, listener_ipfs_id=ipfs_id)
        # switch back current swarm to chain swarm
        self.switch_to_chain_swarm()

    def sync_to_topic(self, topic_id:int=None, interval:int=3600) -> str:
        assert topic_id is not None
        topic_id = str(topic_id)
        # check if topic is un-archived on chain
        query_result = SubstrateInterface(url=self.metarium_node_url).query(
            module=self.__class__.SUBSTRATE_EXTRINSIC,
            storage_function="Topics",
            params=[topic_id],
        )
        topic = query_result.serialize()
        if topic is None:
            raise TopicDoesNotExistError(f"Topic does not exist: {topic_id}")
        else:
            if topic["archived"]:
                raise TopicInactiveError(f"Topic has been archived: {topic_id}")

        # check if swarm/chain.key exists
        if not os.path.exists(f"{self.swarm_directory}/chain.key"):
            raise SwarmKeyDoesNotExistError(f"Swarm key for listening to the chain does not exist: {self.swarm_directory}/chain.key")

        # switch current swarm to chain swarm
        self.switch_to_chain_swarm()

        # create directory for topic if it doesn't exist
        topic_directory = f"{self.sync_directory}/{topic_id}"
        self._set_or_create_directory(f"{topic_directory}")
        
        while True:
            # subscribe to topic updates
            self._ipfs_pubsub_subscribe(topic=str(topic_id), handler=self.__handle_subscription_topic_updates_from_listener)
            # sleep for interval
            time.sleep(interval)
