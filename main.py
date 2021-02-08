# This is a Python port of the Miser's House BASIC adventure.
#
# BASIC original (c) 1981 M. J. Winter
#
# Python Version (c) 2021  Kelly M Hall
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#
# CC BY-NC-SA 3.0
import pyreadline.rlmain

read_line = pyreadline.Readline()
prompt = "> "


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


# useful functions
def clear_screen():
    read_line.console.home()
    read_line.console.clear_to_end_of_window()


def wait_for_keypress():
    _ = read_line.readline()


def delay():
    pass


# variables
program_name, cursor_issue = 'miser', '27'
text_wrap_width = 80
items = []
rooms = []
command_subjects = []
verbs = []
pool_flooded_flag = bucket_full_flag = fire_burning_flag = vault_open_flag = False
found_vault_flag = dungeon_unlocked_flag = know_combination_flag = False
gg_flag = escaped_flag = snake_charmed_flag = angry_snake_flag = jump_warning_flag = False
portal_visible_flag = False
gathered_treasures = 0
current_position = 0

# todo make help message class
help_strings, help_index = [], 0


def main():
    welcome_banner()
    initialize_data()
    clear_screen()
    describe_current_position()
    main_command_loop()


def get_item_location(x):
    global items, command_subjects
    return items[command_subjects[x].item_id].location


def initialize_data():
    # todo: get rid of magic numbers
    global rooms
    global items
    global verbs
    global command_subjects

    global pool_flooded_flag, fire_burning_flag
    pool_flooded_flag = fire_burning_flag = True

    global help_strings
    help_strings = ['what?', "i don't understand that"]

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

    verb_data = [
        ('--unused--', unused_command),
        ('get', get_take_command),
        ('take', get_take_command),
        ('move', move_slide_push_command),
        ('slid', move_slide_push_command),
        ('push', move_slide_push_command),
        ('open', open_command),
        ('read', read_command),
        ('inve', inventory_command),
        ('quit', quit_command),
        ('drop', drop_command),
        ('say', say_command),
        ('pour', pour_command),
        ('fill', fill_command),
        ('unlo', unlock_command),
        ('look', look_command),
        ('go', go_command),
        ('nort', north_command),
        ('n', north_command),
        ('sout', south_command),
        ('s', south_command),
        ('east', east_command),
        ('e', east_command),
        ('west', west_command),
        ('w', west_command),
        ('scor', score_command),
        ('turn', turn_command),
        ('jump', jump_command),
        ('swim', swim_command),
        ('i', inventory_command),
        ('fix', fix_command)
    ]
    temp_list = []
    for (xx, yy) in verb_data:
        temp_list.append(VerbClass(xx, yy))
    verbs = temp_list

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
        # print('xx = ', xx, 'yy = ', yy)
        temp_list.append(ItemClass(xx, yy))
    items = temp_list


def main_command_loop():
    global verbs, command_subjects
    while True:
        # read user input
        print()
        input_str = get_input()
        input_str.strip()
        parsed_words = input_str.split()
        if len(parsed_words) < 1 or len(parsed_words) > 2:
            print('please type a one or two word command')
            continue

        # parse into verb + subject, validate verb
        command_verb = parsed_words[0]
        subject = 'unassigned'
        if len(command_verb) > 4:
            command_verb = command_verb[0:4]
        verb_index = -1
        for x in range(1, len(verbs)):
            if command_verb == verbs[x].text:
                # print(f' command {verbs[x].text} {x}')
                verb_index = x
                break
        if verb_index == -1:
            error_unknown_object(command_verb)
            continue

        # validate object
        if len(parsed_words) == 1:
            subject_index = 0
        else:
            subject = parsed_words[1]
            if len(subject) > 4:
                subject = subject[0:4]
            subject_index = -1
            for x in range(1, len(command_subjects)):
                if subject == command_subjects[x].text:
                    subject_index = x
                    break
            if subject_index == -1:
                error_unknown_object(subject)
                continue

        # call verb handler
        verbs[verb_index].handler(subject_index, subject)


def unused_command(subject_index, subject):
    _, _ = subject_index, subject
    pass


# get, take object
def get_take_command(subject_index, subject):
    _ = subject
    global current_position, command_subjects, items, gathered_treasures
    if subject_index == 0:
        error_unknown_object('what?')
    elif command_subjects[subject_index].item_id == -1:
        print('i am unable to do that.')
    elif get_item_location(subject_index) == -1:
        print("you're already carrying it")
    elif get_item_location(subject_index) != current_position:
        error_not_here()
    else:
        items[command_subjects[subject_index].item_id].location = -1
        print('ok')

        # line 1030
        if (3 < command_subjects[subject_index].item_id < 9) or command_subjects[subject_index].item_id == 19:
            print('you got a treasure!')
            gathered_treasures += 1
        # line 1040
        if subject_index == 2 and items[20].location == -2:
            print('you find a door key!')
            items[20].location = 0


