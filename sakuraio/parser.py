# coding=utf-8
import json

from dateutil import parser as date_parser

from .data import ChannelData, ConnectionData, KeepAliveData, ChannelDataSet
from .error import InvalidJSONException


class ChannelsParser(object):
    @staticmethod
    def parse(json_value):
        try:
            data = json.loads(json_value)
            module = data['module']
            datetime = date_parser.parse(data['datetime'])
            channels = data['payload']['channels']
            return ChannelDataSet(module, datetime, [ChannelData(payload) for payload in channels])
        except:
            raise InvalidJSONException


class ConnectionParser(object):
    @staticmethod
    def parse(json_value):
        try:
            value = json.loads(json_value)
            return ConnectionData(value)
        except:
            raise InvalidJSONException


class KeepAliveParser(object):
    @staticmethod
    def parse(json_value):
        try:
            value = json.loads(json_value)
            return KeepAliveData(value)
        except:
            raise InvalidJSONException


class SakuraIOParser(object):
    """`type` に応じたパーサインスタンスを返す。
    """

    @staticmethod
    def factory(json_value):
        try:
            value = json.loads(json_value)
            t = value.get('type', None)
            if t is None:
                raise TypeError
        except:
            raise
            # return None

        if t == 'channels':
            return ChannelsParser
        elif t == 'connection':
            return ConnectionParser
        elif t == 'keepalive':
            return KeepAliveParser
