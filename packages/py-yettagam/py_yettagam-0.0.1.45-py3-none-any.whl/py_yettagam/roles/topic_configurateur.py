# Author: MetariumProject

# Third party libraries
from substrateinterface import Keypair
# Metarium libraries
from py_metarium_encoder import (
    SubstrateTopicListenerAdderAsConfigurationNode,
)

from ..storage import (
    HasherBase,
)


class TopicConfigurateur(HasherBase):
    """
        A Yettagam Topic Configurateur can perform the following functions:
        [x] Create a new Listener for a Topic
    """

    SUBSTRATE_EXTRINSIC = "Metarium"

    def __init__(self, node_url:str=None, path:str=None, **encoder_kwargs) -> None:
        assert node_url is not None
        assert "mnemonic" in encoder_kwargs or "uri" in encoder_kwargs

        # initialize HasherBase class
        HasherBase.__init__(self)

        if "mnemonic" in encoder_kwargs:
            self.key_pair = Keypair.create_from_mnemonic(encoder_kwargs["mnemonic"])
        elif "uri" in encoder_kwargs:
            self.key_pair = Keypair.create_from_uri(encoder_kwargs["uri"])

        self.metarium_node_url = node_url

        self.listener_adder = SubstrateTopicListenerAdderAsConfigurationNode(url=node_url, **encoder_kwargs)

    def node_added_to_topic_listener_set(self,
            listener_data:dict=None, listener_mnemonic:str=None, swarm_key_path:str=None) -> str:
        assert listener_data is not None
        assert listener_mnemonic is not None
        assert swarm_key_path is not None

        listener_key = Keypair.create_from_mnemonic(mnemonic=listener_mnemonic)
        listener_data["node"] = listener_key.ss58_address

        swarm_key_data = {
            "type": "file",
            "content": swarm_key_path
        }
        listener_data["swarm_key"] = self._blake3_hash(data=swarm_key_data)
        listener_data["status"] = ""
        listener_data["rff"] = ""

        transaction_hash = self.listener_adder.encode(
            data=listener_data,
            wait_for_inclusion=True,
            wait_for_finalization=False
        )
        return transaction_hash