# move, slide, push
def move_slide_push_command(subject_index, subject):
    _ = subject
    global current_position, rooms, command_subjects, items, found_vault_flag
    if subject_index == 0:
        error_unknown_object('move what?')
    elif subject_index == 13 and current_position == 5 and rooms[5].moves[3] == 0:
        print('behind the cabinet is a vault!')
        found_vault_flag = True
        describe_current_position()
    elif command_subjects[subject_index].item_id == -1:
        print('that item stays put.')
    elif get_item_location(subject_index) != current_position and get_item_location(subject_index) != -1:
        error_not_here()
    elif subject_index == 2 and items[20].location == -2:
        # line 1040
        print('you find a door key!')
        items[20].location = 0
    elif subject_index == 10 and items[16].location == -2:
        print('you find a trap door!')
        items[16].location = 6
        describe_current_position()
    else:
        print('moving it reveals nothing.')


# open
# todo  fix this control flow
def open_command(subject_index, subject):
    _ = subject
    if subject_index == 0:
        error_unknown_object('open what?')
    elif subject_index != 11:
        line4030(subject_index)
    elif get_item_location(subject_index) != current_position and get_item_location(subject_index) != -1:
        line4030(subject_index)
    else:
        wrap_string("scrawled in blood on the inside front cover is the message,")
        print("''victory' is a prize-winning word'.")


def line4030(subject_index):
    global current_position, dungeon_unlocked_flag
    if subject_index == 7:
        print('try turning it.')
    elif subject_index != 12:
        line4120(subject_index)
    elif current_position == 0 and not dungeon_unlocked_flag:
        print('sorry, the door is locked.')
    elif current_position == 0 and dungeon_unlocked_flag:
        print("it's already open.")
    elif current_position != 6:
        error_not_here()
    else:
        wrap_string('you open the door. you lean over to peer in, and you fall in!')
        current_position = 47
        describe_current_position()


def line4120(subject_index):
    global current_position, items
    if subject_index != 13:
        line4160(subject_index)
    elif items[26].location != current_position:
        error_not_here()
    else:
        print('the cabinet is empty and dusty.')
        wrap_string("scribbled in the dust on one shelf are the words, 'behind me'.")


def line4160(subject_index):
    global current_position
    if subject_index != 22:
        line4190(subject_index)
    elif get_item_location(subject_index) != current_position and get_item_location(subject_index) != -1:
        error_not_here()
    else:
        print('the bag is knotted securely.')
        print("it won't open.")


def line4190(subject_index):
    global current_position, found_vault_flag, vault_open_flag
    if subject_index != 27:
        line4230(subject_index)
    elif current_position != 5 or not found_vault_flag:
        error_not_here()
    elif vault_open_flag:
        print("it's already open.")
    else:
        print("i can't, it's locked.")


def line4230(subject_index):
    global gg_flag, items
    if subject_index != 16:
        print("i don't know how to open that.")
    elif current_position != 21:
        error_not_here()
    elif not gg_flag:
        print("it's stuck shut.")
    elif items[24].location == -2:
        print("it's already open.")
    else:
        print('as you open it, several objects suddenly appear!')
        items[24].location = -2
        items[25].location = 21
        items[19].location = 21
        items[17].location = 21
        describe_current_position()


# read
def read_command(subject_index, subject):
    _ = subject
    global current_position, know_combination_flag
    if subject_index == 0:
        error_unknown_object('read what?')
    elif command_subjects[subject_index].item_id > -1 \
            and get_item_location(subject_index) != current_position \
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
        know_combination_flag = True


# inventory
def inventory_command(subject_index, subject):
    _, _ = subject_index, subject
    global items, bucket_full_flag
    print('you are carrying the following:')
    carrying_something = False
    for x in range(1, len(items)):
        if items[x].location == -1:
            print(items[x].text)
            carrying_something = True
        if x == 1 and bucket_full_flag and items[1].location == -1:
            print('  the bucket is full of water.')
        if x == 14 and items[14].location == -1:
            print('   (better fix it)')
    if not carrying_something:
        print('nothing at all.')


# quit
def quit_command(subject_index, subject):
    _, _ = subject_index, subject
    print('do you indeed wish to quit now?')
    input_str = get_input()
    if input_str[0].lower() != 'y':
        print('ok')
    else:
        clear_screen()
        final_stats()


