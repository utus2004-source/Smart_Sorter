class Communication:
    # Interface for every communication implementation.
    # The decision logic never talks to the hardware directly,
    # it only produces a command that is passed here.

    def connect(self):
        raise NotImplementedError

    def send(self, command):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError
