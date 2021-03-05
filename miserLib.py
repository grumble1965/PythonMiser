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


# UI base class configuration
class IUserInterface:
    text_wrap_width = 80
    read_line = None
    prompt = None

    def mp(self, *args, sep=' ', end='\n'):
        raise NotImplementedError

    def wrap_print(self, long_string):
        raise NotImplementedError

    def clear_screen(self):
        raise NotImplementedError

    def get_input(self):
        raise NotImplementedError

    def wait_for_keypress(self):
        raise NotImplementedError

    def delay(self):
        raise NotImplementedError


class WindowsConsoleUserInterface(IUserInterface):
    text_wrap_width = 80
    read_line = pyreadline.Readline()
    prompt = "> "

    def mp(self, *args, sep=' ', end='\n'):
        if len(args) == 0:
            print(end=end)
        else:
            for arg in args:
                print(arg, end=sep)
            print(end=end)

    def wrap_print(self, long_string):
        if len(long_string) < self.text_wrap_width:
            self.mp(long_string)
        else:
            last_space_index = long_string.rfind(' ', 0, self.text_wrap_width)
            self.mp(long_string[:last_space_index])
            self.mp(long_string[last_space_index + 1:])

    def clear_screen(self):
        self.read_line.console.home()
        self.read_line.console.clear_to_end_of_window()

    def get_input(self):
        return self.read_line.readline(self.prompt)

    def wait_for_keypress(self):
        _ = self.read_line.readline()

    def delay(self):
        pass


def welcome_banner(ui):
    ui.mp(f'{PROGRAM_NAME:>12} by m.j. lansing')
    ui.mp(f'   cursor # {CURSOR_ISSUE}  copyright (c) 1981')
    ui.mp('*' * 40)
    ui.mp("explore the miser's house   (needs 16k)")
    ui.mp('\n\n\npress return to begin')
    ui.wait_for_keypress()
    ui.mp('\n\none moment please...')


