class Camera:
    # Interface for every camera implementation.
    # The pipeline only uses these methods and does not know
    # which concrete implementation it received.

    def open(self):
        raise NotImplementedError

    def get_frame(self):
        raise NotImplementedError

    def is_open(self):
        raise NotImplementedError

    def print_info(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError
