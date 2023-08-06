
# Standard libraries
import time
# Third party libraries
import ipfshttpclient
from ipfshttpclient.exceptions import (
    ConnectionError,
)
# local libraries
from ..utils import (
    StorageConnectionRefusedError,
)

class IPFSClient(object):
    """
        A Yettagam IPFSClient can perform the following functions:
        [x] Connect to the local IPFS node
        [x] Change the swarm key to connect to a remote IPFS network
    """

    RECONNECTION_WAIT_DURATION_SECONDS = 5
    MAX_RECONNECTION_ATTEMPTS = 10

    def _setup_ipfs_client(self):
        reconnection_attempts = 1
        while True:
            try:
                self._ipfs_client = ipfshttpclient.connect(session=True)
            except ConnectionError:
                if reconnection_attempts == self.__class__.MAX_RECONNECTION_ATTEMPTS:
                    print(f"IPFS connection terminated after {reconnection_attempts} attempts.")
                    raise StorageConnectionRefusedError
                print(f"IPFS connection refused. Retrying in {self.__class__.RECONNECTION_WAIT_DURATION_SECONDS} seconds ...")
                reconnection_attempts += 1
                time.sleep(self.__class__.RECONNECTION_WAIT_DURATION_SECONDS)
                continue
            break
