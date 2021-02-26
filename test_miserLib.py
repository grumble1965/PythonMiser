import unittest
from miserLib import Miser, IUserInterface


class TestUI(IUserInterface):
    @staticmethod
    def mp(*args, sep=' ', end='\n'):
        pass


class MiserTest(unittest.TestCase):
    def test_can_create(self):
        ui = TestUI()
        miser = Miser(ui)
        self.assertIsInstance(miser, Miser)
        self.assertEqual(miser.current_position, 0)

    def test_get_inside(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["get", "mat"])
        miser.handle_command(["get", "key"])
        miser.handle_command(["unlock", "door"])
        miser.handle_command(["north"])
        self.assertEqual(miser.current_position, 1)

    def test_get_and_drop_work(self):
        ui = TestUI()
        miser = Miser(ui)
        mat_index = 2
        self.assertEqual(miser.get_item_location(mat_index), 0)
        miser.handle_command(["get", "mat"])
        self.assertEqual(miser.get_item_location(mat_index), -1)
        miser.handle_command(["drop", "mat"])
        self.assertEqual(miser.get_item_location(mat_index), 0)

    def test_exposing_key_works(self):
        ui = TestUI()
        miser = Miser(ui)
        key_index = 6
        self.assertEqual(miser.get_item_location(key_index), -2)
        miser.handle_command(["get", "mat"])
        self.assertEqual(miser.get_item_location(key_index), 0)


def suite():
    """Test Suite"""
    my_suite = unittest.TestSuite()
    my_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(MiserTest)
    )
    return my_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
