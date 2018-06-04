class ModelInitializationException(Exception):
    """Raised if parsing of yaml file fails for any reason."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

