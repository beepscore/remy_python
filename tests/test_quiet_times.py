import unittest
import quiet_times


class TestQuietTimes(unittest.TestCase):

    def test_get_quiet_times(self):
        times = quiet_times.get_quiet_times('../data/quiet_times.json')

        self.assertTrue(len(times) > 0)
        self.assertEqual(17, times[1].start.hour)
        self.assertEqual(27, times[1].start.minute)
        self.assertEqual(0, times[1].start.second)
        self.assertEqual(17, times[1].end.hour)
        self.assertEqual(31, times[1].end.minute)
        self.assertEqual(20, times[1].end.second)


if __name__ == '__main__':
    unittest.main()
