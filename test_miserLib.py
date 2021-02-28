import unittest
from miserLib import Miser, IUserInterface


class TestUI(IUserInterface):
    def mp(self, *args, sep=' ', end='\n'):
        pass

    def wrap_print(self, long_string):
        pass

    def clear_screen(self):
        pass

    def get_input(self):
        pass

    def wait_for_keypress(self):
        pass

    def delay(self):
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
        miser.handle_command(["drop", "mat"])
        self.assertEqual(miser.get_item_location(mat_index), 0)
        miser.handle_command(["get", "mat"])
        miser.handle_command(["get", "mat"])
        self.assertEqual(miser.get_item_location(mat_index), -1)
        valve_index = 7
        miser.current_position = 26
        miser.handle_command(["get", "valve"])
        self.assertEqual(miser.subjects[valve_index].item_id, -1)
        treasure_count = miser.gathered_treasures
        miser.current_position = 45
        miser.handle_command(["get", "leaf"])
        self.assertEqual(miser.gathered_treasures, treasure_count + 1)
        miser.handle_command(["drop", "leaf"])
        self.assertEqual(miser.gathered_treasures, treasure_count + 1)
        penny_index = 19
        miser.current_position = 28
        miser.handle_command(["get", "penny"])
        self.assertEqual(miser.get_item_location(penny_index), -1)
        miser.current_position = 19
        miser.handle_command(["drop", "penny"])
        self.assertEqual(miser.rooms[21].moves[2], 22)
        self.assertEqual(miser.items[12].location, -2)
        cross_index = 20
        miser.current_position = 23
        miser.handle_command(["get", "cross"])
        self.assertEqual(miser.get_item_location(cross_index), -1)
        miser.current_position = 22
        miser.flags["organ_playing"] = False
        miser.handle_command(["drop", "cross"])
        self.assertEqual(miser.flags["organ_playing"], True)

    def test_exposing_key_works(self):
        ui = TestUI()
        miser = Miser(ui)
        key_index = 6
        self.assertEqual(miser.get_item_location(key_index), -2)
        miser.handle_command(["move", "mat"])
        self.assertEqual(miser.get_item_location(key_index), 0)

    def test_handle_command(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["backflip"])
        self.assertEqual(miser.current_position, 0)
        miser.handle_command(["get", "sword"])
        self.assertEqual(miser.current_position, 0)
        miser.handle_command(["get", "donut"])
        self.assertEqual(miser.current_position, 0)

    def test_inventory_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # works for empty
        miser.handle_command(["inventory"])
        # works for stuff
        miser.handle_command(["move", "mat"])
        miser.handle_command(["get", "key"])
        miser.handle_command(["inventory"])
        self.assertEqual(miser.current_position, 0)

    def test_say_command(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["say", "xyzzy"])
        miser.handle_command(["say", "sword"])
        self.assertEqual(miser.current_position, 0)
        miser.current_position = 0
        miser.handle_command(["say", "victory"])
        self.assertEqual(miser.flags["portal_visible"], False)
        miser.current_position = 8
        miser.handle_command(["say", "victory"])
        self.assertEqual(miser.flags["portal_visible"], True)
        miser.current_position = 0
        miser.handle_command(["say", "ritnew"])
        self.assertEqual(miser.flags["snake_charmed"], False)
        miser.current_position = 4
        miser.handle_command(["say", "ritnew"])
        self.assertEqual(miser.flags["snake_charmed"], True)

    def test_unlock_front_door(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["unlock", "door"])
        self.assertEqual(miser.flags["dungeon_unlocked"], False)
        miser.handle_command(["move", "mat"])
        miser.handle_command(["get", "key"])
        miser.handle_command(["unlock", "door"])
        self.assertEqual(miser.flags["dungeon_unlocked"], True)
        miser.handle_command(["unlock", "door"])
        self.assertEqual(miser.flags["dungeon_unlocked"], True)

    def test_north(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["n"])
        self.assertEqual(miser.current_position, 0)
        miser.flags["dungeon_unlocked"] = True
        miser.handle_command(["n"])
        self.assertEqual(miser.current_position, 1)
        miser.current_position = 12
        miser.handle_command(["n"])
        self.assertEqual(miser.current_position, 12)

    def test_south(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["s"])
        self.assertEqual(miser.current_position, 0)
        miser.current_position = 2
        miser.handle_command(["s"])
        self.assertEqual(miser.current_position, 1)
        miser.current_position = 10
        miser.flags["fire_burning"] = True
        miser.handle_command(["s"])
        self.assertEqual(miser.flags["game_over"], True)

    def test_east(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["e"])
        self.assertEqual(miser.current_position, 0)
        miser.current_position = 12
        miser.handle_command(["e"])
        self.assertEqual(miser.current_position, 1)
        miser.current_position = 4
        miser.flags["snake_charmed"] = False
        miser.flags["angry_snake"] = False
        miser.handle_command(["e"])
        self.assertEqual(miser.current_position, 4)
        self.assertEqual(miser.flags["angry_snake"], True)
        miser.current_position = 4
        miser.flags["snake_charmed"] = False
        miser.flags["angry_snake"] = True
        miser.handle_command(["e"])
        self.assertEqual(miser.flags["game_over"], True)

    def test_west(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["w"])
        self.assertEqual(miser.current_position, 0)
        miser.current_position = 1
        miser.handle_command(["w"])
        self.assertEqual(miser.current_position, 12)

    def test_turn_command(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["turn", "mat"])
        self.assertEqual(miser.current_position, 0)
        miser.handle_command(["turn", "valve"])
        self.assertEqual(miser.current_position, 0)
        miser.current_position = 26
        miser.flags["pool_flooded"] = True
        miser.items[7].location = -3
        miser.handle_command(["turn", "valve"])
        self.assertEqual(miser.flags["pool_flooded"], False)
        self.assertEqual(miser.items[7].location, 25)
        miser.flags["pool_flooded"] = False
        miser.items[7].location = 25
        miser.handle_command(["turn", "valve"])
        self.assertEqual(miser.flags["pool_flooded"], True)
        self.assertEqual(miser.items[7].location, -3)

    def test_final_stats(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.final_stats()
        self.assertEqual(miser.gathered_treasures, 0)
        miser.flags["escaped"] = True
        miser.final_stats()
        self.assertEqual(miser.gathered_treasures, 1)
        miser.gathered_treasures = 1
        miser.flags["escaped"] = True
        miser.final_stats()
        self.assertEqual(miser.gathered_treasures, 2)
        miser.gathered_treasures = 2
        miser.flags["escaped"] = True
        miser.final_stats()
        self.assertEqual(miser.gathered_treasures, 3)
        miser.gathered_treasures = 3
        miser.flags["escaped"] = True
        miser.final_stats()
        self.assertEqual(miser.gathered_treasures, 4)
        miser.gathered_treasures = 4
        miser.flags["escaped"] = True
        miser.final_stats()
        self.assertEqual(miser.gathered_treasures, 5)
        miser.gathered_treasures = 5
        miser.flags["escaped"] = True
        miser.final_stats()
        self.assertEqual(miser.gathered_treasures, 6)

    def test_move_things(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.current_position = 5
        miser.handle_command(["move", "cabinet"])
        self.assertEqual(miser.flags["found_vault"], True)
        miser.current_position = 21
        miser.handle_command(["move", "organ"])
        self.assertEqual(miser.current_position, 21)
        miser.handle_command(["move", "mat"])
        self.assertEqual(miser.current_position, 21)
        miser.current_position = 6
        miser.handle_command(["move", "rug"])
        self.assertEqual(miser.items[16].location, 6)
        miser.current_position = 13
        miser.handle_command(["move", "sword"])
        self.assertEqual(miser.current_position, 13)

    def test_pour_things(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["pour", "mat"])
        self.assertEqual(miser.current_position, 0)
        miser.current_position = 26
        miser.handle_command(["pour", "bucket"])
        self.assertEqual(miser.current_position, 26)
        miser.handle_command(["get", "bucket"])
        miser.flags["bucket_full"] = True
        miser.handle_command(["pour", "bucket"])
        self.assertEqual(miser.current_position, 26)
        self.assertEqual(miser.flags["bucket_full"], False)
        miser.current_position = 10
        miser.flags["fire_burning"] = True
        miser.flags["bucket_full"] = True
        miser.handle_command(["pour", "bucket"])
        self.assertEqual(miser.current_position, 10)
        self.assertEqual(miser.flags["fire_burning"], False)
        self.assertEqual(miser.flags["bucket_full"], False)

    def test_fill_things(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["fill", "pool"])
        self.assertEqual(miser.current_position, 0)
        miser.handle_command(["fill", "key"])
        self.assertEqual(miser.current_position, 0)
        miser.handle_command(["fill", "mat"])
        self.assertEqual(miser.current_position, 0)
        miser.current_position = 26
        miser.handle_command(["get", "bucket"])
        self.assertEqual(miser.flags["bucket_full"], False)
        miser.handle_command(["fill", "bucket"])
        self.assertEqual(miser.current_position, 26)
        self.assertEqual(miser.flags["bucket_full"], False)
        miser.flags["bucket_full"] = True
        miser.handle_command(["fill", "bucket"])
        self.assertEqual(miser.current_position, 26)
        self.assertEqual(miser.flags["bucket_full"], True)
        miser.current_position = 25
        miser.flags["pool_flooded"] = True
        miser.flags["bucket_full"] = False
        miser.handle_command(["fill", "bucket"])
        self.assertEqual(miser.current_position, 25)
        self.assertEqual(miser.flags["bucket_full"], False)
        miser.current_position = 23
        miser.flags["bucket_full"] = False
        miser.handle_command(["fill", "bucket"])
        self.assertEqual(miser.current_position, 23)
        self.assertEqual(miser.flags["bucket_full"], True)

def suite():
    """Test Suite"""
    my_suite = unittest.TestSuite()
    my_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(MiserTest)
    )
    return my_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
