class InvalidJSONException(Exception):
    """Throw this exception when getting invalid JSON
    """
    pass


class InvalidChannelException(Exception):
    """Invalid channel data format
    """
    pass


class InvalidConnectionException(Exception):
    """Invalid connection data format
    """
    pass


class InvalidTypeException(Exception):
    """Invalid data type
    """
    pass
