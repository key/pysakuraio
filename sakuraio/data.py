import binascii
from datetime import datetime
from dateutil import parser as date_parser

TYPE_MAPPING = {
    'i': int,
    'I': int,
    'l': int,
    'L': int,
    'f': float,
    'd': float,
    'b': bin,
}


class BaseData(object):
    datetime: datetime = None

    def __init__(self, payload):
        self.datetime = date_parser.parse(payload['datetime'])


class ChannelData(BaseData):
    data_type: str = 'channel'
    channel: int = None
    type_: type = None
    type_str: str = None
    value: str = None

    def __init__(self, payload: dict):
        super(ChannelData, self).__init__(payload)
        self.channel = payload['channel']
        self.type_str = payload['type']
        self.type_ = TYPE_MAPPING[payload['type']]
        if payload['type'] == 'b':
            self.value = binascii.unhexlify(payload['value'])
        else:
            self.value = self.type_(payload['value'])

    def __str__(self):
        return 'datetime=%s, type=%s, channel=%d, value=%s' % (self.datetime, self.data_type, self.channel, self.value)

    def as_dict(self):
        return {
            'type': self.type_str,
            'channel': self.channel,
            'value': self.value if self.type_ != bin else self.value.hex(),
            'datetime': self.datetime.isoformat()
        }


class ChannelDataSet(object):
    """Collection object of ChannelData
    """
    module: str = ''
    datetime: datetime = None  # NOTE: datetime doesn't have timezone
    data = []

    def __init__(self, module: str, datetime_: datetime, lst: [ChannelData]):
        self.module = module
        self.datetime = datetime_
        self.data = lst

    def as_dict(self):
        return {
            'module': self.module,
            'datetime': self.datetime.isoformat(),
            'type': 'channels',
            'payload': {
                'channels': [d.as_dict() for d in self.data]
            }
        }


class ConnectionData(BaseData):
    # module identifier
    module = None
    is_online = None

    def __init__(self, payload):
        super(ConnectionData, self).__init__(payload)
        self.module = payload['module']
        self.is_online = payload['payload']['is_online']

    def __str__(self):
        return 'datetime=%s, module=%s, is_online=%s' % (self.datetime, self.module, self.is_online)


class KeepAliveData(BaseData):
    def __init__(self, payload):
        super(KeepAliveData, self).__init__(payload)

    def __str__(self):
        return 'datetime=%s' % self.datetime
