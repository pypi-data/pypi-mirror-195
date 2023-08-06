
import os

class StorageBase(object):

    def _set_or_create_directory(self, path:str):
        if not os.path.exists(path):
            os.makedirs(path)

    def _set_or_create_file(self, path:str=None, extension:str=None):
        assert path is not None
        assert extension is not None
        if not os.path.exists(f"{path}.{extension}"):
            with open(f"{path}.{extension}", "w") as f:
                if extension == "json":
                    f.write("{}")
                elif extension == "txt":
                    f.write("")