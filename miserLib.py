# This is a Python port of the Miser's House BASIC adventure.
#
# BASIC original by M. J. Winter
# (c) 1981 The Code Works
#
# Python Version (c) 2021  Kelly M. Hall
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#
# CC BY-NC-SA 3.0

from enum import IntEnum
import pyreadline.rlmain

# constants
PROGRAM_NAME, CURSOR_ISSUE = 'miser', '27'


# todo make help message class
help_strings, help_index = [], 0

# UI configuration
text_wrap_width = 80
read_line = pyreadline.Readline()
prompt = "> "


def clear_screen():
    read_line.console.home()
    read_line.console.clear_to_end_of_window()


def wait_for_keypress():
    _ = read_line.readline()


def delay():
    pass


#
# Class for the overall Miser game
#
class Miser:
    def __init__(self, ui):
        self.ui = ui
        self.flags = {
            "game_over": False,
            "pool_flooded": True,
            "bucket_full": False,
            "fire_burning": True,
            "vault_open": False,
            "found_vault": False,
            "dungeon_unlocked": False,
            "know_combination": False,
            "organ_playing": False,
            "escaped": False,
            "snake_charmed": False,
            "angry_snake": False,
            "jump_warning": False,
            "portal_visible": False
        }

        self.current_position = 0
        self.gathered_treasures = 0

        self.items = []
        self.rooms = []
        self.verbs = []
        self.subjects = []

        global help_strings
        help_strings = ['what?', "i don't understand that"]

        self.initialize_rooms()
        self.initialize_verbs()
        self.initialize_subjects()
        self.initialize_items()

    # todo: get rid of magic numbers
    def initialize_items(self):
        item_data = [
            ('--unused--', -999),
            ('plastic bucket', 26), ('vicious snake', 4), ('charmed snake', -2), ('*golden leaf*', 45),
            ('*bulging moneybag*', 46), ('>$<', -2), ('*diamond ring*', 48), ('*rare painting*', 39),
            ('sword', 13), ('mat', 0), ('rusty cross', 23), ('penny', 28), ('piece of paper', 31),
            ('parachute with no ripcord', 34), ('oriental rug', 6), ("trapdoor marked 'danger'", -2),
            ('parachute ripcord', -2), ('portal in north wall', -2), ('pair of *ruby slippers*', -2),
            ('brass door key', -2), ('majestic staircase leading up', 2),
            ('majestic staircase leading down', 27), ('battered book', 11), ('organ in the corner', 21),
            ('open organ in the corner', -2), ('cabinet on rollers against one wall over', 5),
            ('repaired parachute', -2), ("sign saying 'drop coins for luck'", 19)
        ]
        temp_list = []
        for (xx, yy) in item_data:
            temp_list.append(ItemClass(xx, yy))
        self.items = temp_list

    # todo: get rid of magic numbers
    def initialize_subjects(self):
        command_subject_data = [
            ('--unused--', -999),
            ('ripc', 17), ('mat', 10), ('pape', 13), ('buck', 1), ('swor', 9),
            ('key', 20), ('valv', -1), ('ladd', -1), ('slip', 19), ('rug', 15),
            ('book', 23), ('door', -1), ('cabi', -1), ('ritn', -1), ('vict', -1),
            ('orga', -1), ('para', 14), ('stai', -1), ('penn', 12), ('cros', 11),
            ('leaf', 4), ('bag', 5), ('>$<', -1), ('>$<', -1), ('ring', 7),
            ('pain', 8), ('vaul', -1), ('pool', -1), ('xyzz', -1), ('plug', -1)
        ]
        temp_list = []
        for (xx, yy) in command_subject_data:
            co = CommandSubjectClass(xx, yy)
            temp_list.append(co)
        self.subjects = temp_list

    # todo: get rid of magic numbers
    def initialize_verbs(self):
        verb_data = [
            ('--unused--', self.unused_command),
            ('get', self.get_take_command),
            ('take', self.get_take_command),
            ('move', self.move_slide_push_command),
            ('slid', self.move_slide_push_command),
            ('push', self.move_slide_push_command),
            ('open', self.open_command),
            ('read', self.read_command),
            ('inve', self.inventory_command),
            ('quit', self.quit_command),
            ('drop', self.drop_command),
            ('say', self.say_command),
            ('pour', self.pour_command),
            ('fill', self.fill_command),
            ('unlo', self.unlock_command),
            ('look', self.look_command),
            ('go', self.go_command),
            ('nort', self.north_command),
            ('n', self.north_command),
            ('sout', self.south_command),
            ('s', self.south_command),
            ('east', self.east_command),
            ('e', self.east_command),
            ('west', self.west_command),
            ('w', self.west_command),
            ('scor', self.score_command),
            ('turn', self.turn_command),
            ('jump', self.jump_command),
            ('swim', self.swim_command),
            ('i', self.inventory_command),
            ('fix', self.fix_command)
        ]
        temp_list = []
        for (xx, yy) in verb_data:
            temp_list.append(VerbClass(xx, yy))
        self.verbs = temp_list

    # todo: get rid of magic numbers
    def initialize_rooms(self):
        room_data = [
            ([1, 0, 0, 0], 'front porch'),
            ([2, 0, 0, 12], 'foyer to a large house.  dust is everywhere'),
            ([3, 1, 0, 0], 'great hall.  suits of armor line the walls'),
            ([0, 2, 4, 16], 'breakfast room.  it is bright and cheery'),
            ([0, 5, 7, 3], 'conservatory.  through a window you see a hedge-maze'),
            ([4, 6, 0, 0], 'red-walled room'),
            ([5, 0, 10, 0], 'formal parlor'),
            ([0, 0, 8, 4], 'green drawing room'),
            ([0, 9, 0, 7], 'trophy room.  animal heads line the walls'),
            ([8, 0, 0, 10], 'den'),
            ([0, 11, 9, 6], 'blue drawing room'),
            ([10, 0, 0, 0], 'library.  empty shelves line walls'),
            ([0, 0, 1, 13], 'dining room'),
            ([15, 0, 12, 0], 'chinese room'),
            ([0, 0, 0, 0], '$'),
            ([23, 13, 16, 0], 'kitchen.  it is bare'),
            ([0, 0, 3, 15], 'pantry.  dust covers the mahogany shelves'),
            ([0, 8, 0, 18], 'game room'),
            ([21, 0, 17, 19], 'smoking room.  the air is stale in here'),
            ([21, 0, 18, 20], 'portico.  a murky pool glimmers on the south side'),
            ([21, 21, 19, 19], 'hall of mirrors - a good place to reflect'),
            ([0, 19, 0, 20], 'ballroom.  it has a beautiful wood dance floor'),
            ([0, 0, 0, 21], "chapel.  a tablet says 'drop a religious item or die!!'"),
            ([24, 15, 40, 25], 'back yard'),
            ([24, 23, 24, 24], 'forest'),
            ([26, 0, 23, 0], 'pool area.  there is a large swimming pool here'),
            ([0, 25, 0, 0], 'pump house.  there is pool machinery installed here'),
            ([35, 0, 31, 28], 'middle of the western hallway'),
            ([0, 0, 27, 0], 'west bedroom'),
            ([39, 0, 0, 0], 'front balcony.  there is a large road below'),
            ([0, 0, 0, 0], '$'),
            ([0, 0, 38, 27], 'master bedroom.  there''s a huge four-poster bed'),
            ([0, 36, 0, 0], 'rear balcony.  below you see a hedge maze'),
            ([34, 0, 0, 38], 'east bedroom'),
            ([0, 33, 0, 0], 'closet'),
            ([0, 27, 36, 0], 'junction of the west hallway and the north-south hallway'),
            ([32, 0, 37, 35], 'center of the north-south hallway'),
            ([0, 38, 0, 36], 'junction of the east hallway and the north-south hallway'),
            ([37, 39, 33, 31], 'middle of the east hallway'),
            ([38, 29, 0, 0], 'south end of east hallway'),
            ([0, 42, 0, 41], 'hedge maze'),
            ([44, 42, 0, 0], 'hedge maze'),
            ([41, 44, 43, 0], 'hedge maze'),
            ([41, 23, 0, 0], 'hedge maze'),
            ([0, 42, 0, 45], 'hedge maze'),
            ([0, 0, 44, 0], 'hedge maze'),
            ([0, 0, 0, 5], 'walk-in vault'),
            ([0, 40, 0, 0], 'dungeon.  there is light above and to the south'),
            ([0, 0, 0, 0], 'bottom of the swimming pool.  a ladder leads up and out')
        ]
        temp_list = []
        for (xx, yy) in room_data:
            temp_list.append(RoomClass(yy, xx))
        self.rooms = temp_list

    def get_item_location(self, subject_idx):
        return self.items[self.subjects[subject_idx].item_id].location

    def main_command_loop(self):
        while not self.flags["game_over"]:
            self.ui.mp()
            input_str = get_input()
            input_str.strip()
            parsed_words = input_str.split()
            if len(parsed_words) < 1 or len(parsed_words) > 2:
                self.ui.mp('please type a one or two word command')
            else:
                self.handle_command(parsed_words)

    def handle_command(self, word_list):
        command_verb = word_list[0]
        subject = 'unassigned'
        if len(command_verb) > 4:
            command_verb = command_verb[0:4]
        verb_index = -1
        for x in range(1, len(self.verbs)):
            if command_verb == self.verbs[x].text:
                verb_index = x
                break
        if verb_index == -1:
            error_unknown_object(command_verb)
            return

        if len(word_list) == 1:
            subject_index = 0
        else:
            subject = word_list[1]
            if len(subject) > 4:
                subject = subject[0:4]
            subject_index = -1
            for x in range(1, len(self.subjects)):
                if subject == self.subjects[x].text:
                    subject_index = x
                    break
            if subject_index == -1:
                error_unknown_object(subject)
                return

        self.verbs[verb_index].handler(subject_index, subject)

    # unused command for dummy verbs
    @staticmethod
    def unused_command(subject_index, subject):
        _, _ = subject_index, subject
        pass

    # get, take object
    def get_take_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('what?')
        elif self.subjects[subject_index].item_id == -1:
            self.ui.mp('i am unable to do that.')
        elif self.get_item_location(subject_index) == -1:
            self.ui.mp("you're already carrying it")
        elif self.get_item_location(subject_index) != self.current_position:
            error_not_here()
        else:
            self.items[self.subjects[subject_index].item_id].location = -1
            self.ui.mp('ok')
            if (3 < self.subjects[subject_index].item_id < 9) or self.subjects[subject_index].item_id == 19:
                self.ui.mp('you got a treasure!')
                self.gathered_treasures += 1
            if subject_index == 2 and self.items[20].location == -2:
                self.ui.mp('you find a door key!')
                self.items[20].location = 0

    # move, slide, push
    def move_slide_push_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('move what?')
        elif subject_index == 13 and self.current_position == 5 and self.rooms[5].moves[Move.EAST] == 0:
            self.ui.mp('behind the cabinet is a vault!')
            self.flags["found_vault"] = True
            self.describe_current_position()
        elif self.subjects[subject_index].item_id == -1:
            self.ui.mp('that item stays put.')
        elif self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            error_not_here()
        elif subject_index == 2 and self.items[20].location == -2:
            self.ui.mp('you find a door key!')
            self.items[20].location = 0
        elif subject_index == 10 and self.items[16].location == -2:
            self.ui.mp('you find a trap door!')
            self.items[16].location = 6
            self.describe_current_position()
        else:
            self.ui.mp('moving it reveals nothing.')

    # open
    def open_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('open what?')
        elif subject_index == 11:
            self.open_book(subject_index)
        elif subject_index == 7:
            self.ui.mp('try turning it.')
        elif subject_index == 12:
            self.open_door()
        elif subject_index == 13:
            self.open_cabinet()
        elif subject_index == 22:
            self.open_bag(subject_index)
        elif subject_index == 27:
            self.open_vault()
        elif subject_index == 16:
            self.open_organ()
        else:
            self.ui.mp("i don't know how to open that.")

    def open_door(self):
        if self.current_position == 0 and not self.flags["dungeon_unlocked"]:
            self.ui.mp('sorry, the door is locked.')
        elif self.current_position == 0 and self.flags["dungeon_unlocked"]:
            self.ui.mp("it's already open.")
        elif self.current_position != 6:
            error_not_here()
        else:
            self.wrap_string('you open the door. you lean over to peer in, and you fall in!', text_wrap_width)
            self.current_position = 47
            self.describe_current_position()

    def open_cabinet(self):
        if self.items[26].location != self.current_position:
            error_not_here()
        else:
            self.ui.mp('the cabinet is empty and dusty.')
            self.wrap_string("scribbled in the dust on one shelf are the words, 'behind me'.", text_wrap_width)

    def open_bag(self, subject_index):
        if self.get_item_location(subject_index) != self.current_position\
                and self.get_item_location(subject_index) != -1:
            error_not_here()
        else:
            self.ui.mp('the bag is knotted securely.')
            self.ui.mp("it won't open.")

    def open_vault(self):
        if self.current_position != 5 or not self.flags["found_vault"]:
            error_not_here()
        elif self.flags["vault_open"]:
            self.ui.mp("it's already open.")
        else:
            self.ui.mp("i can't, it's locked.")

    def open_organ(self):
        if self.current_position != 21:
            error_not_here()
        elif not self.flags["organ_playing"]:
            self.ui.mp("it's stuck shut.")
        elif self.items[24].location == -2:
            self.ui.mp("it's already open.")
        else:
            self.ui.mp('as you open it, several objects suddenly appear!')
            self.items[24].location = -2
            self.items[25].location = 21
            self.items[19].location = 21
            self.items[17].location = 21
            self.describe_current_position()

    def open_book(self, subject_index):
        if self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            error_not_here()
        else:
            self.wrap_string("scrawled in blood on the inside front cover is the message,", text_wrap_width)
            self.ui.mp("''victory' is a prize-winning word'.")

    # read
    def read_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('read what?')
        elif self.subjects[subject_index].item_id > -1 \
                and self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            error_not_here()
        elif self.subjects[subject_index].item_id == -1:
            self.ui.mp("there's nothing written on that.")
        elif subject_index != 3 and subject_index != 11:
            self.ui.mp("there's nothing written on that.")
        elif subject_index == 11:
            self.ui.mp('the front cover is inscribed in greek.')
        else:
            self.ui.mp("it says, '12-35-6'.")
            self.ui.mp('hmm.. looks like a combination.')
            self.flags["know_combination"] = True

    # inventory
    def inventory_command(self, subject_index, subject):
        _, _ = subject_index, subject
        self.ui.mp('you are carrying the following:')
        carrying_something = False
        for x in range(1, len(self.items)):
            if self.items[x].location == -1:
                self.ui.mp(self.items[x].text)
                carrying_something = True
            if x == 1 and self.flags["bucket_full"] and self.items[1].location == -1:
                self.ui.mp('  the bucket is full of water.')
            if x == 14 and self.items[14].location == -1:
                self.ui.mp('   (better fix it)')
        if not carrying_something:
            self.ui.mp('nothing at all.')

    # quit
    def quit_command(self, subject_index, subject):
        _, _ = subject_index, subject
        self.ui.mp('do you indeed wish to quit now?')
        input_str = get_input()
        if input_str[0].lower() != 'y':
            self.ui.mp('ok')
        else:
            clear_screen()
            self.final_stats()
            self.flags["game_over"] = True

    # drop
    def drop_command(self, subject_index, subject):
        _ = subject
        if self.get_item_location(subject_index) != -1:
            self.ui.mp("you aren't carrying it!")
            return

        x = self.subjects[subject_index].item_id
        if (3 < x < 9) or x == 19:
            self.ui.mp("don't drop *treasures*!")
        elif self.current_position == 19 and subject_index == 19:
            self.wrap_string('as the penny sinks below the surface of the pool, a fleeting image of', text_wrap_width)
            self.ui.mp('a chapel with dancers appears.')
            self.rooms[21].moves[Move.EAST] = 22
            self.items[12].location = -2
        elif self.current_position == 22 and subject_index == 20:
            self.wrap_string('even before it hits the ground, the cross fades away!', text_wrap_width)
            self.ui.mp('the tablet has disintegrated.')
            self.ui.mp('you hear music from the organ.')
            self.flags["organ_playing"] = True
            self.items[11].location = -2
            self.rooms[22].text = 'chapel'
            self.items[24].text = 'closed organ playing music in the corner'
        else:
            self.items[self.subjects[subject_index].item_id].location = self.current_position
            self.ui.mp('ok')

    # say
    def say_command(self, subject_index, word):
        if subject_index == 0:
            self.ui.mp('say what???')
        elif subject_index == 14:
            self.say_ritnew()
        elif subject_index == 15:
            self.say_victory()
        elif subject_index > 28:
            self.ui.mp("a hollow voice says, 'wrong adventure'.")
        else:
            self.ui.mp('okay, "', word, '".')
            delay()
            self.ui.mp('nothing happens.')

    def say_victory(self):
        if self.current_position != 8 or self.flags["portal_visible"]:
            self.ui.mp('nothing happens.')
        else:
            self.ui.mp('a portal has opened in the north wall!!')
            self.flags["portal_visible"] = True
            self.rooms[8].moves[Move.NORTH] = 17
            self.items[18].location = 8

    def say_ritnew(self):
        if self.current_position != 4 or self.flags["snake_charmed"]:
            self.ui.mp('nothing happens.')
        else:
            self.wrap_string('the snake is charmed by the very utterance of your words.', text_wrap_width)
            self.flags["snake_charmed"] = True
            self.items[2].location = -2
            self.items[3].location = 4

    # pour
    def pour_command(self, subject_index, subject):
        _ = subject
        if subject_index != 4:
            self.ui.mp("i wouldn't know how.")
        elif self.items[1].location != -1 and self.items[1].location != self.current_position:
            error_not_here()
        elif not self.flags["bucket_full"]:
            self.ui.mp('the bucket is already empty')
        elif self.current_position == 19:
            self.ui.mp('ok')
        elif self.current_position != 10 or not self.flags["fire_burning"]:
            self.ui.mp('the water disappears quickly.')
            self.flags["bucket_full"] = False
        else:
            self.ui.mp('congratulations! you have vanquished')
            self.ui.mp('the flames!')
            self.flags["fire_burning"] = False
            self.flags["bucket_full"] = False
            self.describe_current_position()

    # fill
    def fill_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('what?')
        elif self.subjects[subject_index].item_id == -1:
            self.ui.mp("that wouldn't hold anything.")
        elif self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            error_not_here()
        elif subject_index != 4:
            self.ui.mp("that wouldn't hold anything.")
        elif self.flags["bucket_full"]:
            self.ui.mp("it's already full.")
        elif self.current_position == 25 and self.flags["pool_flooded"]:
            self.ui.mp("i'd rather stay away from the mercury.")
        elif self.current_position != 23 and self.current_position != 19:
            self.ui.mp("i don't see any water here.")
        else:
            self.ui.mp('your bucket is now full.')
            self.flags["bucket_full"] = True

    # unlock object
    def unlock_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('what?')
        elif subject_index != 12 and subject_index != 27:
            self.ui.mp("i wouldn't know how to unlock one.")
        elif self.current_position != 0 and self.current_position != 5 and self.current_position != 6:
            error_not_here()
        elif self.current_position == 0 and subject_index == 12:
            self.unlock_front_door()
        elif self.current_position == 5 and subject_index == 27:
            self.unlock_vault()
        elif self.current_position != 6 or subject_index != 12 or self.items[16].location != -2:
            error_not_here()
        else:
            self.ui.mp('the trapdoor has no lock')

    def unlock_vault(self):
        if self.flags["vault_open"]:
            self.ui.mp("it's already open.")
        elif not self.flags["found_vault"]:
            error_not_here()
        elif not self.flags["know_combination"]:
            self.ui.mp('i don''t know the combination.')
        else:
            self.ui.mp("ok, let's see.  12..35..6..")
            self.ui.mp('<click!> the door swings open.')
            self.flags["vault_open"] = True
            self.rooms[5].moves[Move.EAST] = 46
            self.describe_current_position()

    def unlock_front_door(self):
        if self.flags["dungeon_unlocked"]:
            self.ui.mp("it's already unlocked.")
        elif self.items[20].location != -1:
            self.ui.mp('i need a key.')
        else:
            self.ui.mp('the door easily unlocks and swings open.')
            self.flags["dungeon_unlocked"] = True
            self.describe_current_position()

    # look
    def look_command(self, subject_index, subject):
        _, _ = subject_index, subject
        self.describe_current_position()

    # go
    def go_command(self, subject_index, subject):
        _ = subject
        if subject_index != 8 and subject_index != 18 and subject_index != 28:
            error_unknown_object('what?')
        elif subject_index == 8 and self.current_position != 48:
            error_not_here()
        elif subject_index == 18 and self.current_position != 2 and self.current_position != 27:
            error_not_here()
        elif subject_index == 28 and self.current_position != 25:
            error_not_here()
        elif subject_index == 8:
            self.current_position = 25
            self.describe_current_position()
        elif subject_index == 28 and self.flags["pool_flooded"]:
            self.ui.mp('the pool is full of mercury!')
        elif subject_index == 28:
            self.current_position = 48
        elif self.current_position == 27:
            self.current_position = 2
            self.describe_current_position()
        elif self.items[9].location == -1:
            self.ui.mp('the suits of armor try to stop you,')
            self.ui.mp('but you fight them off with your sword.')
            self.current_position = 27
            self.describe_current_position()
        else:
            self.wrap_string('the suits of armor prevent you from going up!', text_wrap_width)

    # north
    def north_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position == 0 and not self.flags["dungeon_unlocked"]:
            self.ui.mp('the door is locked shut.')
            return
        elif self.rooms[self.current_position].moves[Move.NORTH] == 0:
            error_no_path()
            return
        elif self.current_position == 0:
            self.ui.mp('the door slams shut behind you!')
        self.current_position = self.rooms[self.current_position].moves[Move.NORTH]
        self.describe_current_position()

    # south
    def south_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position == 10 and self.flags["fire_burning"]:
            self.ui.mp('you have burnt to a crisp!')
            self.flags["game_over"] = True
            self.final_stats()
        elif self.rooms[self.current_position].moves[Move.SOUTH] == 0:
            error_no_path()
        else:
            self.current_position = self.rooms[self.current_position].moves[Move.SOUTH]
            self.describe_current_position()

    # east
    def east_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position == 4 and not self.flags["snake_charmed"] and not self.flags["angry_snake"]:
            self.ui.mp('the snake is about to attack!')
            self.flags["angry_snake"] = True
        elif self.current_position == 4 and not self.flags["snake_charmed"]:
            self.ui.mp('the snake bites you!')
            self.ui.mp('you are dead.')
            self.flags["game_over"] = True
            self.final_stats()
        elif self.rooms[self.current_position].moves[Move.EAST] == 0:
            error_no_path()
        else:
            self.current_position = self.rooms[self.current_position].moves[Move.EAST]
            self.describe_current_position()

    # west
    def west_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.rooms[self.current_position].moves[Move.WEST] == 0:
            error_no_path()
        else:
            self.current_position = self.rooms[self.current_position].moves[Move.WEST]
            self.describe_current_position()

    # score
    def score_command(self, subject_index, subject):
        _, _ = subject_index, subject
        self.ui.mp('if you were to quit now,')
        self.ui.mp('you would have a score of')
        self.ui.mp(self.gathered_treasures * 20, 'points.')
        self.ui.mp('(100 possible)')
        while not self.flags["game_over"]:
            self.ui.mp('do you indeed wish to quit now? ')
            input_str = get_input()
            if input_str[0].lower() == 'y':
                self.flags["game_over"] = True
                self.final_stats()
            elif input_str[0].lower() == 'n':
                self.ui.mp('ok')
                self.ui.mp()
                break

    # turn
    def turn_command(self, subject_index, subject):
        _ = subject
        if subject_index != 7:
            self.ui.mp("i don't know how to turn such a thing.")
            self.describe_current_position()
        elif self.current_position != 26:
            error_not_here()
        else:
            self.wrap_string('with much effort, you turn the valve 5 times.  you hear the sound of liquid',
                             text_wrap_width)
            self.ui.mp('flowing through the pipes.')
            self.flags["pool_flooded"] = not self.flags["pool_flooded"]
            if not self.flags["pool_flooded"] and self.items[7].location == -3:
                self.items[7].location = 25
            elif self.flags["pool_flooded"] and self.items[7].location == 25:
                self.items[7].location = -3

    # jump
    def jump_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position != 27 and self.current_position != 29 and self.current_position != 32:
            self.ui.mp("there's nowhere to jump.")
        else:
            self.ui.mp('you jump..')
            if self.current_position == 27:
                self.jump_down_stairs()
            elif self.items[14].location == -1:
                self.ui.mp('there is no way to open the parachute!')
            elif self.items[27].location == -1:
                self.ui.mp('you yank the ripcord and the')
                self.ui.mp("'chute comes billowing out.")
                if self.current_position == 32:
                    self.current_position = 40
                    self.describe_current_position()
                else:
                    self.ui.mp('you land safely')
                    self.ui.mp('congratulations on escaping!')
                    self.flags["escaped"] = True
                    self.final_stats()
            self.ui.mp('you hit the ground.')
            self.ui.mp("you have broken your neck!")
            self.ui.mp("you are dead.")
            self.flags["game_over"] = True
            self.final_stats()

    def jump_down_stairs(self):
        if self.flags["jump_warning"]:
            self.ui.mp("now you've done it.  you ignored")
            self.ui.mp("my warning, and as a result")
            self.ui.mp("you have broken your neck!")
            self.ui.mp("you are dead.")
            self.flags["game_over"] = True
            self.final_stats()
        else:
            self.ui.mp('you have landed down-stairs,')
            self.ui.mp('and narrowly escaped serious')
            self.ui.mp("injury.  please don't try it again.")
            self.flags["jump_warning"] = True
            self.current_position = 2
            self.describe_current_position()

    # swim
    def swim_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position != 19 and self.current_position != 25:
            self.ui.mp("there's nothing here to swim in!")
        elif self.current_position == 19:
            self.ui.mp('the water is only a few inches deep.')
        elif self.flags["pool_flooded"]:
            self.ui.mp("in mercury?  no way!")
        else:
            self.ui.mp('the pool is empty.')

    # fix
    def fix_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('what')
        elif subject_index == 7:
            self.ui.mp("i ain't no plumber!")
        elif subject_index != 17:
            self.ui.mp("i wouldn't know how.")
        elif self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            error_not_here()
        elif self.items[14].location == -2:
            self.ui.mp("it's already fixed.")
        elif self.items[17].location != -1:
            self.ui.mp("i'll need a ripcord.")
        else:
            self.ui.mp("i'm no expert, but i think it'll work.")
            self.items[27].location = self.items[14].location
            self.items[14].location = -2
            self.subjects[17].item_id = 27
            self.items[17].location = 0

    def describe_current_position(self):
        self.wrap_string(f'you are in the {self.rooms[self.current_position].text}', text_wrap_width)
        for x in range(1, len(self.items)):
            if self.items[x].location == self.current_position:
                self.wrap_string(f'there is a {self.items[x].text} here', text_wrap_width)
            if x == 1 and self.flags["bucket_full"] and self.items[1].location == self.current_position:
                self.ui.mp("the bucket is full of water")
        if self.current_position == 25:
            if self.flags["pool_flooded"]:
                self.ui.mp('the pool is full of liquid mercury')
            else:
                self.ui.mp("the pool's empty")
                if self.items[7].location == 48:
                    self.ui.mp('i see something shiny in the pool!')
        if self.current_position == 10 and self.flags["fire_burning"]:
            self.ui.mp('there is a hot fire on the south wall!')
            self.ui.mp("if I go that way I'll burn to death!")
        if self.current_position == 16:
            self.wrap_string("a rich, full voice says, 'ritnew is a charming word'.", text_wrap_width)
        if self.current_position == 26:
            self.ui.mp('there is a valve on one of the pipes.')
        if self.current_position == 23:
            self.ui.mp('there is a leaky faucet nearby.')
        if self.current_position == 10 and not self.flags["fire_burning"]:
            self.ui.mp('there is evidence of a recent fire here.')
        if self.current_position == 5 and self.flags["found_vault"]:
            self.ui.mp('there is a vault in the east wall.')
        if self.current_position == 5 and self.flags["vault_open"]:
            self.ui.mp('the vault is open')
        if self.current_position == 0 and self.flags["dungeon_unlocked"]:
            self.ui.mp('an open door leads north.')
        if self.current_position != 48:
            self.ui.mp('obvious exits:')
            if self.rooms[self.current_position].moves[Move.NORTH] > 0:
                self.ui.mp('n ', end='')
            if self.rooms[self.current_position].moves[Move.SOUTH] > 0:
                self.ui.mp('s ', end='')
            if self.rooms[self.current_position].moves[Move.EAST] > 0:
                self.ui.mp('e ', end='')
            if self.rooms[self.current_position].moves[Move.WEST] > 0:
                self.ui.mp('w ', end='')
            self.ui.mp('')

    def final_stats(self):
        self.ui.mp('you accumulated', self.gathered_treasures, 'treasures,')
        self.ui.mp('for a score of', self.gathered_treasures * 20, 'points.')
        self.ui.mp('(100 possible)')
        if not self.flags["escaped"]:
            self.ui.mp('however, you did not escape.')
        self.ui.mp('this puts you in a class of:')
        if self.flags["escaped"]:
            self.gathered_treasures += 1
        if self.gathered_treasures == 0:
            self.ui.mp('<beginner adventurer>')
        elif self.gathered_treasures == 1:
            self.ui.mp('<amateur adventurer>')
        elif self.gathered_treasures == 2:
            self.ui.mp('<journeyman adventurer>')
        elif self.gathered_treasures == 3:
            self.ui.mp('<experienced adventurer>')
        elif self.gathered_treasures == 4:
            self.ui.mp('<professional adventurer>')
        elif self.gathered_treasures == 5:
            self.ui.mp('<master adventurer>')
        else:
            self.ui.mp('<grandmaster adventurer>')
        if self.gathered_treasures < 6:
            self.ui.mp('better luck next time!')

    @staticmethod
    def wrap_string(long_string, width):
        if len(long_string) < width:
            print(long_string)
        else:
            last_space_index = long_string.rfind(' ', 0, width)
            print(long_string[:last_space_index])
            print(long_string[last_space_index + 1:])


class Move(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


#
# class for locations that the adventurer can move between
#
class RoomClass:
    def __init__(self, description, directions):
        self.text = description
        self.moves = directions


#
# class for items that the adventurer can carry and maybe drop
#
class ItemClass:
    def __init__(self, text, location):
        self.text = text
        self.location = location


#
# class for things that a command can mention
#
class CommandSubjectClass:
    def __init__(self, text, item_id):
        self.text = text
        self.item_id = item_id


#
# class for defined verbs and their handler function
#
class VerbClass:
    def __init__(self, text, handler):
        self.text = text
        self.handler = handler


class IUserInterface:
    @staticmethod
    def mp(*args, sep=' ', end='\n'):
        raise NotImplementedError


def error_unknown_object(subject):
    global help_index
    print(f'{subject}?  {help_strings[help_index]}')
    help_index += 1
    if help_index >= len(help_strings):
        help_index = 0


def error_not_here():
    print("i don't see it here")


def error_no_path():
    print("it's impossible to go that way.")


def get_input():
    global prompt
    return read_line.readline(prompt)
