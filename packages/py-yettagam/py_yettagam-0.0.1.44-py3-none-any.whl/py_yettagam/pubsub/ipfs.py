# Author: MetariumProject

# Standard libraries
import threading


from .base import PubSubBase


class IPFSPubSub(PubSubBase):

    def __init__(self):
        super().__init__()

    def _ipfs_pubsub_publish(self, topic:str=None, message:str=None, listener_ip_address:str="127.0.0.1", port:int=5001):
        assert topic is not None
        assert message is not None
        self._publish(topic=topic, message=message, ip=listener_ip_address, port=port)

    def _ipfs_pubsub_unsubscribe(self, topic:str=None):
        assert topic is not None
        self._unsubscribe(topic=topic)

    def _ipfs_pubsub_subscribe(self, topic:str=None, handler=None):
        assert topic is not None
        assert handler is not None
        if not topic in self._subscribers.keys():
            self._subscribers[topic] = [[],True]
        self._subscribers[topic][1] = True

        th = threading.Thread(target=self._subscribe, kwargs={"topic":topic, "callback":handler})
        th.daemon = True
        th.start()