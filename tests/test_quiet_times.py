import unittest
import quiet_times


class MyTestCase(unittest.TestCase):

    def test_get_quiet_times(self):
        times = quiet_times.get_quiet_times('../data/quiet_times.json')

        self.assertTrue(len(times) > 0)
        self.assertEqual(17, times[1].start.hour)
        self.assertEqual(27, times[1].start.minute)
        self.assertEqual(0, times[1].start.second)

        self.assertEqual(240, times[1].duration.seconds)
        self.assertEqual(180, times[2].duration.seconds)


if __name__ == '__main__':
    unittest.main()
