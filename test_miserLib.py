import unittest
from miserLib import Miser, IUserInterface, Items, Rooms, Subjects, welcome_banner


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
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)

    def test_get_inside(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["get", "mat"])
        miser.handle_command(["get", "key"])
        miser.handle_command(["unlock", "door"])
        miser.handle_command(["north"])
        self.assertEqual(miser.current_position, Rooms.FOYER)

    def test_get_and_drop_work(self):
        ui = TestUI()
        miser = Miser(ui)
        self.assertEqual(miser.get_item_location(Subjects.MAT), Rooms.FRONT_PORCH)
        miser.handle_command(["get", "mat"])
        self.assertEqual(miser.get_item_location(Subjects.MAT), -1)
        miser.handle_command(["drop", "mat"])
        self.assertEqual(miser.get_item_location(Subjects.MAT), Rooms.FRONT_PORCH)
        miser.handle_command(["drop", "mat"])
        self.assertEqual(miser.get_item_location(Subjects.MAT), Rooms.FRONT_PORCH)
        miser.handle_command(["get", "mat"])
        miser.handle_command(["get", "mat"])
        self.assertEqual(miser.get_item_location(Subjects.MAT), -1)
        miser.current_position = Rooms.PUMP_HOUSE
        miser.handle_command(["get", "valve"])
        self.assertEqual(miser.subjects[Subjects.VALVE].item_id, Items.UNMOVEABLE)
        treasure_count = miser.gathered_treasures
        miser.current_position = Rooms.HEDGE_MAZE5
        miser.handle_command(["get", "leaf"])
        self.assertEqual(miser.gathered_treasures, treasure_count + 1)
        miser.handle_command(["drop", "leaf"])
        self.assertEqual(miser.gathered_treasures, treasure_count + 1)
        miser.current_position = Rooms.WEST_BEDROOM
        miser.handle_command(["get", "penny"])
        self.assertEqual(miser.get_item_location(Subjects.PENNY), -1)
        miser.current_position = Rooms.PORTICO
        miser.handle_command(["drop", "penny"])
        self.assertEqual(miser.rooms[Rooms.BALLROOM].moves[2], Rooms.CHAPEL)
        self.assertEqual(miser.items[Items.PENNY].location, -2)
        miser.current_position = Rooms.BACK_YARD
        miser.handle_command(["get", "cross"])
        self.assertEqual(miser.get_item_location(Subjects.CROSS), -1)
        miser.current_position = Rooms.CHAPEL
        miser.flags["organ_playing"] = False
        miser.handle_command(["drop", "cross"])
        self.assertEqual(miser.flags["organ_playing"], True)

    def test_exposing_key_works(self):
        ui = TestUI()
        miser = Miser(ui)
        self.assertEqual(miser.get_item_location(Subjects.KEY), -2)
        miser.handle_command(["move", "mat"])
        self.assertEqual(miser.get_item_location(Subjects.KEY), Rooms.FRONT_PORCH)

    def test_handle_command(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["backflip"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.handle_command(["get", "sword"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.handle_command(["get", "donut"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)

    def test_inventory_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # works for empty
        miser.handle_command(["inventory"])
        # works for stuff
        miser.handle_command(["move", "mat"])
        miser.handle_command(["get", "key"])
        miser.handle_command(["inventory"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # full bucket works
        miser.current_position = Rooms.PUMP_HOUSE
        miser.handle_command(["get", "bucket"])
        miser.flags["bucket_full"] = True
        miser.handle_command(["inventory"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        # broken parachute works
        miser.current_position = Rooms.CLOSET
        miser.handle_command(["get", "parachute"])
        miser.handle_command(["inventory"])
        self.assertEqual(miser.current_position, Rooms.CLOSET)

    def test_say_command(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["say", "xyzzy"])
        miser.handle_command(["say", "sword"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["say", "victory"])
        self.assertEqual(miser.flags["portal_visible"], False)
        miser.current_position = Rooms.TROPHY_ROOM
        miser.handle_command(["say", "victory"])
        self.assertEqual(miser.flags["portal_visible"], True)
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["say", "ritnew"])
        self.assertEqual(miser.flags["snake_charmed"], False)
        miser.current_position = Rooms.CONSERVATORY
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
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.flags["dungeon_unlocked"] = True
        miser.handle_command(["n"])
        self.assertEqual(miser.current_position, Rooms.FOYER)
        miser.current_position = Rooms.DINING_ROOM
        miser.handle_command(["n"])
        self.assertEqual(miser.current_position, Rooms.DINING_ROOM)

    def test_south(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["s"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.GREAT_HALL
        miser.handle_command(["s"])
        self.assertEqual(miser.current_position, Rooms.FOYER)
        miser.current_position = Rooms.BLUE_ROOM
        miser.flags["fire_burning"] = True
        miser.handle_command(["s"])
        self.assertEqual(miser.flags["game_over"], True)

    def test_east(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["e"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.DINING_ROOM
        miser.handle_command(["e"])
        self.assertEqual(miser.current_position, Rooms.FOYER)
        miser.current_position = Rooms.CONSERVATORY
        miser.flags["snake_charmed"] = False
        miser.flags["angry_snake"] = False
        miser.handle_command(["e"])
        self.assertEqual(miser.current_position, Rooms.CONSERVATORY)
        self.assertEqual(miser.flags["angry_snake"], True)
        miser.current_position = Rooms.CONSERVATORY
        miser.flags["snake_charmed"] = False
        miser.flags["angry_snake"] = True
        miser.handle_command(["e"])
        self.assertEqual(miser.flags["game_over"], True)

    def test_west(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["w"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.FOYER
        miser.handle_command(["w"])
        self.assertEqual(miser.current_position, Rooms.DINING_ROOM)

    def test_turn_command(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["turn", "mat"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.handle_command(["turn", "valve"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.PUMP_HOUSE
        miser.flags["pool_flooded"] = True
        miser.items[Items.RING].location = -3
        miser.handle_command(["turn", "valve"])
        self.assertEqual(miser.flags["pool_flooded"], False)
        self.assertEqual(miser.items[Items.RING].location, Rooms.POOL_AREA)
        miser.flags["pool_flooded"] = False
        miser.items[Items.RING].location = Rooms.POOL_AREA
        miser.handle_command(["turn", "valve"])
        self.assertEqual(miser.flags["pool_flooded"], True)
        self.assertEqual(miser.items[Items.RING].location, -3)

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
        miser.current_position = Rooms.REDWALL_ROOM
        miser.handle_command(["move", "cabinet"])
        self.assertEqual(miser.flags["found_vault"], True)
        miser.current_position = Rooms.BALLROOM
        miser.handle_command(["move", "organ"])
        self.assertEqual(miser.current_position, Rooms.BALLROOM)
        miser.handle_command(["move", "mat"])
        self.assertEqual(miser.current_position, Rooms.BALLROOM)
        miser.current_position = Rooms.PARLOR
        miser.handle_command(["move", "rug"])
        self.assertEqual(miser.items[Items.TRAPDOOR].location, Rooms.PARLOR)
        miser.current_position = Rooms.CHINESE_ROOM
        miser.handle_command(["move", "sword"])
        self.assertEqual(miser.current_position, Rooms.CHINESE_ROOM)

    def test_pour_things(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["pour", "mat"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.handle_command(["pour", "bucket"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.PUMP_HOUSE
        miser.handle_command(["pour", "bucket"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        miser.handle_command(["get", "bucket"])
        miser.flags["bucket_full"] = True
        miser.handle_command(["pour", "bucket"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        self.assertEqual(miser.flags["bucket_full"], False)
        miser.current_position = Rooms.BLUE_ROOM
        miser.flags["fire_burning"] = True
        miser.flags["bucket_full"] = True
        miser.handle_command(["pour", "bucket"])
        self.assertEqual(miser.current_position, Rooms.BLUE_ROOM)
        self.assertEqual(miser.flags["fire_burning"], False)
        self.assertEqual(miser.flags["bucket_full"], False)
        # pour into wishing well
        miser.flags["bucket_full"] = True
        miser.current_position = Rooms.PORTICO
        miser.handle_command(["pour", "bucket"])
        self.assertEqual(miser.current_position, Rooms.PORTICO)

    def test_fill_things(self):
        ui = TestUI()
        miser = Miser(ui)
        miser.handle_command(["fill", "pool"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.handle_command(["fill", "key"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.handle_command(["fill", "mat"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.PUMP_HOUSE
        miser.handle_command(["get", "bucket"])
        self.assertEqual(miser.flags["bucket_full"], False)
        miser.handle_command(["fill", "bucket"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        self.assertEqual(miser.flags["bucket_full"], False)
        miser.flags["bucket_full"] = True
        miser.handle_command(["fill", "bucket"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        self.assertEqual(miser.flags["bucket_full"], True)
        miser.current_position = Rooms.POOL_AREA
        miser.flags["pool_flooded"] = True
        miser.flags["bucket_full"] = False
        miser.handle_command(["fill", "bucket"])
        self.assertEqual(miser.current_position, Rooms.POOL_AREA)
        self.assertEqual(miser.flags["bucket_full"], False)
        miser.current_position = Rooms.BACK_YARD
        miser.flags["bucket_full"] = False
        miser.handle_command(["fill", "bucket"])
        self.assertEqual(miser.current_position, Rooms.BACK_YARD)
        self.assertEqual(miser.flags["bucket_full"], True)

    def test_read_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # read something not present
        miser.handle_command(["read", "ring"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # read something unmovable
        miser.handle_command(["read", "door"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # read something without writing
        miser.handle_command(["read", "mat"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # read a book
        miser.current_position = Rooms.LIBRARY
        miser.handle_command(["read", "book"])
        self.assertEqual(miser.current_position, Rooms.LIBRARY)
        # read a paper
        miser.current_position = Rooms.MASTER_BEDROOM
        miser.handle_command(["read", "paper"])
        self.assertEqual(miser.current_position, Rooms.MASTER_BEDROOM)

    def test_look_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # carrying full bucket
        miser.current_position = Rooms.PUMP_HOUSE
        miser.flags["bucket_full"] = True
        miser.handle_command(["look"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        # pool flooded and empty
        miser.current_position = Rooms.POOL_AREA
        miser.flags["pool_flooded"] = False
        miser.handle_command(["look"])
        miser.flags["pool_flooded"] = True
        miser.handle_command(["look"])
        self.assertEqual(miser.current_position, Rooms.POOL_AREA)
        # fire in Blue room
        miser.current_position = Rooms.BLUE_ROOM
        miser.flags["fire_burning"] = True
        miser.handle_command(["look"])
        self.assertEqual(miser.current_position, Rooms.BLUE_ROOM)
        # pantry
        miser.current_position = Rooms.PANTRY
        miser.handle_command(["look"])
        self.assertEqual(miser.current_position, Rooms.PANTRY)
        # back yard
        miser.current_position = Rooms.BACK_YARD
        miser.handle_command(["look"])
        self.assertEqual(miser.current_position, Rooms.BACK_YARD)
        # open vault in Red Wall room
        miser.current_position = Rooms.REDWALL_ROOM
        miser.flags["vault_open"] = True
        miser.handle_command(["look"])
        self.assertEqual(miser.current_position, Rooms.REDWALL_ROOM)

    def test_fix_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # fix valve
        miser.current_position = Rooms.PUMP_HOUSE
        miser.handle_command(["fix", "valve"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        # fix not parachute
        miser.handle_command(["fix", "bucket"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        # fix parachute when not here
        miser.handle_command(["fix", "parachute"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        # fix parachute without ripcord
        miser.current_position = Rooms.CLOSET
        miser.handle_command(["get", "parachute"])
        miser.handle_command(["fix", "parachute"])
        self.assertEqual(miser.current_position, Rooms.CLOSET)
        # fix parachute
        miser.current_position = Rooms.BALLROOM
        miser.flags["organ_playing"] = True
        miser.handle_command(["open", "organ"])
        self.assertEqual(miser.get_item_location(Subjects.RIPCORD), Rooms.BALLROOM)
        miser.handle_command(["get", "ripcord"])
        miser.handle_command(["fix", "parachute"])
        self.assertEqual(miser.current_position, Rooms.BALLROOM)
        # fix it again
        miser.handle_command(["fix", "parachute"])
        self.assertEqual(miser.current_position, Rooms.BALLROOM)

    def test_swim_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # can't swim here
        miser.handle_command(["swim"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # swim in wishing well
        miser.current_position = Rooms.PORTICO
        miser.handle_command(["swim"])
        self.assertEqual(miser.current_position, Rooms.PORTICO)
        # swim in mercury pool
        miser.current_position = Rooms.POOL_AREA
        miser.handle_command(["swim"])
        self.assertEqual(miser.current_position, Rooms.POOL_AREA)
        # swim in empty pool
        miser.flags["pool_flooded"] = False
        miser.handle_command(["swim"])
        self.assertEqual(miser.current_position, Rooms.POOL_AREA)

    def test_unlock_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # unhandled object
        miser.handle_command(["unlock", "mat"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # handled object, wrong location
        miser.current_position = Rooms.FOYER
        miser.handle_command(["unlock", "door"])
        self.assertEqual(miser.current_position, Rooms.FOYER)
        # vault not visible
        miser.current_position = Rooms.REDWALL_ROOM
        miser.handle_command(["unlock", "door"])
        self.assertEqual(miser.current_position, Rooms.REDWALL_ROOM)
        # trapdoor has no lock
        miser.current_position = Rooms.PARLOR
        miser.handle_command(["unlock", "door"])
        self.assertEqual(miser.current_position, Rooms.PARLOR)

    def test_unlock_vault(self):
        ui = TestUI()
        miser = Miser(ui)
        # vault is hidden
        miser.current_position = Rooms.REDWALL_ROOM
        miser.handle_command(["unlock", "vault"])
        self.assertEqual(miser.current_position, Rooms.REDWALL_ROOM)
        # vault exposed, no combo
        miser.flags["found_vault"] = True
        miser.handle_command(["unlock", "vault"])
        self.assertEqual(miser.current_position, Rooms.REDWALL_ROOM)
        # vault exposed, known combo
        miser.flags["know_combination"] = True
        miser.handle_command(["unlock", "vault"])
        self.assertEqual(miser.flags["vault_open"], True)
        # vault reopen
        miser.handle_command(["unlock", "vault"])
        self.assertEqual(miser.flags["vault_open"], True)

    def test_go_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # no stairs without sword
        miser.current_position = Rooms.GREAT_HALL
        miser.handle_command(["go", "stairs"])
        self.assertEqual(miser.current_position, Rooms.GREAT_HALL)
        # stairs with sword
        miser.current_position = Rooms.CHINESE_ROOM
        miser.handle_command(["get", "sword"])
        miser.current_position = Rooms.GREAT_HALL
        miser.handle_command(["go", "stairs"])
        self.assertEqual(miser.current_position, Rooms.MIDDLE_WESTERN_HALLWAY)
        # stairs down
        miser.handle_command(["go", "stairs"])
        self.assertEqual(miser.current_position, Rooms.GREAT_HALL)
        # no stairs
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["go", "stairs"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # ladder in wrong place
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["go", "ladder"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # pool in wrong place
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["go", "pool"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # can't go flooded pool
        miser.current_position = Rooms.POOL_AREA
        miser.flags["pool_flooded"] = True
        miser.handle_command(["go", "pool"])
        self.assertEqual(miser.current_position, Rooms.POOL_AREA)
        # can go empty pool
        miser.flags["pool_flooded"] = False
        miser.handle_command(["go", "pool"])
        self.assertEqual(miser.current_position, Rooms.BOTTOM_OF_POOL)
        # can go up ladder
        miser.handle_command(["go", "ladder"])
        self.assertEqual(miser.current_position, Rooms.POOL_AREA)

    def test_jump_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # no place to jump
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["jump"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # jump stairs (first)
        miser.current_position = Rooms.MIDDLE_WESTERN_HALLWAY
        miser.handle_command(["jump"])
        self.assertEqual(miser.current_position, Rooms.GREAT_HALL)
        self.assertTrue(miser.flags["jump_warning"])
        # jump stairs (second) kills you
        miser.current_position = Rooms.MIDDLE_WESTERN_HALLWAY
        miser.handle_command(["jump"])
        self.assertTrue(miser.flags["game_over"])
        # jump front balcony no parachute kills you
        miser = Miser(ui)
        miser.current_position = Rooms.FRONT_BALCONY
        miser.handle_command(["jump"])
        self.assertTrue(miser.flags["game_over"])
        # jump with broken parachute does nothing
        miser = Miser(ui)
        miser.current_position = Rooms.CLOSET
        miser.handle_command(["get", "parachute"])
        miser.current_position = Rooms.FRONT_BALCONY
        miser.handle_command(["jump"])
        self.assertEqual(miser.current_position, Rooms.FRONT_BALCONY)
        # jump rear balcony with good parachute lands in maze
        miser = Miser(ui)
        miser.items[Items.REPAIRED_PARACHUTE].location = -1
        miser.current_position = Rooms.REAR_BALCONY
        miser.handle_command(["jump"])
        self.assertEqual(miser.current_position, Rooms.HEDGE_MAZE0)
        # jump front balcony with good parachute escapes
        miser = Miser(ui)
        miser.items[Items.REPAIRED_PARACHUTE].location = -1
        miser.current_position = Rooms.FRONT_BALCONY
        miser.handle_command(["jump"])
        self.assertTrue(miser.flags["escaped"])

    def test_open_command(self):
        ui = TestUI()
        miser = Miser(ui)
        # can't open missing book
        miser.handle_command(["open", "book"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # can open book if present
        miser.current_position = Rooms.LIBRARY
        miser.handle_command(["open", "book"])
        self.assertEqual(miser.current_position, Rooms.LIBRARY)
        # can open book in inventory
        miser.handle_command(["get", "book"])
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["open", "book"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        # open valve
        miser.current_position = Rooms.PUMP_HOUSE
        miser.handle_command(["open", "valve"])
        self.assertEqual(miser.current_position, Rooms.PUMP_HOUSE)
        # open front door only if unlocked
        miser = Miser(ui)
        miser.handle_command(["open", "door"])
        self.assertFalse(miser.flags["dungeon_unlocked"])
        miser.flags["dungeon_unlocked"] = True
        miser.handle_command(["open", "door"])
        self.assertTrue(miser.flags["dungeon_unlocked"])
        miser.handle_command(["open", "door"])
        self.assertTrue(miser.flags["dungeon_unlocked"])
        # can't open doors just anywhere
        miser.current_position = Rooms.CLOSET
        miser.handle_command(["open", "door"])
        self.assertEqual(miser.current_position, Rooms.CLOSET)
        # opening trapdoor leads to dungeon
        miser.current_position = Rooms.PARLOR
        miser.handle_command(["open", "door"])
        self.assertEqual(miser.current_position, Rooms.DUNGEON)
        # open cabinet needs cabinet
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["open", "cabinet"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.REDWALL_ROOM
        miser.handle_command(["open", "cabinet"])
        self.assertEqual(miser.current_position, Rooms.REDWALL_ROOM)
        # open bag needs bag
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["open", "bag"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.VAULT
        miser.handle_command(["open", "bag"])
        self.assertEqual(miser.current_position, Rooms.VAULT)
        # open vault needs vault
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["open", "vault"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.REDWALL_ROOM
        miser.flags["found_vault"] = True
        miser.flags["vault_open"] = False
        miser.handle_command(["open", "vault"])
        self.assertEqual(miser.current_position, Rooms.REDWALL_ROOM)
        miser.flags["vault_open"] = True
        miser.handle_command(["open", "vault"])
        self.assertEqual(miser.current_position, Rooms.REDWALL_ROOM)
        # open organ needs ballroom
        miser.current_position = Rooms.FRONT_PORCH
        miser.handle_command(["open", "organ"])
        self.assertEqual(miser.current_position, Rooms.FRONT_PORCH)
        miser.current_position = Rooms.BALLROOM
        miser.handle_command(["open", "organ"])
        self.assertEqual(miser.current_position, Rooms.BALLROOM)
        miser.flags["organ_playing"] = True
        miser.handle_command(["open", "organ"])
        self.assertEqual(miser.current_position, Rooms.BALLROOM)
        miser.handle_command(["open", "organ"])
        self.assertEqual(miser.current_position, Rooms.BALLROOM)

    def test_welcome(self):
        ui = TestUI()
        welcome_banner(ui)
        self.assertTrue(True)


def suite():
    """Test Suite"""
    my_suite = unittest.TestSuite()
    my_suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(MiserTest)
    )
    return my_suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
