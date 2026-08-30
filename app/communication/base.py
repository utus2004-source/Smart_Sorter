class Communication:
    # Interface for every communication implementation.
    # it only produces a command that is passed here.

    def connect(self):
        raise NotImplementedError

    def send(self, command):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