#
# Class for the overall Miser game
#
class Miser:
    def __init__(self, ui=WindowsConsoleUserInterface()):
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

        global help_strings
        help_strings = ['what?', "i don't understand that"]

        self.current_position = Rooms.FRONT_PORCH
        self.gathered_treasures = 0

        self.rooms = []
        self.verbs = []
        self.subjects = []
        self.items = []

        self.initialize_rooms()
        self.initialize_verbs()
        self.initialize_subjects()
        self.initialize_items()

    def initialize_items(self):
        item_data = [
            ('--unused--', -999),
            ('plastic bucket', Rooms.PUMP_HOUSE), ('vicious snake', Rooms.CONSERVATORY), ('charmed snake', -2),
            ('*golden leaf*', Rooms.HEDGE_MAZE5), ('*bulging moneybag*', Rooms.VAULT), ('>$<', -2),
            ('*diamond ring*', Rooms.BOTTOM_OF_POOL), ('*rare painting*', Rooms.SOUTH_END_EAST_HALLWAY),
            ('sword', Rooms.CHINESE_ROOM), ('mat', Rooms.FRONT_PORCH), ('rusty cross', Rooms.BACK_YARD),
            ('penny', Rooms.WEST_BEDROOM), ('piece of paper', Rooms.MASTER_BEDROOM),
            ('parachute with no ripcord', Rooms.CLOSET), ('oriental rug', Rooms.PARLOR),
            ("trapdoor marked 'danger'", -2), ('parachute ripcord', -2), ('portal in north wall', -2),
            ('pair of *ruby slippers*', -2), ('brass door key', -2),
            ('majestic staircase leading up', Rooms.GREEN_ROOM),
            ('majestic staircase leading down', Rooms.MIDDLE_WESTERN_HALLWAY), ('battered book', Rooms.LIBRARY),
            ('organ in the corner', Rooms.BALLROOM), ('open organ in the corner', -2),
            ('cabinet on rollers against one wall over', Rooms.REDWALL_ROOM), ('repaired parachute', -2),
            ("sign saying 'drop coins for luck'", Rooms.PORTICO)
        ]
        temp_list = []
        for (xx, yy) in item_data:
            temp_list.append(ItemClass(xx, yy))
        self.items = temp_list

    def initialize_subjects(self):
        command_subject_data = [
            ('--unused--', -999),
            ('ripc', Items.RIPCORD), ('mat', Items.MAT), ('pape', Items.PAPER),
            ('buck', Items.BUCKET), ('swor', Items.SWORD), ('key', Items.KEY),
            ('valv', Items.UNMOVEABLE), ('ladd', Items.UNMOVEABLE), ('slip', Items.SLIPPERS),
            ('rug', Items.RUG), ('book', Items.BOOK), ('door', Items.UNMOVEABLE),
            ('cabi', Items.UNMOVEABLE), ('ritn', Items.UNMOVEABLE), ('vict', Items.UNMOVEABLE),
            ('orga', Items.UNMOVEABLE), ('para', Items.BROKEN_PARACHUTE), ('stai', Items.UNMOVEABLE),
            ('penn', Items.PENNY), ('cros', Items.CROSS), ('leaf', Items.LEAF), ('bag', Items.MONEYBAGS),
            ('>$<', -1), ('>$<', -1), ('ring', Items.RING), ('pain', Items.PAINTING),
            ('vaul', Items.UNMOVEABLE), ('pool', Items.UNMOVEABLE), ('xyzz', Items.UNMOVEABLE),
            ('plug', Items.UNMOVEABLE)
        ]
        temp_list = []
        for (xx, yy) in command_subject_data:
            co = CommandSubjectClass(xx, yy)
            temp_list.append(co)
        self.subjects = temp_list

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
            ([1, 0, 0, 0], 'front porch'),                                                 # 0
            ([2, 0, 0, 12], 'foyer to a large house.  dust is everywhere'),                # 1
            ([3, 1, 0, 0], 'great hall.  suits of armor line the walls'),                  # 2
            ([0, 2, 4, 16], 'breakfast room.  it is bright and cheery'),                   # 3
            ([0, 5, 7, 3], 'conservatory.  through a window you see a hedge-maze'),        # 4
            ([4, 6, 0, 0], 'red-walled room'),                                             # 5
            ([5, 0, 10, 0], 'formal parlor'),                                              # 6
            ([0, 0, 8, 4], 'green drawing room'),                                          # 7
            ([0, 9, 0, 7], 'trophy room.  animal heads line the walls'),                   # 8
            ([8, 0, 0, 10], 'den'),                                                        # 9
            ([0, 11, 9, 6], 'blue drawing room'),                                          # 10
            ([10, 0, 0, 0], 'library.  empty shelves line walls'),                         # 11
            ([0, 0, 1, 13], 'dining room'),                                                # 12
            ([15, 0, 12, 0], 'chinese room'),                                              # 13
            ([0, 0, 0, 0], '$'),                                                           # 14
            ([23, 13, 16, 0], 'kitchen.  it is bare'),                                     # 15
            ([0, 0, 3, 15], 'pantry.  dust covers the mahogany shelves'),                  # 16
            ([0, 8, 0, 18], 'game room'),                                                  # 17
            ([21, 0, 17, 19], 'smoking room.  the air is stale in here'),                  # 18
            ([21, 0, 18, 20], 'portico.  a murky pool glimmers on the south side'),        # 19
            ([21, 21, 19, 19], 'hall of mirrors - a good place to reflect'),               # 20
            ([0, 19, 0, 20], 'ballroom.  it has a beautiful wood dance floor'),            # 21
            ([0, 0, 0, 21], "chapel.  a tablet says 'drop a religious item or die!!'"),    # 22
            ([24, 15, 40, 25], 'back yard'),                                               # 23
            ([24, 23, 24, 24], 'forest'),                                                  # 24
            ([26, 0, 23, 0], 'pool area.  there is a large swimming pool here'),           # 25
            ([0, 25, 0, 0], 'pump house.  there is pool machinery installed here'),        # 26
            ([35, 0, 31, 28], 'middle of the western hallway'),                            # 27
            ([0, 0, 27, 0], 'west bedroom'),                                               # 28
            ([39, 0, 0, 0], 'front balcony.  there is a large road below'),                # 29
            ([0, 0, 0, 0], '$'),                                                           # 30
            ([0, 0, 38, 27], 'master bedroom.  there''s a huge four-poster bed'),          # 31
            ([0, 36, 0, 0], 'rear balcony.  below you see a hedge maze'),                  # 32
            ([34, 0, 0, 38], 'east bedroom'),                                              # 33
            ([0, 33, 0, 0], 'closet'),                                                     # 34
            ([0, 27, 36, 0], 'junction of the west hallway and the north-south hallway'),  # 35
            ([32, 0, 37, 35], 'center of the north-south hallway'),                        # 36
            ([0, 38, 0, 36], 'junction of the east hallway and the north-south hallway'),  # 37
            ([37, 39, 33, 31], 'middle of the east hallway'),                              # 38
            ([38, 29, 0, 0], 'south end of east hallway'),                                 # 39
            ([0, 42, 0, 41], 'hedge maze'),                                                # 40
            ([44, 42, 0, 0], 'hedge maze'),                                                # 41
            ([41, 44, 43, 0], 'hedge maze'),                                               # 42
            ([41, 23, 0, 0], 'hedge maze'),                                                # 43
            ([0, 42, 0, 45], 'hedge maze'),                                                # 44
            ([0, 0, 44, 0], 'hedge maze'),                                                 # 45
            ([0, 0, 0, 5], 'walk-in vault'),                                               # 46
            ([0, 40, 0, 0], 'dungeon.  there is light above and to the south'),            # 47
            ([0, 0, 0, 0], 'bottom of the swimming pool.  a ladder leads up and out')      # 48
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
            input_str = self.ui.get_input()
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
            self.error_unknown_object(command_verb)
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
                self.error_unknown_object(subject)
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
            self.error_unknown_object('what?')
        elif self.subjects[subject_index].item_id == Items.UNMOVEABLE:
            self.ui.mp('i am unable to do that.')
        elif self.get_item_location(subject_index) == -1:
            self.ui.mp("you're already carrying it")
        elif self.get_item_location(subject_index) != self.current_position:
            self.error_not_here()
        else:
            self.items[self.subjects[subject_index].item_id].location = -1
            self.ui.mp('ok')
            if (Items.CHARMED_SNAKE < self.subjects[subject_index].item_id < Items.SWORD) or self.subjects[subject_index].item_id == Items.SLIPPERS:
                self.ui.mp('you got a treasure!')
                self.gathered_treasures += 1
            if subject_index == Subjects.MAT and self.items[Items.KEY].location == -2:
                self.ui.mp('you find a door key!')
                self.items[Items.KEY].location = Rooms.FRONT_PORCH

    # move, slide, push
    def move_slide_push_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            self.error_unknown_object('move what?')
        elif subject_index == Subjects.CABINET and self.current_position == Rooms.REDWALL_ROOM and self.rooms[Rooms.REDWALL_ROOM].moves[Move.EAST] == 0:
            self.ui.mp('behind the cabinet is a vault!')
            self.flags["found_vault"] = True
            self.describe_current_position()
        elif self.subjects[subject_index].item_id == Items.UNMOVEABLE:
            self.ui.mp('that item stays put.')
        elif self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            self.error_not_here()
        elif subject_index == Subjects.MAT and self.items[Items.KEY].location == -2:
            self.ui.mp('you find a door key!')
            self.items[Items.KEY].location = Rooms.FRONT_PORCH
        elif subject_index == Subjects.RUG and self.items[Items.TRAPDOOR].location == -2:
            self.ui.mp('you find a trap door!')
            self.items[Items.TRAPDOOR].location = Rooms.PARLOR
            self.describe_current_position()
        else:
            self.ui.mp('moving it reveals nothing.')

    # open
    def open_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            self.error_unknown_object('open what?')
        elif subject_index == Subjects.BOOK:
            self.open_book(subject_index)
        elif subject_index == Subjects.VALVE:
            self.ui.mp('try turning it.')
        elif subject_index == Subjects.DOOR:
            self.open_door()
        elif subject_index == Subjects.CABINET:
            self.open_cabinet()
        elif subject_index == Subjects.MONEYBAG:
            self.open_bag(subject_index)
        elif subject_index == Subjects.VAULT:
            self.open_vault()
        elif subject_index == Subjects.ORGAN:
            self.open_organ()
        else:
            self.ui.mp("i don't know how to open that.")

    def open_door(self):
        if self.current_position == Rooms.FRONT_PORCH and not self.flags["dungeon_unlocked"]:
            self.ui.mp('sorry, the door is locked.')
        elif self.current_position == Rooms.FRONT_PORCH and self.flags["dungeon_unlocked"]:
            self.ui.mp("it's already open.")
        elif self.current_position != Rooms.PARLOR:
            self.error_not_here()
        else:
            self.ui.wrap_print('you open the door. you lean over to peer in, and you fall in!')
            self.current_position = Rooms.DUNGEON
            self.describe_current_position()

    def open_cabinet(self):
        if self.items[Items.CABINET].location != self.current_position:
            self.error_not_here()
        else:
            self.ui.mp('the cabinet is empty and dusty.')
            self.ui.wrap_print("scribbled in the dust on one shelf are the words, 'behind me'.")

    def open_bag(self, subject_index):
        if self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            self.error_not_here()
        else:
            self.ui.mp('the bag is knotted securely.')
            self.ui.mp("it won't open.")

    def open_vault(self):
        if self.current_position != Rooms.REDWALL_ROOM or not self.flags["found_vault"]:
            self.error_not_here()
        elif self.flags["vault_open"]:
            self.ui.mp("it's already open.")
        else:
            self.ui.mp("i can't, it's locked.")

    def open_organ(self):
        if self.current_position != Rooms.BALLROOM:
            self.error_not_here()
        elif not self.flags["organ_playing"]:
            self.ui.mp("it's stuck shut.")
        elif self.items[Items.CLOSED_ORGAN].location == -2:
            self.ui.mp("it's already open.")
        else:
            self.ui.mp('as you open it, several objects suddenly appear!')
            self.items[Items.CLOSED_ORGAN].location = -2
            self.items[Items.OPEN_ORGAN].location = Rooms.BALLROOM
            self.items[Items.SLIPPERS].location = Rooms.BALLROOM
            self.items[Items.RIPCORD].location = Rooms.BALLROOM
            self.describe_current_position()

    def open_book(self, subject_index):
        if self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            self.error_not_here()
        else:
            self.ui.wrap_print("scrawled in blood on the inside front cover is the message,")
            self.ui.mp("''victory' is a prize-winning word'.")

    # read
    def read_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            self.error_unknown_object('read what?')
        elif self.subjects[subject_index].item_id > Items.UNMOVEABLE \
                and self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            self.error_not_here()
        elif self.subjects[subject_index].item_id == Items.UNMOVEABLE:
            self.ui.mp("there's nothing written on that.")
        elif subject_index != Subjects.PAPER and subject_index != Subjects.BOOK:
            self.ui.mp("there's nothing written on that.")
        elif subject_index == Subjects.BOOK:
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
            if x == Items.BUCKET and self.flags["bucket_full"] and self.items[Items.BUCKET].location == -1:
                self.ui.mp('  the bucket is full of water.')
            if x == Items.BROKEN_PARACHUTE and self.items[Items.BROKEN_PARACHUTE].location == -1:
                self.ui.mp('   (better fix it)')
        if not carrying_something:
            self.ui.mp('nothing at all.')

    # quit
    def quit_command(self, subject_index, subject):
        _, _ = subject_index, subject
        self.ui.mp('do you indeed wish to quit now?')
        input_str = self.ui.get_input()
        if input_str[0].lower() != 'y':
            self.ui.mp('ok')
        else:
            self.ui.clear_screen()
            self.final_stats()
            self.flags["game_over"] = True

    # drop
    def drop_command(self, subject_index, subject):
        _ = subject
        if self.get_item_location(subject_index) != -1:
            self.ui.mp("you aren't carrying it!")
            return

        x = self.subjects[subject_index].item_id
        if (Items.CHARMED_SNAKE < x < Items.SWORD) or x == Items.SLIPPERS:
            self.ui.mp("don't drop *treasures*!")
        elif self.current_position == Rooms.PORTICO and subject_index == Subjects.PENNY:
            self.ui.wrap_print('as the penny sinks below the surface of the pool, a fleeting image of')
            self.ui.mp('a chapel with dancers appears.')
            self.rooms[Rooms.BALLROOM].moves[Move.EAST] = Rooms.CHAPEL
            self.items[Items.PENNY].location = -2
        elif self.current_position == Rooms.CHAPEL and subject_index == Subjects.CROSS:
            self.ui.wrap_print('even before it hits the ground, the cross fades away!')
            self.ui.mp('the tablet has disintegrated.')
            self.ui.mp('you hear music from the organ.')
            self.flags["organ_playing"] = True
            self.items[Items.CROSS].location = -2
            self.rooms[Rooms.CHAPEL].text = 'chapel'
            self.items[Items.CLOSED_ORGAN].text = 'closed organ playing music in the corner'
        else:
            self.items[self.subjects[subject_index].item_id].location = self.current_position
            self.ui.mp('ok')

    # say
    def say_command(self, subject_index, word):
        if subject_index == 0:
            self.ui.mp('say what???')
        elif subject_index == Subjects.RITNEW:
            self.say_ritnew()
        elif subject_index == Subjects.VICTORY:
            self.say_victory()
        elif subject_index > Subjects.POOL:
            self.ui.mp("a hollow voice says, 'wrong adventure'.")
        else:
            self.ui.mp('okay, "', word, '".')
            self.ui.delay()
            self.ui.mp('nothing happens.')

    def say_victory(self):
        if self.current_position != Rooms.TROPHY_ROOM or self.flags["portal_visible"]:
            self.ui.mp('nothing happens.')
        else:
            self.ui.mp('a portal has opened in the north wall!!')
            self.flags["portal_visible"] = True
            self.rooms[Rooms.TROPHY_ROOM].moves[Move.NORTH] = Rooms.GAME_ROOM
            self.items[Items.PORTAL].location = Rooms.TROPHY_ROOM

    def say_ritnew(self):
        if self.current_position != Rooms.CONSERVATORY or self.flags["snake_charmed"]:
            self.ui.mp('nothing happens.')
        else:
            self.ui.wrap_print('the snake is charmed by the very utterance of your words.')
            self.flags["snake_charmed"] = True
            self.items[Items.VICIOUS_SNAKE].location = -2
            self.items[Items.CHARMED_SNAKE].location = Rooms.CONSERVATORY

    # pour
    def pour_command(self, subject_index, subject):
        _ = subject
        if subject_index != Subjects.BUCKET:
            self.ui.mp("i wouldn't know how.")
        elif self.items[Items.BUCKET].location != -1 and self.items[Items.BUCKET].location != self.current_position:
            self.error_not_here()
        elif not self.flags["bucket_full"]:
            self.ui.mp('the bucket is already empty')
        elif self.current_position == Rooms.PORTICO:
            self.ui.mp('ok')
        elif self.current_position != Rooms.BLUE_ROOM or not self.flags["fire_burning"]:
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
            self.error_unknown_object('what?')
        elif self.subjects[subject_index].item_id == Items.UNMOVEABLE:
            self.ui.mp("that wouldn't hold anything.")
        elif self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            self.error_not_here()
        elif subject_index != Subjects.BUCKET:
            self.ui.mp("that wouldn't hold anything.")
        elif self.flags["bucket_full"]:
            self.ui.mp("it's already full.")
        elif self.current_position == Rooms.POOL_AREA and self.flags["pool_flooded"]:
            self.ui.mp("i'd rather stay away from the mercury.")
        elif self.current_position != Rooms.BACK_YARD and self.current_position != Rooms.PORTICO:
            self.ui.mp("i don't see any water here.")
        else:
            self.ui.mp('your bucket is now full.')
            self.flags["bucket_full"] = True

    # unlock object
    def unlock_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            self.error_unknown_object('what?')
        elif subject_index != Subjects.DOOR and subject_index != Subjects.VAULT:
            self.ui.mp("i wouldn't know how to unlock one.")
        elif self.current_position != Rooms.FRONT_PORCH and self.current_position != Rooms.REDWALL_ROOM and self.current_position != Rooms.PARLOR:
            self.error_not_here()
        elif self.current_position == Rooms.FRONT_PORCH and subject_index == Subjects.DOOR:
            self.unlock_front_door()
        elif self.current_position == Rooms.REDWALL_ROOM and subject_index == Subjects.VAULT:
            self.unlock_vault()
        elif self.current_position != Rooms.PARLOR or subject_index != Subjects.DOOR or self.items[Items.TRAPDOOR].location != -2:
            self.error_not_here()
        else:
            self.ui.mp('the trapdoor has no lock')

    def unlock_vault(self):
        if self.flags["vault_open"]:
            self.ui.mp("it's already open.")
        elif not self.flags["found_vault"]:
            self.error_not_here()
        elif not self.flags["know_combination"]:
            self.ui.mp('i don''t know the combination.')
        else:
            self.ui.mp("ok, let's see.  12..35..6..")
            self.ui.mp('<click!> the door swings open.')
            self.flags["vault_open"] = True
            self.rooms[Rooms.REDWALL_ROOM].moves[Move.EAST] = Rooms.VAULT
            self.describe_current_position()

    def unlock_front_door(self):
        if self.flags["dungeon_unlocked"]:
            self.ui.mp("it's already unlocked.")
        elif self.items[Items.KEY].location != -1:
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
        if subject_index != Subjects.LADDER and subject_index != Subjects.STAIRS and subject_index != Subjects.POOL:
            self.error_unknown_object('what?')
        elif subject_index == Subjects.LADDER and self.current_position != Rooms.BOTTOM_OF_POOL:
            self.error_not_here()
        elif subject_index == Subjects.STAIRS and self.current_position != Rooms.GREAT_HALL and self.current_position != Rooms.MIDDLE_WESTERN_HALLWAY:
            self.error_not_here()
        elif subject_index == Subjects.POOL and self.current_position != Rooms.POOL_AREA:
            self.error_not_here()
        elif subject_index == Subjects.LADDER:
            self.current_position = Rooms.POOL_AREA
            self.describe_current_position()
        elif subject_index == Subjects.POOL and self.flags["pool_flooded"]:
            self.ui.mp('the pool is full of mercury!')
        elif subject_index == Subjects.POOL:
            self.current_position = Rooms.BOTTOM_OF_POOL
        elif self.current_position == Rooms.MIDDLE_WESTERN_HALLWAY:
            self.current_position = Rooms.GREAT_HALL
            self.describe_current_position()
        elif self.items[Items.SWORD].location == -1:
            self.ui.mp('the suits of armor try to stop you,')
            self.ui.mp('but you fight them off with your sword.')
            self.current_position = Rooms.MIDDLE_WESTERN_HALLWAY
            self.describe_current_position()
        else:
            self.ui.wrap_print('the suits of armor prevent you from going up!')

    # north
    def north_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position == Rooms.FRONT_PORCH and not self.flags["dungeon_unlocked"]:
            self.ui.mp('the door is locked shut.')
            return
        elif self.rooms[self.current_position].moves[Move.NORTH] == 0:
            self.error_no_path()
            return
        elif self.current_position == 0:
            self.ui.mp('the door slams shut behind you!')
        self.current_position = self.rooms[self.current_position].moves[Move.NORTH]
        self.describe_current_position()

    # south
    def south_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position == Rooms.BLUE_ROOM and self.flags["fire_burning"]:
            self.ui.mp('you have burnt to a crisp!')
            self.flags["game_over"] = True
            self.final_stats()
        elif self.rooms[self.current_position].moves[Move.SOUTH] == 0:
            self.error_no_path()
        else:
            self.current_position = self.rooms[self.current_position].moves[Move.SOUTH]
            self.describe_current_position()

    # east
    def east_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position == Rooms.CONSERVATORY and not self.flags["snake_charmed"] and not self.flags["angry_snake"]:
            self.ui.mp('the snake is about to attack!')
            self.flags["angry_snake"] = True
        elif self.current_position == Rooms.CONSERVATORY and not self.flags["snake_charmed"]:
            self.ui.mp('the snake bites you!')
            self.ui.mp('you are dead.')
            self.flags["game_over"] = True
            self.final_stats()
        elif self.rooms[self.current_position].moves[Move.EAST] == 0:
            self.error_no_path()
        else:
            self.current_position = self.rooms[self.current_position].moves[Move.EAST]
            self.describe_current_position()

    # west
    def west_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.rooms[self.current_position].moves[Move.WEST] == 0:
            self.error_no_path()
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
            input_str = self.ui.get_input()
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
        if subject_index != Subjects.VALVE:
            self.ui.mp("i don't know how to turn such a thing.")
            self.describe_current_position()
        elif self.current_position != Rooms.PUMP_HOUSE:
            self.error_not_here()
        else:
            self.ui.wrap_print('with much effort, you turn the valve 5 times.  you hear the sound of liquid')
            self.ui.mp('flowing through the pipes.')
            self.flags["pool_flooded"] = not self.flags["pool_flooded"]
            if not self.flags["pool_flooded"] and self.items[Items.RING].location == -3:
                self.items[Items.RING].location = Rooms.POOL_AREA
            elif self.flags["pool_flooded"] and self.items[Items.RING].location == Rooms.POOL_AREA:
                self.items[Items.RING].location = -3

    # jump
    def jump_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position != Rooms.MIDDLE_WESTERN_HALLWAY and self.current_position != Rooms.FRONT_BALCONY and self.current_position != Rooms.REAR_BALCONY:
            self.ui.mp("there's nowhere to jump.")
        else:
            self.ui.mp('you jump..')
            if self.current_position == Rooms.MIDDLE_WESTERN_HALLWAY:
                self.jump_down_stairs()
            elif self.items[Items.BROKEN_PARACHUTE].location == -1:
                self.ui.mp('there is no way to open the parachute!')
            elif self.items[Items.REPAIRED_PARACHUTE].location == -1:
                self.ui.mp('you yank the ripcord and the')
                self.ui.mp("'chute comes billowing out.")
                if self.current_position == Rooms.REAR_BALCONY:
                    self.current_position = Rooms.HEDGE_MAZE0
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
            self.current_position = Rooms.GREAT_HALL
            self.describe_current_position()

    # swim
    def swim_command(self, subject_index, subject):
        _, _ = subject_index, subject
        if self.current_position != Rooms.PORTICO and self.current_position != Rooms.POOL_AREA:
            self.ui.mp("there's nothing here to swim in!")
        elif self.current_position == Rooms.PORTICO:
            self.ui.mp('the water is only a few inches deep.')
        elif self.flags["pool_flooded"]:
            self.ui.mp("in mercury?  no way!")
        else:
            self.ui.mp('the pool is empty.')

    # fix
    def fix_command(self, subject_index, subject):
        _ = subject
        if subject_index == 0:
            self.error_unknown_object('what')
        elif subject_index == Subjects.VALVE:
            self.ui.mp("i ain't no plumber!")
        elif subject_index != Subjects.PARACHUTE:
            self.ui.mp("i wouldn't know how.")
        elif self.get_item_location(subject_index) != self.current_position \
                and self.get_item_location(subject_index) != -1:
            self.error_not_here()
        elif self.items[Items.BROKEN_PARACHUTE].location == -2:
            self.ui.mp("it's already fixed.")
        elif self.items[Items.RIPCORD].location != -1:
            self.ui.mp("i'll need a ripcord.")
        else:
            self.ui.mp("i'm no expert, but i think it'll work.")
            self.items[Items.REPAIRED_PARACHUTE].location = self.items[Items.BROKEN_PARACHUTE].location
            self.items[Items.BROKEN_PARACHUTE].location = -2
            self.subjects[Subjects.PARACHUTE].item_id = Items.REPAIRED_PARACHUTE
            self.items[Items.RIPCORD].location = 0

    def describe_current_position(self):
        self.ui.wrap_print(f'you are in the {self.rooms[self.current_position].text}')
        for x in range(1, len(self.items)):
            if self.items[x].location == self.current_position:
                self.ui.wrap_print(f'there is a {self.items[x].text} here')
            if x == Items.BUCKET and self.flags["bucket_full"] and self.items[Items.BUCKET].location == self.current_position:
                self.ui.mp("the bucket is full of water")
        if self.current_position == Rooms.POOL_AREA:
            if self.flags["pool_flooded"]:
                self.ui.mp('the pool is full of liquid mercury')
            else:
                self.ui.mp("the pool's empty")
                if self.items[Items.RING].location == Rooms.BOTTOM_OF_POOL:
                    self.ui.mp('i see something shiny in the pool!')
        if self.current_position == Rooms.BLUE_ROOM and self.flags["fire_burning"]:
            self.ui.mp('there is a hot fire on the south wall!')
            self.ui.mp("if I go that way I'll burn to death!")
        if self.current_position == Rooms.PANTRY:
            self.ui.wrap_print("a rich, full voice says, 'ritnew is a charming word'.")
        if self.current_position == Rooms.PUMP_HOUSE:
            self.ui.mp('there is a valve on one of the pipes.')
        if self.current_position == Rooms.BACK_YARD:
            self.ui.mp('there is a leaky faucet nearby.')
        if self.current_position == Rooms.BLUE_ROOM and not self.flags["fire_burning"]:
            self.ui.mp('there is evidence of a recent fire here.')
        if self.current_position == Rooms.REDWALL_ROOM and self.flags["found_vault"]:
            self.ui.mp('there is a vault in the east wall.')
        if self.current_position == Rooms.REDWALL_ROOM and self.flags["vault_open"]:
            self.ui.mp('the vault is open')
        if self.current_position == Rooms.FRONT_PORCH and self.flags["dungeon_unlocked"]:
            self.ui.mp('an open door leads north.')
        if self.current_position != Rooms.BOTTOM_OF_POOL:
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

    def error_unknown_object(self, subject):
        global help_index
        self.ui.mp(f'{subject}?  {help_strings[help_index]}')
        help_index += 1
        if help_index >= len(help_strings):
            help_index = 0

    def error_not_here(self):
        self.ui.mp("i don't see it here")

    def error_no_path(self):
        self.ui.mp("it's impossible to go that way.")


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


