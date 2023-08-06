from os import environ


class Config:
    MAX_CONTENT_SIZE = 1024 * 4
    """The maximum request content size allowed. Should
    be set to a sane value to prevent DoS-Attacks.
    """

    def __init__(self):
        # todo: initialize values from ENV ot default
        ...


rpc_config = Config()
