import unittest
from miserLib import Miser


class MiserTest(unittest.TestCase):
    def test_can_create(self):
        miser = Miser()
        self.assertIsInstance(miser, Miser)
        self.assertEqual(miser.current_position, 0)

    def test_get_inside(self):
        miser = Miser()
        miser.handle_command(["get", "mat"])
        miser.handle_command(["get", "key"])
        miser.handle_command(["unlock", "door"])
        miser.handle_command(["north"])
        self.assertEqual(miser.current_position, 1)


def suite():
    """Test Suite"""
    my_suite = unittest.TestSuite()
    my_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(MiserTest)
    )
    return my_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
