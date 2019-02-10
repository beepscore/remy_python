import unittest
import ir_remote


class MyTestCase(unittest.TestCase):

    def test_irsend(self):
        self.assertEqual('irsend', ir_remote.IRSEND)

    def test_send_once(self):
        self.assertEqual('SEND_ONCE', ir_remote.SEND_ONCE)

    def test_polk(self):
        self.assertEqual('polk', ir_remote.POLK_IR_REMOTE)


if __name__ == '__main__':
    unittest.main()
