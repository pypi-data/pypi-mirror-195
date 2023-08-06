class TopicDoesNotExistError(Exception):
    pass

class TopicInactiveError(Exception):
    pass

class StorageConnectionRefusedError(Exception):
    pass

class StorageError(Exception):
    pass

class SwarmKeyDoesNotExistError(Exception):
    pass