def final_stats():
    global gathered_treasures, escaped_flag
    print('you accumulated', gathered_treasures, 'treasures,')
    print('for a score of', gathered_treasures * 20, 'points.')
    print('(100 possible)')
    if not escaped_flag:
        print('however, you did not escape.')
    print('this puts you in a class of:')
    if escaped_flag:
        gathered_treasures += 1
    if gathered_treasures == 0:
        print('<beginner adventurer>')
    elif gathered_treasures == 1:
        print('<amateur adventurer>')
    elif gathered_treasures == 2:
        print('<journeyman adventurer>')
    elif gathered_treasures == 3:
        print('<experienced adventurer>')
    elif gathered_treasures == 4:
        print('<professional adventurer>')
    elif gathered_treasures == 5:
        print('<master adventurer>')
    else:
        print('<grandmaster adventurer>')
    if gathered_treasures < 6:
        print('better luck next time!')
    exit(0)


# drop
def drop_command(subject_index, subject):
    _ = subject
    global current_position, items, command_subjects, rooms, gg_flag
    if get_item_location(subject_index) != -1:
        print("you aren't carrying it!")
        return

    x = command_subjects[subject_index].item_id
    if (3 < x < 9) or x == 19:
        print("don't drop *treasures*!")
    elif current_position == 19 and subject_index == 19:
        wrap_string('as the penny sinks below the surface of the pool, a fleeting image of')
        print('a chapel with dancers appears.')
        rooms[21].moves[2] = 22
        items[12].location = -2
    elif current_position == 22 and subject_index == 20:
        wrap_string('even before it hits the ground, the cross fades away!')
        print('the tablet has disintegrated.')
        print('you hear music from the organ.')
        gg_flag = True
        items[11].location = -2
        rooms[22].text = 'chapel'
        items[24].text = 'closed organ playing music in the corner'
    else:
        items[command_subjects[subject_index].item_id].location = current_position
        print('ok')


# say
def say_command(subject_index, word):
    # global current_position, ol, rooms, snake_charmed_flag, portal_visible_flag
    if subject_index == 0:
        print('say what???')
    elif subject_index == 14:
        say_ritnew()
    elif subject_index == 15:
        say_victory()
    elif subject_index > 28:
        print("a hollow voice says, 'wrong adventure'.")
    else:
        print('okay, "', word, '".')
        delay()
        print('nothing happens.')


def say_victory():
    global items, rooms, current_position, portal_visible_flag
    if current_position != 8 or portal_visible_flag:
        print('nothing happens.')
    else:
        print('a portal has opened in the north wall!!')
        portal_visible_flag = True
        rooms[8].moves[0] = 17
        items[18].location = 8


def say_ritnew():
    global current_position, items, snake_charmed_flag
    if current_position != 4 or snake_charmed_flag:
        print('nothing happens.')
    else:
        wrap_string('the snake is charmed by the very utterance of your words.')
        snake_charmed_flag = True
        items[2].location = -2
        items[3].location = 4


# pour
def pour_command(subject_index, subject):
    _ = subject
    global current_position, items, bucket_full_flag, fire_burning_flag
    if subject_index != 4:
        print("i wouldn't know how.")
    elif items[1].location != -1 and items[1].location != current_position:
        error_not_here()
    elif not bucket_full_flag:
        print('the bucket is already empty')
    elif current_position == 19:
        print('ok')
    elif current_position != 10 or not fire_burning_flag:
        print('the water disappears quickly.')
        bucket_full_flag = False
    else:
        print('congratulations! you have vanquished')
        print('the flames!')
        fire_burning_flag = False
        bucket_full_flag = False
        describe_current_position()


# fill
def fill_command(subject_index, subject):
    _ = subject
    global current_position, command_subjects, bucket_full_flag, pool_flooded_flag
    if subject_index == 0:
        error_unknown_object('what?')
    elif command_subjects[subject_index].item_id == -1:
        print("that wouldn't hold anything.")
    elif get_item_location(subject_index) != current_position and get_item_location(subject_index) != -1:
        error_not_here()
    elif subject_index != 4:
        print("that wouldn't hold anything.")
    elif bucket_full_flag:
        print("it's already full.")
    elif current_position == 25 and pool_flooded_flag:
        print("i'd rather stay away from the mercury.")
    elif current_position != 23 and current_position != 19:
        print("i don't see any water here.")
    else:
        print('your bucket is now full.')
        bucket_full_flag = True


