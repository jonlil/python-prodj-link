import unittest
from packets import DBMessage
import dataprovider
from dbclient import DBClient
from construct import Container


class DbclientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = DBClient('mock_prodj')

    def test_parsing_root_metadata_payload(self):
        self.assertEqual({
                'menu_id': 22,
                'name': '\ufffaARTIST\ufffb',
            },
            self.client.parse_metadata_payload(Container(args=[
                Container(type='int32')(value=0),
                Container(type='int32')(value=22),
                Container(type='int32')(value=20),
                Container(type='string')(value='\ufffaARTIST\ufffb'),
                Container(type='int32')(value=2),
                Container(type='string')(value=''),
                Container(type='int32')(value=149),
                Container(type='int32')(value=0),
                Container(type='int32')(value=0),
                Container(type='int32')(value=0),
                Container(type='int32')(value=0),
                Container(type='int32')(value=0),
            ]).args),
        )

        self.assertEqual({
            'menu_id': 3,
            'name': '\ufffaALBUM\ufffb',
        }, self.client.parse_metadata_payload(Container(args=[
            Container(type='int32')(value=0),  # 0
            Container(type='int32')(value=3),  # 1
            Container(type='int32')(value=16),  # 2
            Container(type='string')(value='\ufffaALBUM\ufffb'),  # 3
            Container(type='int32')(value=2),  # 4
            Container(type='string')(value=''),  # 5
            Container(type='int32')(value=130),  # 6
            Container(type='int32')(value=0),
            Container(type='int32')(value=0),
            Container(type='int32')(value=0),
            Container(type='int32')(value=0),
            Container(type='int32')(value=0),
        ]).args))
