import unittest
import scheduler


class MyTestCase(unittest.TestCase):

    def test_get_quiet_times(self):
        quiet_times = scheduler.get_quiet_times('../data/quiet_times.json')

        self.assertTrue(len(quiet_times) > 0)
        self.assertEqual(17, quiet_times[1].start.hour)
        self.assertEqual(27, quiet_times[1].start.minute)
        self.assertEqual(0, quiet_times[1].start.second)
        self.assertEqual(17, quiet_times[1].end.hour)
        self.assertEqual(31, quiet_times[1].end.minute)
        self.assertEqual(20, quiet_times[1].end.second)


if __name__ == '__main__':
    unittest.main()
