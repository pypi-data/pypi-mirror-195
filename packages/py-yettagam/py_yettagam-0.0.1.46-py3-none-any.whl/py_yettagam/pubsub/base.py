# Author: MetariumProject

# Standard libraries
import io
import json
# Third party libraries
import multibase
import requests


class PubSubBase(object):

    def __init__(self) -> None:
        self._subscribers = {}
        
    def _subscribe(self, topic:str=None, ip:str="127.0.0.1", port:int=5001, callback=None):
        seq_offset = -1
        with requests.post("http://"+ip+":"+str(port)+"/api/v0/pubsub/sub?arg="+multibase.encode("base64url", topic).decode("utf8"), stream=True) as r:
            self._subscribers[topic][0].append(r)
            while True:
                try:
                    for m in r.iter_lines():
                        j = json.loads(m.decode("utf8"))
                        j["data"] = multibase.decode(j["data"])
                        j["seqno"] = int.from_bytes(multibase.decode(j["seqno"]),"big")

                        if seq_offset == -1:
                            seq_offset = j["seqno"]
                        j["seqno"] = j["seqno"] - seq_offset

                        for i in range(len(j["topicIDs"])):
                            j["topicIDs"][i] = multibase.decode(j["topicIDs"][i])
                        
                        if callback is not None:
                            callback(data=j["data"],seqno=j["seqno"],topic_ids=j["topicIDs"],cid=j["from"], subscription=r)
                except:
                    if not topic in self._subscribers.keys() or self._subscribers[topic][1] == False:
                        return

    def _unsubscribe(self, topic:str=None):
        if topic in self._subscribers.keys():
            print(f"Unsubscribing from topic: {topic}")
            for i in range(len(self._subscribers[topic][0])-1,-1,-1):
                if not self._subscribers[topic][0][i] is None:
                    self._subscribers[topic][0][i].close()
                    self._subscribers[topic][0][i] = None
            self._subscribers[topic][1] = False
        else:
            print(f"Topic {topic} not found in subscribers!")

    def _publish(self, topic:str=None, message:str=None, ip:str="127.0.0.1", port:int=5001):
        file = io.BytesIO(message if type(message) == bytes else message.encode("utf8"))

        files = {'file': file}

        print(f"Publishing message {message} for topic {topic} to {ip}:{port} with files {files} ...")
        requests.post("http://"+ip+":"+str(port)+"/api/v0/pubsub/pub?arg="+multibase.encode("base64url",topic).decode("utf8"),files=files)

