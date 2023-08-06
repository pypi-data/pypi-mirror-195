
from blake3 import blake3

class HasherBase(object):

    def _blake3_hash(self, data:dict=None) -> str:
        # Create a Blake3 hash object
        hasher = blake3(max_threads=blake3.AUTO)
        with open(data["content"], "rb") as f:
            counter = 0
            while True:
                counter += 1
                content = f.read(1024)
                if not content:
                    break
                hasher.update(content)
        
        return hasher.hexdigest()
