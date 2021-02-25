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

import pyreadline.rlmain

# constants
PROGRAM_NAME, CURSOR_ISSUE = 'miser', '27'
MOVE_NORTH, MOVE_SOUTH, MOVE_EAST, MOVE_WEST = 0, 1, 2, 3

# variables
# todo put these into the miser class
items = []
rooms = []
command_subjects = []
verbs = []

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


def get_item_location(subject_idx):
    global items, command_subjects
    return items[command_subjects[subject_idx].item_id].location


#
# Class for the overall Miser game
#
class Miser:
    def __init__(self):
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

        global rooms
        global items
        global verbs
        global command_subjects

        global help_strings
        help_strings = ['what?', "i don't understand that"]

        self.initialize_rooms()
        self.initialize_verbs()
        self.initialize_subjects()
        self.initialize_items()

    # todo: get rid of magic numbers
    @staticmethod
    def initialize_items():
        global items
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
        items = temp_list

    # todo: get rid of magic numbers
    @staticmethod
    def initialize_subjects():
        global command_subjects
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
        command_subjects = temp_list

    # todo: get rid of magic numbers
    def initialize_verbs(self):
        global verbs
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
        verbs = temp_list

    # todo: get rid of magic numbers
    @staticmethod
    def initialize_rooms():
        global rooms
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
        rooms = temp_list

    def main_command_loop(self):
        while not self.flags["game_over"]:
            print()
            input_str = get_input()
            input_str.strip()
            parsed_words = input_str.split()
            if len(parsed_words) < 1 or len(parsed_words) > 2:
                print('please type a one or two word command')
            else:
                self.handle_command(parsed_words)

    @staticmethod
    def handle_command(word_list):
        global verbs, command_subjects
        command_verb = word_list[0]
        subject = 'unassigned'
        if len(command_verb) > 4:
            command_verb = command_verb[0:4]
        verb_index = -1
        for x in range(1, len(verbs)):
            if command_verb == verbs[x].text:
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
            for x in range(1, len(command_subjects)):
                if subject == command_subjects[x].text:
                    subject_index = x
                    break
            if subject_index == -1:
                error_unknown_object(subject)
                return

        verbs[verb_index].handler(subject_index, subject)

    # unused command for dummy verbs
    @staticmethod
    def unused_command(subject_index, subject):
        _, _ = subject_index, subject
        pass

    # get, take object
    def get_take_command(self, subject_index, subject):
        _ = subject
        global command_subjects, items
        if subject_index == 0:
            error_unknown_object('what?')
        elif command_subjects[subject_index].item_id == -1:
            print('i am unable to do that.')
        elif get_item_location(subject_index) == -1:
            print("you're already carrying it")
        elif get_item_location(subject_index) != self.current_position:
            error_not_here()
        else:
            items[command_subjects[subject_index].item_id].location = -1
            print('ok')
            if (3 < command_subjects[subject_index].item_id < 9) or command_subjects[subject_index].item_id == 19:
                print('you got a treasure!')
                self.gathered_treasures += 1
            if subject_index == 2 and items[20].location == -2:
                print('you find a door key!')
                items[20].location = 0

    # move, slide, push
    def move_slide_push_command(self, subject_index, subject):
        _ = subject
        global rooms, command_subjects, items
        if subject_index == 0:
            error_unknown_object('move what?')
        elif subject_index == 13 and self.current_position == 5 and rooms[5].moves[MOVE_EAST] == 0:
            print('behind the cabinet is a vault!')
            self.flags["found_vault"] = True
            self.describe_current_position()
        elif command_subjects[subject_index].item_id == -1:
            print('that item stays put.')
        elif get_item_location(subject_index) != self.current_position and get_item_location(subject_index) != -1:
            error_not_here()
        elif subject_index == 2 and items[20].location == -2:
            print('you find a door key!')
            items[20].location = 0
        elif subject_index == 10 and items[16].location == -2:
            print('you find a trap door!')
            items[16].location = 6
            self.describe_current_position()
        else:
            print('moving it reveals nothing.')

    # open
    def open_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('open what?')
        elif subject_index == 11:
            self.open_book(subject_index)
        elif subject_index == 7:
            print('try turning it.')
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
            print("i don't know how to open that.")

    def open_door(self):
        if self.current_position == 0 and not self.flags["dungeon_unlocked"]:
            print('sorry, the door is locked.')
        elif self.current_position == 0 and self.flags["dungeon_unlocked"]:
            print("it's already open.")
        elif self.current_position != 6:
            error_not_here()
        else:
            wrap_string('you open the door. you lean over to peer in, and you fall in!')
            self.current_position = 47
            self.describe_current_position()

    def open_cabinet(self):
        if items[26].location != self.current_position:
            error_not_here()
        else:
            print('the cabinet is empty and dusty.')
            wrap_string("scribbled in the dust on one shelf are the words, 'behind me'.")

    def open_bag(self, subject_index):
        if get_item_location(subject_index) != self.current_position and get_item_location(subject_index) != -1:
            error_not_here()
        else:
            print('the bag is knotted securely.')
            print("it won't open.")

    def open_vault(self):
        if self.current_position != 5 or not self.flags["found_vault"]:
            error_not_here()
        elif self.flags["vault_open"]:
            print("it's already open.")
        else:
            print("i can't, it's locked.")

    def open_organ(self):
        global items
        if self.current_position != 21:
            error_not_here()
        elif not self.flags["organ_playing"]:
            print("it's stuck shut.")
        elif items[24].location == -2:
            print("it's already open.")
        else:
            print('as you open it, several objects suddenly appear!')
            items[24].location = -2
            items[25].location = 21
            items[19].location = 21
            items[17].location = 21
            self.describe_current_position()

    def open_book(self, subject_index):
        if get_item_location(subject_index) != self.current_position and get_item_location(subject_index) != -1:
            error_not_here()
        else:
            wrap_string("scrawled in blood on the inside front cover is the message,")
            print("''victory' is a prize-winning word'.")

    # read
    def read_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            error_unknown_object('read what?')
        elif command_subjects[subject_index].item_id > -1 \
                and get_item_location(subject_index) != self.current_position \
                and get_item_location(subject_index) != -1:
            error_not_here()
        elif command_subjects[subject_index].item_id == -1:
            print("there's nothing written on that.")
        elif subject_index != 3 and subject_index != 11:
            print("there's nothing written on that.")
        elif subject_index == 11:
            print('the front cover is inscribed in greek.')
        else:
            print("it says, '12-35-6'.")
            print('hmm.. looks like a combination.')
            self.flags["know_combination"] = True

    # inventory
    def inventory_command(self, subject_index, subject):
        _, _ = subject_index, subject
        global items
        print('you are carrying the following:')
        carrying_something = False
        for x in range(1, len(items)):
            if items[x].location == -1:
                print(items[x].text)
                carrying_something = True
            if x == 1 and self.flags["bucket_full"] and items[1].location == -1:
                print('  the bucket is full of water.')
            if x == 14 and items[14].location == -1:
                print('   (better fix it)')
        if not carrying_something:
            print('nothing at all.')

    # quit
    def quit_command(self, subject_index, subject):
        _, _ = subject_index, subject
        print('do you indeed wish to quit now?')
        input_str = get_input()
        if input_str[0].lower() != 'y':
            print('ok')
        else:
            clear_screen()
            self.final_stats()
            self.flags["game_over"] = True

    # drop
    def drop_command(self, subject_index, subject):
        _ = subject
        global items, command_subjects, rooms
        if get_item_location(subject_index) != -1:
            print("you aren't carrying it!")
            return

        x = command_subjects[subject_index].item_id
        if (3 < x < 9) or x == 19:
            print("don't drop *treasures*!")
        elif self.current_position == 19 and subject_index == 19:
            wrap_string('as the penny sinks below the surface of the pool, a fleeting image of')
            print('a chapel with dancers appears.')
            rooms[21].moves[MOVE_EAST] = 22
            items[12].location = -2
        elif self.current_position == 22 and subject_index == 20:
            wrap_string('even before it hits the ground, the cross fades away!')
            print('the tablet has disintegrated.')
            print('you hear music from the organ.')
            self.flags["organ_playing"] = True
            items[11].location = -2
            rooms[22].text = 'chapel'
            items[24].text = 'closed organ playing music in the corner'
        else:
            items[command_subjects[subject_index].item_id].location = self.current_position
            print('ok')

    # say
    def say_command(self, subject_index, word):
        # global current_position, ol, rooms, snake_charmed_flag, portal_visible_flag
        if subject_index == 0:
            print('say what???')
        elif subject_index == 14:
            self.say_ritnew()
        elif subject_index == 15:
            self.say_victory()
        elif subject_index > 28:
            print("a hollow voice says, 'wrong adventure'.")
        else:
            print('okay, "', word, '".')
            delay()
            print('nothing happens.')

    def say_victory(self):
        global items, rooms
        if self.current_position != 8 or self.flags["portal_visible"]:
            print('nothing happens.')
        else:
            print('a portal has opened in the north wall!!')
            self.flags["portal_visible"] = True
            rooms[8].moves[MOVE_NORTH] = 17
            items[18].location = 8

    def say_ritnew(self):
        global items
        if self.current_position != 4 or self.flags["snake_charmed"]:
            print('nothing happens.')
        else:
            wrap_string('the snake is charmed by the very utterance of your words.')
            self.flags["snake_charmed"] = True
            items[2].location = -2
            items[3].location = 4

    # pour
    def pour_command(self, subject_index, subject):
        _ = subject
        global items
        if subject_index != 4:
            print("i wouldn't know how.")
        elif items[1].location != -1 and items[1].location != self.current_position:
            error_not_here()
        elif not self.flags["bucket_full"]:
            print('the bucket is already empty')
        elif self.current_position == 19:
            print('ok')
        elif self.current_position != 10 or not self.flags["fire_burning"]:
            print('the water disappears quickly.')
            self.flags["bucket_full"] = False
        else:
            print('congratulations! you have vanquished')
            print('the flames!')
            self.flags["fire_burning"] = False
            self.flags["bucket_full"] = False
            self.describe_current_position()

    # fill
    def fill_command(self, subject_index, subject):
        _ = subject
        global command_subjects
        if subject_index == 0:
            error_unknown_object('what?')
        elif command_subjects[subject_index].item_id == -1:
            print("that wouldn't hold anything.")
        elif get_item_location(subject_index) != self.current_position and get_item_location(subject_index) != -1:
            error_not_here()
        elif subject_index != 4:
            print("that wouldn't hold anything.")
        elif self.flags["bucket_full"]:
            print("it's already full.")
        elif self.current_position == 25 and self.flags["pool_flooded"]:
            print("i'd rather stay away from the mercury.")
        elif self.current_position != 23 and self.current_position != 19:
            print("i don't see any water here.")
        else:
            print('your bucket is now full.')
            self.flags["bucket_full"] = True

    # unlock object
    def unlock_command(self, subject_index, subject):
        _ = subject
        global items
        if subject_index == 0:
            error_unknown_object('what?')
        elif subject_index != 12 and subject_index != 27:
            print("i wouldn't know how to unlock one.")
        elif self.current_position != 0 and self.current_position != 5 and self.current_position != 6:
            error_not_here()
        elif self.current_position == 0 and subject_index == 12:
            self.unlock_front_door()
        elif self.current_position == 5 and subject_index == 27:
            self.unlock_vault()
        elif self.current_position != 6 or subject_index != 12 or items[16].location != -2:
            error_not_here()
        else:
            print('the trapdoor has no lock')

    def unlock_vault(self):
        global rooms
        if self.flags["vault_open"]:
            print("it's already open.")
        elif not self.flags["found_vault"]:
            error_not_here()
        elif not self.flags["know_combination"]:
            print('i don''t know the combination.')
        else:
            print("ok, let's see.  12..35..6..")
            print('<click!> the door swings open.')
            self.flags["vault_open"] = True
            rooms[5].moves[MOVE_EAST] = 46
            self.describe_current_position()

    def unlock_front_door(self):
        global items
        if self.flags["dungeon_unlocked"]:
            print("it's already unlocked.")
        elif items[20].location != -1:
            print('i need a key.')
        else:
            print('the door easily unlocks and swings open.')
            self.flags["dungeon_unlocked"] = True
            self.describe_current_position()

    # look
    def look_command(self, subject_index, subject):
        _, _ = subject_index, subject
        self.describe_current_position()

    # go
    def go_command(self, subject_index, subject):
        _ = subject
        global items
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
            print('the pool is full of mercury!')
        elif subject_index == 28:
            self.current_position = 48
        elif self.current_position == 27:
            self.current_position = 2
            self.describe_current_position()
        elif items[9].location == -1:
            print('the suits of armor try to stop you,')
            print('but you fight them off with your sword.')
            self.current_position = 27
            self.describe_current_position()
        else:
            wrap_string('the suits of armor prevent you from going up!')

    # north
    def north_command(self, subject_index, subject):
        _, _ = subject_index, subject
        global rooms
        if self.current_position == 0 and not self.flags["dungeon_unlocked"]:
            print('the door is locked shut.')
            return
        elif rooms[self.current_position].moves[MOVE_NORTH] == 0:
            error_no_path()
            return
        elif self.current_position == 0:
            print('the door slams shut behind you!')
        self.current_position = rooms[self.current_position].moves[MOVE_NORTH]
        self.describe_current_position()

    # south
    def south_command(self, subject_index, subject):
        _, _ = subject_index, subject
        global rooms
        if self.current_position == 10 and self.flags["fire_burning"]:
            print('you have burnt to a crisp!')
            self.flags["game_over"] = True
            self.final_stats()
        elif rooms[self.current_position].moves[MOVE_SOUTH] == 0:
            error_no_path()
        else:
            self.current_position = rooms[self.current_position].moves[MOVE_SOUTH]
            self.describe_current_position()

    # east
    def east_command(self, subject_index, subject):
        _, _ = subject_index, subject
        global rooms
        if self.current_position == 4 and not self.flags["snake_charmed"] and not self.flags["angry_snake"]:
            print('the snake is about to attack!')
            self.flags["angry_snake"] = True
        elif self.current_position == 4 and not self.flags["snake_charmed"]:
            print('the snake bites you!')
            print('you are dead.')
            self.flags["game_over"] = True
            self.final_stats()
        elif rooms[self.current_position].moves[MOVE_EAST] == 0:
            error_no_path()
        else:
            self.current_position = rooms[self.current_position].moves[MOVE_EAST]
            self.describe_current_position()

    # west
    def west_command(self, subject_index, subject):
        _, _ = subject_index, subject
        global rooms
        if rooms[self.current_position].moves[MOVE_WEST] == 0:
            error_no_path()
        else:
            self.current_position = rooms[self.current_position].moves[MOVE_WEST]
            self.describe_current_position()

    # score
    def score_command(self, subject_index, subject):
        _, _ = subject_index, subject
        print('if you were to quit now,')
        print('you would have a score of')
        print(self.gathered_treasures * 20, 'points.')
        print('(100 possible)')
        while not self.flags["game_over"]:
            print('do you indeed wish to quit now? ')
            input_str = get_input()
            if input_str[0].lower() == 'y':
                self.flags["game_over"] = True
                self.final_stats()
            elif input_str[0].lower() == 'n':
                print('ok')
                print()
                break

    # turn
    def turn_command(self, subject_index, subject):
        _ = subject
        global items
        if subject_index != 7:
            print("i don't know how to turn such a thing.")
            self.describe_current_position()
        elif self.current_position != 26:
            error_not_here()
        else:
            wrap_string('with much effort, you turn the valve 5 times.  you hear the sound of liquid')
            print('flowing through the pipes.')
            self.flags["pool_flooded"] = not self.flags["pool_flooded"]
            if not self.flags["pool_flooded"] and items[7].location == -3:
                items[7].location = 25
            elif self.flags["pool_flooded"] and items[7].location == 25:
                items[7].location = -3

    # jump
    def jump_command(self, subject_index, subject):
        _, _ = subject_index, subject
        global items
        if self.current_position != 27 and self.current_position != 29 and self.current_position != 32:
            print("there's nowhere to jump.")
        else:
            print('you jump..')
            if self.current_position == 27:
                self.jump_down_stairs()
            elif items[14].location == -1:
                print('there is no way to open the parachute!')
            elif items[27].location == -1:
                print('you yank the ripcord and the')
                print("'chute comes billowing out.")
                if self.current_position == 32:
                    self.current_position = 40
                    self.describe_current_position()
                else:
                    print('you land safely')
                    print('congratulations on escaping!')
                    self.flags["escaped"] = True
                    self.final_stats()
            print('you hit the ground.')
            print("you have broken your neck!")
            print("you are dead.")
            self.flags["game_over"] = True
            self.final_stats()

    def jump_down_stairs(self):
        if self.flags["jump_warning"]:
            print("now you've done it.  you ignored")
            print("my warning, and as a result")
            print("you have broken your neck!")
            print("you are dead.")
            self.flags["game_over"] = True
            self.final_stats()
        else:
            print('you have landed down-stairs,')
            print('and narrowly escaped serious')
            print("injury.  please don't try it again.")
            self.flags["jump_warning"] = True
            self.current_position = 2
            self.describe_current_position()

    # swim
    def swim_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position != 19 and self.current_position != 25:
            print("there's nothing here to swim in!")
        elif self.current_position == 19:
            print('the water is only a few inches deep.')
        elif self.flags["pool_flooded"]:
            print("in mercury?  no way!")
        else:
            print('the pool is empty.')

    # fix
    def fix_command(self, subject_index, subject):
        _ = subject
        global items, command_subjects
        if subject_index == 0:
            error_unknown_object('what')
        elif subject_index == 7:
            print("i ain't no plumber!")
        elif subject_index != 17:
            print("i wouldn't know how.")
        elif get_item_location(subject_index) != self.current_position and get_item_location(subject_index) != -1:
            error_not_here()
        elif items[14].location == -2:
            print("it's already fixed.")
        elif items[17].location != -1:
            print("i'll need a ripcord.")
        else:
            print("i'm no expert, but i think it'll work.")
            items[27].location = items[14].location
            items[14].location = -2
            command_subjects[17].item_id = 27
            items[17].location = 0

    def describe_current_position(self):
        global rooms, items
        wrap_string(f'you are in the {rooms[self.current_position].text}')
        for x in range(1, len(items)):
            if items[x].location == self.current_position:
                wrap_string(f'there is a {items[x].text} here')
            if x == 1 and self.flags["bucket_full"] and items[1].location == self.current_position:
                print("the bucket is full of water")
        if self.current_position == 25:
            if self.flags["pool_flooded"]:
                print('the pool is full of liquid mercury')
            else:
                print("the pool's empty")
                if items[7].location == 48:
                    print('i see something shiny in the pool!')
        if self.current_position == 10 and self.flags["fire_burning"]:
            print('there is a hot fire on the south wall!')
            print("if I go that way I'll burn to death!")
        if self.current_position == 16:
            wrap_string("a rich, full voice says, 'ritnew is a charming word'.")
        if self.current_position == 26:
            print('there is a valve on one of the pipes.')
        if self.current_position == 23:
            print('there is a leaky faucet nearby.')
        if self.current_position == 10 and not self.flags["fire_burning"]:
            print('there is evidence of a recent fire here.')
        if self.current_position == 5 and self.flags["found_vault"]:
            print('there is a vault in the east wall.')
        if self.current_position == 5 and self.flags["vault_open"]:
            print('the vault is open')
        if self.current_position == 0 and self.flags["dungeon_unlocked"]:
            print('an open door leads north.')
        if self.current_position != 48:
            print('obvious exits:')
            if rooms[self.current_position].moves[MOVE_NORTH] > 0:
                print('n ', end='')
            if rooms[self.current_position].moves[MOVE_SOUTH] > 0:
                print('s ', end='')
            if rooms[self.current_position].moves[MOVE_EAST] > 0:
                print('e ', end='')
            if rooms[self.current_position].moves[MOVE_WEST] > 0:
                print('w ', end='')
            print('')

    def final_stats(self):
        print('you accumulated', self.gathered_treasures, 'treasures,')
        print('for a score of', self.gathered_treasures * 20, 'points.')
        print('(100 possible)')
        if not self.flags["escaped"]:
            print('however, you did not escape.')
        print('this puts you in a class of:')
        if self.flags["escaped"]:
            self.gathered_treasures += 1
        if self.gathered_treasures == 0:
            print('<beginner adventurer>')
        elif self.gathered_treasures == 1:
            print('<amateur adventurer>')
        elif self.gathered_treasures == 2:
            print('<journeyman adventurer>')
        elif self.gathered_treasures == 3:
            print('<experienced adventurer>')
        elif self.gathered_treasures == 4:
            print('<professional adventurer>')
        elif self.gathered_treasures == 5:
            print('<master adventurer>')
        else:
            print('<grandmaster adventurer>')
        if self.gathered_treasures < 6:
            print('better luck next time!')


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


def wrap_string(long_string):
    global text_wrap_width
    if len(long_string) < text_wrap_width:
        print(long_string)
    else:
        last_space_index = long_string.rfind(' ', 0, text_wrap_width)
        print(long_string[:last_space_index])
        print(long_string[last_space_index + 1:])


def get_input():
    global prompt
    return read_line.readline(prompt)