# unlock object
def unlock_command(subject_index, subject):
    _ = subject
    global current_position, items
    if subject_index == 0:
        error_unknown_object('what?')
    elif subject_index != 12 and subject_index != 27:
        print("i wouldn't know how to unlock one.")
        main_command_loop()
    elif current_position != 0 and current_position != 5 and current_position != 6:
        error_not_here()
    elif current_position == 0 and subject_index == 12:
        unlock_front_door()
    elif current_position == 5 and subject_index == 27:
        unlock_vault()
    elif current_position != 6 or subject_index != 12 or items[16].location != -2:
        error_not_here()
    else:
        print('the trapdoor has no lock')


def unlock_vault():
    global rooms, vault_open_flag, found_vault_flag, know_combination_flag
    if vault_open_flag:
        print("it's already open.")
    elif not found_vault_flag:
        error_not_here()
    elif not know_combination_flag:
        print('i don''t know the combination.')
    else:
        print("ok, let's see.  12..35..6..")
        print('<click!> the door swings open.')
        vault_open_flag = True
        rooms[5].moves[2] = 46
        describe_current_position()


def unlock_front_door():
    global items, dungeon_unlocked_flag
    if dungeon_unlocked_flag:
        print("it's already unlocked.")
    elif items[20].location != -1:
        print('i need a key.')
    else:
        print('the door easily unlocks and swings open.')
        dungeon_unlocked_flag = True
        describe_current_position()


# look
def look_command(subject_index, subject):
    _, _ = subject_index, subject
    describe_current_position()


def describe_current_position():
    global current_position, rooms, items
    global pool_flooded_flag, fire_burning_flag, found_vault_flag, vault_open_flag, dungeon_unlocked_flag
    wrap_string(f'you are in the {rooms[current_position].text}')
    for x in range(1, len(items)):
        if items[x].location == current_position:
            wrap_string(f'there is a {items[x].text} here')
        if x == 1 and bucket_full_flag and items[1].location == current_position:
            print("the bucket is full of water")
    if current_position == 25:
        if pool_flooded_flag:
            print('the pool is full of liquid mercury')
        else:
            print("the pool's empty")
            if items[7].location == 48:
                print('i see something shiny in the pool!')
    if current_position == 10 and fire_burning_flag:
        print('there is a hot fire on the south wall!')
        print("if I go that way I'll burn to death!")
    if current_position == 16:
        wrap_string("a rich, full voice says, 'ritnew is a charming word'.")
    if current_position == 26:
        print('there is a valve on one of the pipes.')
    if current_position == 23:
        print('there is a leaky faucet nearby.')
    if current_position == 10 and not fire_burning_flag:
        print('there is evidence of a recent fire here.')
    if current_position == 5 and found_vault_flag:
        print('there is a vault in the east wall.')
    if current_position == 5 and vault_open_flag:
        print('the vault is open')
    if current_position == 0 and dungeon_unlocked_flag:
        print('an open door leads north.')
    if current_position != 48:
        print('obvious exits:')
        if rooms[current_position].moves[0] > 0:
            print('n ', end='')
        if rooms[current_position].moves[1] > 0:
            print('s ', end='')
        if rooms[current_position].moves[2] > 0:
            print('e ', end='')
        if rooms[current_position].moves[3] > 0:
            print('w ', end='')
        print('')


# go
def go_command(subject_index, subject):
    _ = subject
    global current_position, items
    if subject_index != 8 and subject_index != 18 and subject_index != 28:
        error_unknown_object('what?')
    elif subject_index == 8 and current_position != 48:
        error_not_here()
    elif subject_index == 18 and current_position != 2 and current_position != 27:
        error_not_here()
    elif subject_index == 28 and current_position != 25:
        error_not_here()
    elif subject_index == 8:
        current_position = 25
        describe_current_position()
    elif subject_index == 28 and pool_flooded_flag:
        print('the pool is full of mercury!')
    elif subject_index == 28:
        current_position = 48
    elif current_position == 27:
        current_position = 2
        describe_current_position()
    elif items[9].location == -1:
        print('the suits of armor try to stop you,')
        print('but you fight them off with your sword.')
        current_position = 27
        describe_current_position()
    else:
        wrap_string('the suits of armor prevent you from going up!')


# north
def north_command(subject_index, subject):
    _, _ = subject_index, subject
    global current_position, rooms, dungeon_unlocked_flag
    if current_position == 0 and not dungeon_unlocked_flag:
        print('the door is locked shut.')
        return
    elif rooms[current_position].moves[0] == 0:
        error_no_path()
        return
    elif current_position == 0:
        print('the door slams shut behind you!')
    current_position = rooms[current_position].moves[0]
    describe_current_position()


# south
def south_command(subject_index, subject):
    _, _ = subject_index, subject
    global current_position, rooms, fire_burning_flag
    if current_position == 10 and fire_burning_flag:
        print('you have burnt to a crisp!')
        exit()

    if rooms[current_position].moves[1] == 0:
        error_no_path()
    else:
        current_position = rooms[current_position].moves[1]
        describe_current_position()


# east
def east_command(subject_index, subject):
    _, _ = subject_index, subject
    global current_position, rooms, snake_charmed_flag, angry_snake_flag
    if current_position == 4 and not snake_charmed_flag and not angry_snake_flag:
        print('the snake is about to attack!')
        angry_snake_flag = True
    elif current_position == 4 and not snake_charmed_flag:
        print('the snake bites you!')
        print('you are dead.')
        exit()

    if rooms[current_position].moves[2] == 0:
        error_no_path()
    else:
        current_position = rooms[current_position].moves[2]
        describe_current_position()


# west
def west_command(subject_index, subject):
    _, _ = subject_index, subject
    global current_position, rooms
    if rooms[current_position].moves[3] == 0:
        error_no_path()
    else:
        current_position = rooms[current_position].moves[3]
        describe_current_position()


# score
def score_command(subject_index, subject):
    _, _ = subject_index, subject
    global gathered_treasures
    print('if you were to quit now,')
    print('you would have a score of')
    print(gathered_treasures * 20, 'points.')
    print('(100 possible)')
    while True:
        print('do you indeed wish to quit now? ')
        input_str = get_input()
        if input_str[0].lower() == 'y':
            final_stats()
        elif input_str[0].lower() == 'n':
            print('ok')
            print()
            break


# turn
def turn_command(subject_index, subject):
    _ = subject
    global current_position, items, pool_flooded_flag
    if subject_index != 7:
        print("i don't know how to turn such a thing.")
        describe_current_position()
    elif current_position != 26:
        error_not_here()
    else:
        wrap_string('with much effort, you turn the valve 5 times.  you hear the sound of liquid')
        print('flowing through the pipes.')
        pool_flooded_flag = not pool_flooded_flag
        if not pool_flooded_flag and items[7].location == -3:
            items[7].location = 25
        elif pool_flooded_flag and items[7].location == 25:
            items[7].location = -3


# jump
def jump_command(subject_index, subject):
    _, _ = subject_index, subject
    global current_position, items, escaped_flag, jump_warning_flag
    if current_position != 27 and current_position != 29 and current_position != 32:
        print("there's nowhere to jump.")
        main_command_loop()
    else:
        print('you jump..')
        if current_position == 27:
            jump_down_stairs()
        elif items[14].location == -1:
            print('there is no way to open the parachute!')
        elif items[27].location == -1:
            print('you yank the ripcord and the')
            print("'chute comes billowing out.")
            if current_position == 32:
                current_position = 40
                describe_current_position()
            else:
                print('you land safely')
                print('congratulations on escaping!')
                escaped_flag = True
                final_stats()
        print('you hit the ground.')
        print("you have broken your neck!")
        print("you are dead.")
        exit()


def jump_down_stairs():
    global jump_warning_flag, current_position
    if jump_warning_flag:
        print("now you've done it.  you ignored")
        print("my warning, and as a result")
        print("you have broken your neck!")
        print("you are dead.")
        exit()
    else:
        print('you have landed down-stairs,')
        print('and narrowly escaped serious')
        print("injury.  please don't try it again.")
        jump_warning_flag = True
        current_position = 2
        describe_current_position()


# swim
def swim_command(subject_index, subject):
    _, _ = subject_index, subject
    global current_position, pool_flooded_flag
    if current_position != 19 and current_position != 25:
        print("there's nothing here to swim in!")
    elif current_position == 19:
        print('the water is only a few inches deep.')
    elif pool_flooded_flag:
        print("in mercury?  no way!")
    else:
        print('the pool is empty.')


# fix
def fix_command(subject_index, subject):
    _ = subject
    global current_position, items, command_subjects
    if subject_index == 0:
        error_unknown_object('what')
    elif subject_index == 7:
        print("i ain't no plumber!")
    elif subject_index != 17:
        print("i wouldn't know how.")
    elif get_item_location(subject_index) != current_position and get_item_location(subject_index) != -1:
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


def welcome_banner():
    print(f'{program_name:>12} by m.j. lansing')
    print(f'   cursor # {cursor_issue}  copyright (c) 1981')
    print('*' * 40)
    print("explore the miser's house   (needs 16k)")
    print('\n\n\npress return to begin')
    wait_for_keypress()
    print('\n\none moment please...')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
