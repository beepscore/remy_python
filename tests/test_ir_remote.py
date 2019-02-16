import unittest
import ir_remote
from remote_command import RemoteCommand


class MyTestCase(unittest.TestCase):

    def test_irsend(self):
        self.assertEqual('irsend', ir_remote.IRSEND)

    def test_send_once(self):
        self.assertEqual('SEND_ONCE', ir_remote.SEND_ONCE)

    def test_polk(self):
        self.assertEqual('polk', ir_remote.POLK_IR_REMOTE)

    def test_ir_command(self):
        self.assertEqual('KEY_MUTE', ir_remote.ir_command(RemoteCommand.MUTE))
        self.assertEqual('KEY_VOLUMEDOWN',
                         ir_remote.ir_command(RemoteCommand.VOLUME_DECREASE))
        self.assertEqual('KEY_VOLUMEUP',
                         ir_remote.ir_command(RemoteCommand.VOLUME_INCREASE))

    def test_ir_command_none(self):
        self.assertIsNone(ir_remote.ir_command('garbage'))


if __name__ == '__main__':
    unittest.main()
