from datetime import datetime
from struct import pack
from unittest import TestCase

class SakuraIODataSetTestCase(TestCase):

    maxDiff = 4000

    def test_channel_data(self):
        from sakuraio.data import ChannelData

        now = datetime.utcnow()
        isonow = now.isoformat()
        timestamp = now.timestamp() * (10 ** 3)

        ch0 = ChannelData({'datetime': isonow, 'channel': 0, 'type': 'L',
                           'value': timestamp})  # timestamp
        self.assertDictEqual({
            'channel': 0,
            'type': 'L',
            'value': int(timestamp),
            'datetime': isonow
        }, ch0.as_dict())

    def test_channel_dataset(self):
        from sakuraio.data import ChannelData
        from sakuraio.data import ChannelDataSet

        module = 'xxxxxxxx'
        now = datetime.utcnow()
        isonow = now.isoformat()
        timestamp = now.timestamp() * (10 ** 3)
        ch0 = ChannelData({'datetime': isonow, 'channel': 0, 'type': 'L',
                           'value': timestamp})  # timestamp
        ch1 = ChannelData({'datetime': isonow, 'channel': 1, 'type': 'b',
                           'value': pack('<2f', 40.0, 140.0).hex()})  # location
        ch2 = ChannelData({'datetime': isonow, 'channel': 2, 'type': 'b',
                           'value': pack('<f2H', 3776.8, 58, 124).hex()})  # altitude, hdop, vdop
        ch3 = ChannelData({'datetime': isonow, 'channel': 3, 'type': 'b',
                           'value': pack('<fH2x', 18.5, 5).hex()})  # speed, course
        ch4 = ChannelData({'datetime': isonow, 'channel': 4, 'type': 'b',
                           'value': pack('<3B5x', 1, 1, 125).hex()})  # meta data
        ch5 = ChannelData({'datetime': isonow, 'channel': 5, 'type': 'b',
                           'value': pack('<h2H2x', 3022, 10130, 2520).hex()})  # environment

        message = ChannelDataSet(module, now, [ch0, ch1, ch2, ch3, ch4, ch5])
        self.assertDictEqual({
            'module': module,
            'datetime': now.isoformat(),
            'type': 'channels',
            'payload': {
                'channels': [
                    {
                        'channel': 0,
                        'type': 'L',
                        'datetime': isonow,
                        'value': int(timestamp),
                    },
                    {
                        'channel': 1,
                        'type': 'b',
                        'datetime': isonow,
                        'value': pack('<2f', 40.0, 140.0).hex(),
                    },
                    {
                        'channel': 2,
                        'type': 'b',
                        'datetime': isonow,
                        'value': pack('<f2H', 3776.8, 58, 124).hex(),
                    },
                    {
                        'channel': 3,
                        'type': 'b',
                        'datetime': isonow,
                        'value': pack('<fH2x', 18.5, 5).hex(),
                    },
                    {
                        'channel': 4,
                        'type': 'b',
                        'datetime': isonow,
                        'value': pack('<3B5x', 1, 1, 125).hex(),
                    },
                    {
                        'channel': 5,
                        'type': 'b',
                        'datetime': isonow,
                        'value': pack('<h2H2x', 3022, 10130, 2520).hex(),
                    },
                ]
            }
        }, message.as_dict())