#
# Enumeration to replace Item constants
#
class Items(IntEnum):
    BUCKET, VICIOUS_SNAKE, CHARMED_SNAKE, LEAF = 1, 2, 3, 4
    MONEYBAGS, RING, PAINTING = 5, 7, 8
    SWORD, MAT, CROSS, PENNY, PAPER = 9, 10, 11, 12, 13
    BROKEN_PARACHUTE, RUG, TRAPDOOR = 14, 15, 16
    RIPCORD, PORTAL, SLIPPERS = 17, 18, 19
    KEY, UP_STAIRCASE = 20, 21
    DOWN_STAIRCASE, BOOK, CLOSED_ORGAN = 22, 23, 24
    OPEN_ORGAN, CABINET = 25, 26
    REPAIRED_PARACHUTE, SIGN = 27, 28
    UNMOVEABLE = -1


class Rooms(IntEnum):
    FRONT_PORCH, FOYER, GREAT_HALL, BREAKFAST_ROOM, CONSERVATORY = 0, 1, 2, 3, 4
    REDWALL_ROOM, PARLOR, GREEN_ROOM, TROPHY_ROOM, DEN, BLUE_ROOM = 5, 6, 7, 8, 9, 10
    LIBRARY, DINING_ROOM, CHINESE_ROOM, KITCHEN, PANTRY = 11, 12, 13, 15, 16
    GAME_ROOM, SMOKING_ROOM, PORTICO, HALL_OF_MIRRORS, BALLROOM = 17, 18, 19, 20, 21
    CHAPEL, BACK_YARD, FOREST, POOL_AREA, PUMP_HOUSE = 22, 23, 24, 25, 26
    MIDDLE_WESTERN_HALLWAY, WEST_BEDROOM, FRONT_BALCONY = 27, 28, 29
    MASTER_BEDROOM, REAR_BALCONY, EAST_BEDROOM, CLOSET = 31, 32, 33, 34
    JUNCTION_WEST_HALLWAY, CENTER_NORTH_SOUTH_HALLWAY, JUNCTION_EAST_HALLWAY = 35, 36, 37
    MIDDLE_EAST_HALLWAY, SOUTH_END_EAST_HALLWAY = 38, 39
    HEDGE_MAZE0, HEDGE_MAZE1, HEDGE_MAZE2, HEDGE_MAZE3, HEDGE_MAZE4, HEDGE_MAZE5 = 40, 41, 42, 43, 44, 45
    VAULT, DUNGEON, BOTTOM_OF_POOL = 46, 47, 48


class Subjects(IntEnum):
    RIPCORD, MAT, PAPER = 1, 2, 3
    BUCKET, SWORD, KEY = 4, 5, 6
    VALVE, LADDER, SLIPPER = 7, 8, 9
    RUG, BOOK, DOOR = 10, 11, 12
    CABINET, RITNEW, VICTORY = 13, 14, 15
    ORGAN, PARACHUTE, STAIRS = 16, 17, 18
    PENNY, CROSS, LEAF, MONEYBAG = 19, 20, 21, 22
    RING, PAINTING = 25, 26
    VAULT, POOL, XYZZY, PLUGH = 27, 28, 29, 30
