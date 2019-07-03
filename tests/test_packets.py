import unittest
from packets import DBField, DBMessage, ManyDBMessages
from construct import Container
import fixtures

import pprint
pa = pprint.PrettyPrinter(indent=2)


class PacketsTestCase(unittest.TestCase):
    def test_string_parsing(self):
        self.assertEqual(
            DBField.parse(
                b"\x26\x00\x00\x00\x0a\xff\xfa\x00\x48\x00\x49\x00" +
                b"\x53\x00\x54\x00\x4f\x00\x52\x00\x59\xff\xfb\x00\x00"
            ),
            Container(type='string')(value="\ufffaHISTORY\ufffb"),
        )

        self.assertEqual(
            DBField.parse(
                b"\x26\x00\x00\x00\x0b\xff\xfa\x00\x50\x00\x4c\x00" +
                b"\x41\x00\x59\x00\x4c\x00\x49\x00\x53\x00\x54\xff\xfb" +
                b"\x00\x00"
            ),
            Container(type='string')(value="\ufffaPLAYLIST\ufffb"),
        )

        self.assertEqual(
            DBField.parse(bytes([
                0x26, 0x00, 0x00, 0x00, 0x09, 0xff, 0xfa, 0x00, 0x41,
                0x00, 0x52, 0x00, 0x54, 0x00, 0x49, 0x00, 0x53,
                0x00, 0x54, 0xff, 0xfb, 0x00, 0x00,
            ])),
            Container(type='string')(value="\ufffaARTIST\ufffb"))

    def test_parsing_unwrapped_string(self):
        self.assertEqual(
            DBField.parse(bytes([
                0x26, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x4c, 0x00, 0x6f, 0x00, 0x6f, 0x00,
                0x70, 0x00, 0x6d, 0x00, 0x61, 0x00, 0x73, 0x00, 0x74, 0x00, 0x65, 0x00,
                0x72, 0x00, 0x73, 0x00, 0x00,
            ])),
            Container(type='string')(value="Loopmasters"))

    def test_parsing_artist_request(self):
        message = DBField.parse(fixtures.artist_request)

    def test_building_root_menu_request_menu_item_artist_part(self):
        data = bytes([
            0x11, 0x87, 0x23, 0x49, 0xae, 0x11, 0x05, 0x80, 0x00, 0x01, 0x10,
            0x41, 0x01, 0x0f, 0x0c, 0x14, 0x00, 0x00, 0x00, 0x0c, 0x06, 0x06,
            0x06, 0x02, 0x06, 0x02, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x11,
            0x00, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x16, 0x11, 0x00,
            0x00, 0x00, 0x14, 0x26, 0x00, 0x00, 0x00, 0x09, 0xff, 0xfa, 0x00,
            0x41, 0x00, 0x52, 0x00, 0x54, 0x00, 0x49, 0x00, 0x53, 0x00, 0x54,
            0xff, 0xfb, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x02, 0x26, 0x00,
            0x00, 0x00, 0x01, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x95, 0x11,
            0x00, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00,
            0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00,
            0x00, 0x00,
        ])

        message = DBMessage.parse(data)
        self.assertEqual(message.type, 'menu_item')
        self.assertEqual(
            message,
            (Container
                (magic=2267236782)
                (transaction_id=92274689)
                (type='menu_item')
                (argument_count=12)
                (arg_types=[
                    'int32', 'int32', 'int32', 'string', 'int32', 'string',
                    'int32', 'int32', 'int32', 'int32', 'int32', 'int32',
                ])
                (args=[
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
                ])
             )
        )

    def test_building_root_menu_request_menu_item_album_part(self):
        message = DBMessage.parse(bytes([
            0x11, 0x87, 0x23, 0x49, 0xae, 0x11, 0x05, 0x80, 0x00, 0x01, 0x10,
            0x41, 0x01, 0x0f, 0x0c, 0x14, 0x00, 0x00, 0x00, 0x0c, 0x06, 0x06,
            0x06, 0x02, 0x06, 0x02, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x11,
            0x00, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x03, 0x11, 0x00,
            0x00, 0x00, 0x10, 0x26, 0x00, 0x00, 0x00, 0x08, 0xff, 0xfa, 0x00,
            0x41, 0x00, 0x4c, 0x00, 0x42, 0x00, 0x55, 0x00, 0x4d, 0xff, 0xfb,
            0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x02, 0x26, 0x00, 0x00, 0x00,
            0x01, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x82, 0x11, 0x00, 0x00,
            0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00,
            0x00, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00,
        ]))

        self.assertEqual(message.type, 'menu_item')
        self.assertEqual(
            message,
            (Container
                (magic=2267236782)
                (transaction_id=92274689)
                (type='menu_item')
                (argument_count=12)
                (arg_types=[
                    'int32', 'int32', 'int32', 'string', 'int32', 'string',
                    'int32', 'int32', 'int32', 'int32', 'int32', 'int32',
                ])
                (args=[
                    Container(type='int32')(value=0),
                    Container(type='int32')(value=3),
                    Container(type='int32')(value=16),
                    Container(type='string')(value='\ufffaALBUM\ufffb'),
                    Container(type='int32')(value=2),
                    Container(type='string')(value=''),
                    Container(type='int32')(value=130),
                    Container(type='int32')(value=0),
                    Container(type='int32')(value=0),
                    Container(type='int32')(value=0),
                    Container(type='int32')(value=0),
                    Container(type='int32')(value=0),
                ])
             )
        )

    def test_parsing_render_title(self):
        messages = ManyDBMessages.parse(bytes([
            0x11, 0x87, 0x23, 0x49, 0xae, 0x11, 0x05, 0x80,
            0x00, 0x17, 0x10, 0x40, 0x01, 0x0f, 0x02, 0x14,
            0x00, 0x00, 0x00, 0x0c, 0x06, 0x06, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x00, 0x01, 0x11, 0x00, 0x00,
            0x00, 0x00, 0x11, 0x87, 0x23, 0x49, 0xae, 0x11,
            0x05, 0x80, 0x00, 0x17, 0x10, 0x41, 0x01, 0x0f,
            0x0c, 0x14, 0x00, 0x00, 0x00, 0x0c, 0x06, 0x06,
            0x06, 0x02, 0x06, 0x02, 0x06, 0x06, 0x06, 0x06,
            0x06, 0x06, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11,
            0x00, 0x00, 0x00, 0x05, 0x11, 0x00, 0x00, 0x00,
            0x1a, 0x26, 0x00, 0x00, 0x00, 0x0d, 0x00, 0x44,
            0x00, 0x65, 0x00, 0x6d, 0x00, 0x6f, 0x00, 0x20,
            0x00, 0x54, 0x00, 0x72, 0x00, 0x61, 0x00, 0x63,
            0x00, 0x6b, 0x00, 0x20, 0x00, 0x31, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x00, 0x02, 0x26, 0x00, 0x00,
            0x00, 0x01, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00,
            0x04, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00,
            0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x01, 0x00, 0x11, 0x00, 0x00,
            0x00, 0x00, 0x11, 0x87, 0x23, 0x49, 0xae, 0x11,
            0x05, 0x80, 0x00, 0x17, 0x10, 0x41, 0x01, 0x0f,
            0x0c, 0x14, 0x00, 0x00, 0x00, 0x0c, 0x06, 0x06,
            0x06, 0x02, 0x06, 0x02, 0x06, 0x06, 0x06, 0x06,
            0x06, 0x06, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11,
            0x00, 0x00, 0x00, 0x06, 0x11, 0x00, 0x00, 0x00,
            0x1a, 0x26, 0x00, 0x00, 0x00, 0x0d, 0x00, 0x44,
            0x00, 0x65, 0x00, 0x6d, 0x00, 0x6f, 0x00, 0x20,
            0x00, 0x54, 0x00, 0x72, 0x00, 0x61, 0x00, 0x63,
            0x00, 0x6b, 0x00, 0x20, 0x00, 0x32, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x00, 0x02, 0x26, 0x00, 0x00,
            0x00, 0x01, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00,
            0x04, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00,
            0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x01, 0x00, 0x11, 0x00, 0x00,
            0x00, 0x00, 0x11, 0x87, 0x23, 0x49, 0xae, 0x11,
            0x05, 0x80, 0x00, 0x17, 0x10, 0x42, 0x01, 0x0f,
            0x00, 0x14, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00
        ]))

    def test_parsing_render_artist(self):
        messages = ManyDBMessages.parse(bytes([
            0x11, 0x87, 0x23, 0x49, 0xae, 0x11, 0x05, 0x80,
            0x00, 0x17, 0x10, 0x40, 0x01, 0x0f, 0x02, 0x14,
            0x00, 0x00, 0x00, 0x0c, 0x06, 0x06, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x00, 0x01, 0x11, 0x00, 0x00,
            0x00, 0x00, 0x11, 0x87, 0x23, 0x49, 0xae, 0x11,
            0x05, 0x80, 0x00, 0x17, 0x10, 0x41, 0x01, 0x0f,
            0x0c, 0x14, 0x00, 0x00, 0x00, 0x0c, 0x06, 0x06,
            0x06, 0x02, 0x06, 0x02, 0x06, 0x06, 0x06, 0x06,
            0x06, 0x06, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11,
            0x00, 0x00, 0x00, 0x05, 0x11, 0x00, 0x00, 0x00,
            0x1a, 0x26, 0x00, 0x00, 0x00, 0x0d, 0x00, 0x44,
            0x00, 0x65, 0x00, 0x6d, 0x00, 0x6f, 0x00, 0x20,
            0x00, 0x54, 0x00, 0x72, 0x00, 0x61, 0x00, 0x63,
            0x00, 0x6b, 0x00, 0x20, 0x00, 0x31, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x00, 0x02, 0x26, 0x00, 0x00,
            0x00, 0x01, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00,
            0x04, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00,
            0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x01, 0x00, 0x11, 0x00, 0x00,
            0x00, 0x00, 0x11, 0x87, 0x23, 0x49, 0xae, 0x11,
            0x05, 0x80, 0x00, 0x17, 0x10, 0x41, 0x01, 0x0f,
            0x0c, 0x14, 0x00, 0x00, 0x00, 0x0c, 0x06, 0x06,
            0x06, 0x02, 0x06, 0x02, 0x06, 0x06, 0x06, 0x06,
            0x06, 0x06, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11,
            0x00, 0x00, 0x00, 0x06, 0x11, 0x00, 0x00, 0x00,
            0x1a, 0x26, 0x00, 0x00, 0x00, 0x0d, 0x00, 0x44,
            0x00, 0x65, 0x00, 0x6d, 0x00, 0x6f, 0x00, 0x20,
            0x00, 0x54, 0x00, 0x72, 0x00, 0x61, 0x00, 0x63,
            0x00, 0x6b, 0x00, 0x20, 0x00, 0x32, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x00, 0x02, 0x26, 0x00, 0x00,
            0x00, 0x01, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00,
            0x04, 0x11, 0x00, 0x00, 0x00, 0x00, 0x11, 0x00,
            0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x00,
            0x11, 0x00, 0x00, 0x01, 0x00, 0x11, 0x00, 0x00,
            0x00, 0x00, 0x11, 0x87, 0x23, 0x49, 0xae, 0x11,
            0x05, 0x80, 0x00, 0x17, 0x10, 0x42, 0x01, 0x0f,
            0x00, 0x14, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00
        ]))

    def test_parsing_complete_render_response(self):
        messages = ManyDBMessages.parse(fixtures.root_menu_render_response)

        self.assertEqual(messages,
            [
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_header')
                    (argument_count=2)
                    (arg_types=['int32', 'int32'])
                    (args=[
                        Container(type='int32')(value=1),
                        Container(type='int32')(value=0),
                    ]),
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_item')
                    (argument_count=12)
                    (arg_types=['int32', 'int32', 'int32', 'string', 'int32', 'string', 'int32', 'int32', 'int32', 'int32', 'int32', 'int32'])
                    (args=[
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=2),
                        Container(type='int32')(value=18),
                        Container(type='string')(value='\ufffaARTIST\ufffb'),
                        Container(type='int32')(value=2),
                        Container(type='string')(value=''),
                        Container(type='int32')(value=129),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0)
                    ]),
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_item')
                    (argument_count=12)
                    (arg_types=['int32', 'int32', 'int32', 'string', 'int32', 'string', 'int32', 'int32', 'int32', 'int32', 'int32', 'int32'])
                    (args=[
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=3),
                        Container(type='int32')(value=16),
                        Container(type='string')(value='\ufffaALBUM\ufffb'),
                        Container(type='int32')(value=2),
                        Container(type='string')(value=''),
                        Container(type='int32')(value=130),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0)
                    ]),
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_item')
                    (argument_count=12)
                    (arg_types=['int32', 'int32', 'int32', 'string', 'int32', 'string', 'int32', 'int32', 'int32', 'int32', 'int32', 'int32'])
                    (args=[
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=4),
                        Container(type='int32')(value=16),
                        Container(type='string')(value='\ufffaTRACK\ufffb'),
                        Container(type='int32')(value=2),
                        Container(type='string')(value=''),
                        Container(type='int32')(value=131),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0)
                    ]),
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_item')
                    (argument_count=12)
                    (arg_types=['int32', 'int32', 'int32', 'string', 'int32', 'string', 'int32', 'int32', 'int32', 'int32', 'int32', 'int32'])
                    (args=[
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=12),
                        Container(type='int32')(value=12),
                        Container(type='string')(value='\ufffaKEY\ufffb'),
                        Container(type='int32')(value=2),
                        Container(type='string')(value=''),
                        Container(type='int32')(value=139),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0)
                    ]),
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_item')
                    (argument_count=12)
                    (arg_types=['int32', 'int32', 'int32', 'string', 'int32', 'string', 'int32', 'int32', 'int32', 'int32', 'int32', 'int32'])
                    (args=[
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=5),
                        Container(type='int32')(value=22),
                        Container(type='string')(value='\ufffaPLAYLIST\ufffb'),
                        Container(type='int32')(value=2),
                        Container(type='string')(value=''),
                        Container(type='int32')(value=132),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0)
                    ]),
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_item')
                    (argument_count=12)
                    (arg_types=['int32', 'int32', 'int32', 'string', 'int32', 'string', 'int32', 'int32', 'int32', 'int32', 'int32', 'int32'])
                    (args=[
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=22),
                        Container(type='int32')(value=20),
                        Container(type='string')(value='\ufffaHISTORY\ufffb'),
                        Container(type='int32')(value=2),
                        Container(type='string')(value=''),
                        Container(type='int32')(value=149),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0)
                    ]),
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_item')
                    (argument_count=12)
                    (arg_types=['int32', 'int32', 'int32', 'string', 'int32', 'string', 'int32', 'int32', 'int32', 'int32', 'int32', 'int32'])
                    (args=[
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=18),
                        Container(type='int32')(value=18),
                        Container(type='string')(value='\ufffaSEARCH\ufffb'),
                        Container(type='int32')(value=2),
                        Container(type='string')(value=''),
                        Container(type='int32')(value=145),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                        Container(type='int32')(value=0),
                    ]),
                Container
                    (magic=2267236782)
                    (transaction_id=92274703)
                    (type='menu_footer')
                    (argument_count=0)
                    (arg_types=[])
                    (args=[])])

    def test_metadata_request(self):
        messages = ManyDBMessages.parse(fixtures.metadata_render_response)

        pa.pprint(messages)
