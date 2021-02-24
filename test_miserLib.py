import unittest
from miserLib import Miser


class MiserTest(unittest.TestCase):
    def test_can_create(self):
        miser = Miser()
        self.assertIsInstance(miser, Miser)
        self.assertEqual(miser.current_position, 0)


def suite():
    """Test Suite"""
    my_suite = unittest.TestSuite()
    my_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(MiserTest)
    )
    return my_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
