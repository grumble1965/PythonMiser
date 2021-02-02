# This is a Python port of the Miser's House BASIC adventure.

import pyreadline.rlmain

rl = pyreadline.Readline()
prompt = "> "


# useful functions
def clear_screen():
    rl.console.home()
    rl.console.clear_to_end_of_window()
    pass


def wait_for_keypress():
    _ = rl.readline()
    # _ = readline()


def delay():
    pass


# todo: rename horrible names
# variables
program_name, cursor_issue = 'miser', '27'
help_strings, help_index = [], 0
text_wrap_width = 80
ol = pt = []
rStr = []
rInt = []
om = []
verbs = o = []
pool_flooded_flag = bucket_full_flag = fire_burning_flag = vault_open_flag = False
found_vault_flag = dungeon_unlocked_flag = know_combination_flag = False
gg_flag = escaped_flag = snake_charmed_flag = angry_snake_flag = jump_warning_flag = False
portal_visible_flag = False
gathered_treasures = 0
current_position = 0


def line0():
    welcome_banner()
    initialize_data()
    clear_screen()
    line699()


def fna(x):
    global ol
    global pt
    return ol[pt[x]]


def initialize_data():
    # TODO: make parallel arrays into structs or objects
    global rStr
    global rInt
    global om
    global ol
    global verbs
    global o
    global pt
    global pool_flooded_flag
    pool_flooded_flag = 1
    global fire_burning_flag
    fire_burning_flag = 1
    global help_strings
    help_strings = ['what?', "i don't understand that"]
    r_int_r_str_data = [
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
        ([0, 0, 0, 21], 'chapel.  a tablet says ''drop a religious item or die!!'''),
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
    l1 = []
    l2 = []
    for (xx, yy) in r_int_r_str_data:
        l1.append(xx)
        l2.append(yy)
    rInt = l1
    rStr = l2

    verbs = ['--unused--', 'get', 'take', 'move', 'slid', 'push', 'open', 'read', 'inve', 'quit']
    verbs += ['drop', 'say', 'pour', 'fill', 'unlo', 'look']
    verbs += ['go', 'nort', 'n', 'sout', 's', 'east', 'e', 'west', 'w', 'scor', 'turn']
    verbs += ['jump', 'swim', 'i', 'fix']

    o_pt_data = [
        ('--unused--', -999),
        ('ripc', 17), ('mat', 10), ('pape', 13), ('buck', 1), ('swor', 9),
        ('key', 20), ('valv', -1), ('ladd', -1), ('slip', 19), ('rug', 15),
        ('book', 23), ('door', -1), ('cabi', -1), ('ritn', -1), ('vict', -1),
        ('orga', -1), ('para', 14), ('stai', -1), ('penn', 12), ('cros', 11),
        ('leaf', 4), ('bag', 5), ('>$<', -1), ('>$<', -1), ('ring', 7),
        ('pain', 8), ('vaul', -1), ('pool', -1), ('xyzz', -1), ('plug', -1)
    ]
    l1 = []
    l2 = []
    for (xx, yy) in o_pt_data:
        l1.append(xx)
        l2.append(yy)
    o = l1
    pt = l2

    om_ol_data = [
        ('--unused--', -999),
        ('plastic bucket', 26), ('vicious snake', 4), ('charmed snake', -2), ('*golden leaf*', 45),
        ('*bulging moneybag*', 46), ('>$<', -2), ('*diamond ring*', 48), ('*rare painting*', 39),
        ('sword', 13), ('mat', 0), ('rusty cross', 23), ('penny', 28), ('piece of paper', 31),
        ('parachute with no ripcord', 34), ('oriental rug', 6), ('trapdoor marked ''danger''', -2),
        ('parachute ripcord', -2), ('portal in north wall', -2), ('pair of *ruby slippers*', -2),
        ('brass door key', -2), ('majestic staircase leading up', 2),
        ('majestic staircase leading down', 27), ('battered book', 11), ('organ in the corner', 21),
        ('open organ in the corner', -2), ('cabinet on rollers against one wall over', 5),
        ('repaired parachute', -2), ("sign saying 'drop coins for luck'", 19)
    ]
    l1 = []
    l2 = []
    for (xx, yy) in om_ol_data:
        # print('xx = ', xx, 'yy = ', yy)
        l1.append(xx)
        l2.append(yy)
    om = l1
    ol = l2


def line699():
    look_command()


# todo: fix disgusting control flow
def line700():
    print()
    input_str = get_input()
    input_str.strip()
    parse = input_str.split()
    if len(parse) < 1 or len(parse) > 2:
        print('please type a one or two world command')
        line700()
    command_verb = parse[0]
    command_object = 'unassigned'
    if len(command_verb) > 4:
        command_verb = command_verb[0:4]
    verb_index = -1
    for x in range(1, len(verbs)):
        if command_verb == verbs[x]:
            print(f'command {verbs[x]} {x}')
            verb_index = x
    if verb_index == -1:
        error_unknown_object(command_verb)
        line700()

    if len(parse) == 1:
        object_index = 0
    else:
        command_object = parse[1]
        if len(command_object) > 4:
            command_object = command_object[0:4]
        object_index = -1
        for x in range(1, len(o)):
            if command_object == o[x]:
                # print(f'object {o[x]} {x}')
                object_index = x
        if object_index == -1:
            error_unknown_object(command_object)
            line700()
    if verb_index == 1 or verb_index == 2:
        get_take_command(object_index)
    elif verb_index == 3 or verb_index == 4 or verb_index == 5:
        move_slide_push_command(object_index)
    elif verb_index == 6:
        open_command(object_index)
    elif verb_index == 7:
        read_command(object_index)
    elif verb_index == 8:
        inventory_command()
    elif verb_index == 9:
        quit_command()
    elif verb_index == 10:
        drop_command(object_index)
    elif verb_index == 11:
        say_command(object_index, command_object)
    elif verb_index == 12:
        pour_command(object_index)
    elif verb_index == 13:
        fill_command(object_index)
    elif verb_index == 14:
        unlock_command(object_index)
    elif verb_index == 15:
        look_command()
    elif verb_index == 16:
        go_command(object_index)
    elif verb_index == 17 or verb_index == 18:
        north_command()
    elif verb_index == 19 or verb_index == 20:
        south_command()
    elif verb_index == 21 or verb_index == 22:
        east_command()
    elif verb_index == 23 or verb_index == 24:
        west_command()
    elif verb_index == 25:
        score_command()
    elif verb_index == 26:
        turn_command(object_index)
    elif verb_index == 27:
        jump_command()
    elif verb_index == 28:
        swim_command()
    elif verb_index == 29:
        inventory_command()
    elif verb_index == 30:
        fix_command(object_index)

    line700()


# get, take object
def get_take_command(obj):
    global pt
    global current_position
    global ol
    global gathered_treasures
    if obj == 0:
        error_unknown_object('what?')
    elif pt[obj] == -1:
        print('i am unable to do that.')
    elif fna(obj) == -1:
        print("you're already carrying it")
    elif fna(obj) != current_position:
        error_not_here()
    else:
        # print('obj = ', obj)
        # print('pt = ', pt)
        # print('ol = ', ol)
        ol[pt[obj]] = -1
        print('ok')

        # line 1030
        if (3 < pt[obj] < 9) or pt[obj] == 19:
            print('you got a treasure!')
            gathered_treasures += 1
        # line 1040
        if obj == 2 and ol[20] == -2:
            print('you find a door key!')
            ol[20] = 0
    line700()


# move, slide, push
def move_slide_push_command(obj):
    global current_position
    global rInt
    global pt
    global ol
    global found_vault_flag
    print('2000 command')
    if obj == 0:
        error_unknown_object('move what?')
    elif obj == 13 and current_position == 5 and rInt[5][3] == 0:
        print('behind the cabinet is a vault!')
        found_vault_flag = True
        line699()
    elif pt[obj] == -1:
        print('that item stays put.')
    elif fna(obj) != current_position and fna(obj) != -1:
        error_not_here()
    elif obj == 2 and ol[20] == -2:
        # line 1040
        print('you find a door key!')
        ol[20] = 0
    elif obj == 10 and ol[16] == -2:
        print('you find a trap door!')
        ol[16] = 6
        line699()
    else:
        print('moving it reveals nothing.')
    line700()


# open
def open_command(obj):
    print('4000 command')
    if obj == 0:
        error_unknown_object('open what?')
    elif obj != 11:
        line4030(obj)
    elif fna(obj) != current_position and fna(obj) != -1:
        line4030(obj)
    else:
        wrap_string("scrawled in blood on the inside front cover is the message,")
        print("''victory' is a prize-winning word'.")
    line700()


def line4030(obj):
    global current_position
    global dungeon_unlocked_flag
    print('line4030')
    if obj == 7:
        print('try turning it.')
        line700()
    elif obj != 12:
        line4120(obj)
    elif current_position == 0 and not dungeon_unlocked_flag:
        print('sorry, the door is locked.')
        line700()
    elif current_position == 0 and dungeon_unlocked_flag:
        print("it's already open.")
        line700()
    elif current_position != 6:
        error_not_here()
    else:
        wrap_string('you open the door. you lean over to peer in, and you fall in!')
        current_position = 47
        line699()


def line4120(obj):
    global current_position
    if obj != 13:
        line4160(obj)
    elif ol[26] != current_position:
        error_not_here()
    else:
        print('the cabinet is empty and dusty.')
        wrap_string("scribbled in the dust on one shelf are the words, 'behind me'.")
    line700()


def line4160(obj):
    global current_position
    if obj != 22:
        line4190(obj)
    elif fna(obj) != current_position and fna(obj) != -1:
        error_not_here()
    else:
        print('the bag is knotted securely.')
        print("it won't open.")
        line700()


def line4190(obj):
    global current_position
    global found_vault_flag
    global vault_open_flag
    if obj != 27:
        line4230(obj)
    elif current_position != 5 or not found_vault_flag:
        error_not_here()
    elif vault_open_flag:
        print("it's already open.")
    else:
        print("i can't, it's locked.")
    line700()


def line4230(obj):
    global gg_flag
    global ol
    if obj != 16:
        print("i don't know how to open that.")
    elif current_position != 21:
        error_not_here()
    elif not gg_flag:
        print("it's stuck shut.")
    elif ol[24] == -2:
        print("it's already open.")
    else:
        print('as you open it, several objects suddenly appear!')
        ol[24] = -2
        ol[25] = 21
        ol[19] = 21
        ol[17] = 21
        line699()
    line700()


# read
def read_command(obj):
    print('5000 command')
    global current_position
    global know_combination_flag
    if obj == 0:
        error_unknown_object('read what?')
    if pt[obj] > -1 and fna(obj) != current_position and fna(obj) != -1:
        error_not_here()
    elif pt[obj] == -1:
        print("there's nothing written on that.")
    elif obj != 3 and obj != 11:
        print("there's nothing written on that.")
    elif obj == 11:
        print('the front cover is inscribed in greek.')
    else:
        print("it says, '12-35-6'.")
        print('hmm.. looks like a combination.')
        know_combination_flag = True
    line700()


# inventory
def inventory_command():
    print('6000 command')
    global ol
    global om
    global bucket_full_flag
    print('you are carrying the following:')
    carrying_something = False
    # print('ol = ', ol)
    # print('om = ', om)
    for x in range(1, len(ol)):
        if ol[x] == -1:
            print(om[x])
            carrying_something = True
        if x == 1 and bucket_full_flag and ol[1] == -1:
            print('  the bucket is full of water.')
        if x == 14 and ol[14] == -1:
            print('   (better fix it)')
    if not carrying_something:
        print('nothing at all.')
    line700()


# quit
def quit_command():
    print('7000 command')
    print('do you indeed wish to quit now?')
    input_str = get_input()
    if input_str[0].lower() != 'y':
        print('ok')
    else:
        clear_screen()
        final_stats()
    line700()


def final_stats():
    global gathered_treasures
    global escaped_flag
    print('7010 command')
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
def drop_command(obj):
    global current_position
    global ol
    global om
    global pt
    global rInt
    global rStr
    global gg_flag
    print('8000 command')
    if fna(obj) != -1:
        print("you aren't carrying it!")
    else:
        x = pt[obj]
        if (3 < x < 9) or x == 19:
            print("don't drop *treasures*!")
        elif current_position == 19 and obj == 19:
            wrap_string('as the penny sinks below the surface of the pool, a fleeting image of')
            print('a chapel with dancers appears.')
            rInt[21][3] = 22
            ol[12] = -2
        elif current_position == 22 and obj == 20:
            wrap_string('even before it hits the ground, the cross fades away!')
            print('the tablet has disintegrated.')
            print('you hear music from the organ.')
            gg_flag = True
            ol[11] = -2
            rStr[22] = 'chapel'
            om[24] = 'closed organ playing music in the corner'
        else:
            ol[pt[obj]] = current_position
            print('ok')
    line700()


# say
def say_command(obj, word):
    global current_position
    global snake_charmed_flag
    global ol
    global portal_visible_flag
    global rInt
    print('9000 command')
    if obj == 0:
        print('say what???')
    elif obj == 14:
        if current_position != 4 or snake_charmed_flag == 1:
            print('nothing happens.')
        else:
            wrap_string('the snake is charmed by the very utterance of your words.')
            snake_charmed_flag = True
            ol[2] = -2
            ol[3] = 4
    elif obj == 15:
        if current_position != 8 or portal_visible_flag:
            print('nothing happens.')
        else:
            print('a portal has opened in the north wall!!')
            portal_visible_flag = True
            rInt[8][0] = 17
            ol[18] = 8
    elif obj > 28:
        print("a hollow voice says, 'wrong adventure'.")
    else:
        print('okay, "', word, '".')
        delay()
        print('nothing happens.')
    line700()


# pour
def pour_command(obj):
    global ol
    global current_position
    global bucket_full_flag
    global fire_burning_flag
    print('10000 command')
    if obj != 4:
        print("i wouldn't know how.")
    elif ol[1] != -1 and ol[1] != current_position:
        error_not_here()
    elif not bucket_full_flag:
        print('the bucket is already empty')
    elif current_position == 19:
        print('ok')
    elif current_position != 10 or not fire_burning_flag:
        print('the water disappears quickly.')
        bucket_full_flag = 0
    else:
        print('congratulations! you have vanquished')
        print('the flames!')
        fire_burning_flag = False
        bucket_full_flag = False
        line699()
    line700()


# fill
def fill_command(obj):
    global pt
    global current_position
    global bucket_full_flag
    global pool_flooded_flag
    print('11000 command')
    if obj == 0:
        error_unknown_object('what?')
    elif pt[obj] == -1:
        print("that wouldn't hold anything.")
    elif fna(obj) != current_position and fna(obj) != -1:
        error_not_here()
    elif obj != 4:
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
    line700()


# unlock object
def unlock_command(obj):
    global current_position
    global ol
    print('12000 command')
    if obj == 0:
        error_unknown_object('what?')
    elif obj != 12 and obj != 27:
        print("i wouldn't know how to unlock one.")
        line700()
    elif current_position != 0 and current_position != 5 and current_position != 6:
        error_not_here()
    elif current_position == 0 and obj == 12:
        line12200()
    elif current_position == 5 and obj == 27:
        line12300()
    elif current_position != 6 or obj != 12 or ol[16] != -2:
        error_not_here()
    else:
        print('the trapdoor has no lock')
    line700()


def line12200():
    global dungeon_unlocked_flag
    global ol
    if dungeon_unlocked_flag:
        print("it's already unlocked.")
        line700()
    elif ol[20] != -1:
        print('i need a key.')
        line700()
    else:
        print('the door easily unlocks and swings open.')
        dungeon_unlocked_flag = True
        look_command()


def line12300():
    global vault_open_flag
    global found_vault_flag
    global know_combination_flag
    global rInt
    if vault_open_flag:
        print("it's already open.")
        line700()
    elif not found_vault_flag:
        error_not_here()
    elif not know_combination_flag:
        print('i don''t know the combination.')
        line700()
    else:
        print("ok, let's see.  12..35..6..")
        print('<click!> the door swings open.')
        vault_open_flag = True
        rInt[5][2] = 46
        look_command()


# look
def look_command():
    global current_position
    global rStr
    global rInt
    global om
    global ol
    global pool_flooded_flag
    global fire_burning_flag
    global found_vault_flag
    global vault_open_flag
    global dungeon_unlocked_flag
    wrap_string(f'you are in the {rStr[current_position]}')
    # print('ol = ', ol)
    # print('om = ', om)
    for x in range(1, len(ol)):
        if ol[x] == current_position:
            wrap_string(f'there is a {om[x]} here')
        if x == 1 and bucket_full_flag and ol[1] == current_position:
            print("the bucket is full of water")
    if current_position == 25:
        if pool_flooded_flag:
            print('the pool is full of liquid mercury')
        else:
            print("the pool's empty")
            if ol[7] == 48:
                print('i see something shiny in the pool!')
    if current_position == 10 and fire_burning_flag:
        print('there is a hot fire on the south wall!')
        print('if I go that way I''ll burn to death!')
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
        if rInt[current_position][0] > 0:
            print('n ', end='')
        if rInt[current_position][1] > 0:
            print('s ', end='')
        if rInt[current_position][2] > 0:
            print('e ', end='')
        if rInt[current_position][3] > 0:
            print('w ', end='')
        print('')
    line700()


# go
def go_command(obj):
    global current_position
    global ol
    print('15000 command')
    if obj != 8 and obj != 18 and obj != 28:
        error_unknown_object('what?')
    elif obj == 8 and current_position != 48:
        error_not_here()
    elif obj == 18 and current_position != 2 and current_position != 27:
        error_not_here()
    elif obj == 28 and current_position != 25:
        error_not_here()
    elif obj == 8:
        current_position = 25
        line699()
    elif obj == 28 and pool_flooded_flag:
        print('the pool is full of mercury!')
        line700()
    elif obj == 28:
        current_position = 48
        line700()
    elif current_position == 27:
        current_position = 2
        line699()
    elif ol[9] == -1:
        print('the suits of armor try to stop you,')
        print('but you fight them off with your sword.')
        current_position = 27
        line699()
    else:
        wrap_string('the suits of armor prevent you from going up!')
        line700()


# north
def north_command():
    global current_position
    global dungeon_unlocked_flag
    global rInt
    if current_position == 0 and not dungeon_unlocked_flag:
        print('the door is locked shut.')
        line700()
    elif rInt[current_position][0] == 0:
        error_no_path()
    elif current_position == 0:
        print('the door slams shut behind you!')
    current_position = rInt[current_position][0]
    look_command()


# south
def south_command():
    global current_position
    global fire_burning_flag
    print('17000 command')
    if current_position == 10 and fire_burning_flag:
        print('you have burnt to a crisp!')
        exit()

    if rInt[current_position][1] == 0:
        error_no_path()
    else:
        current_position = rInt[current_position][1]
        line699()


# east
def east_command():
    global current_position
    global snake_charmed_flag
    global angry_snake_flag
    global rInt
    print('17010 command')
    if current_position == 4 and not snake_charmed_flag and not angry_snake_flag:
        print('the snake is about to attack!')
        angry_snake_flag = True
        line700()
    elif current_position == 4 and not snake_charmed_flag:
        print('the snake bites you!')
        print('you are dead.')
        exit()

    if rInt[current_position][2] == 0:
        error_no_path()
    else:
        current_position = rInt[current_position][2]
        line699()


# west
def west_command():
    global current_position
    global rInt
    print('19000 command')
    if rInt[current_position][3] == 0:
        error_no_path()
    else:
        current_position = rInt[current_position][3]
        line699()


# score
def score_command():
    global gathered_treasures
    print('20000 command')
    print('if you were to quit now,')
    print('you would have a score of')
    print(gathered_treasures * 20, 'points.')
    print('(100 possible)')
    while True:
        print('do you indeed wish to quit now?')
        input_str = get_input()
        if input_str[0].lower() == 'y':
            final_stats()
        elif input_str[0].lower() == 'n':
            print('ok')
            print()
            break
    line700()


# turn
def turn_command(obj):
    global current_position
    global pool_flooded_flag
    global ol
    print('21000 command')
    if obj != 7:
        print("i don't know how to turn such a thing.")
        line699()
    elif current_position != 26:
        error_not_here()
    else:
        wrap_string('with much effort, you turn the valve 5 times.  you hear the sound of liquid')
        print('flowing through the pipes.')
        pool_flooded_flag = not pool_flooded_flag
        if not pool_flooded_flag and ol[7] == -3:
            ol[7] = 25
            line700()
        elif pool_flooded_flag and ol[7] == 25:
            ol[7] = -3
            line700()
        else:
            line700()


# jump
def jump_command():
    global ol
    global current_position
    global escaped_flag
    global jump_warning_flag
    print('22000 command')
    if current_position != 27 and current_position != 29 and current_position != 32:
        print("there's nowhere to jump.")
        line700()
    else:
        print('you jump..')
        if current_position == 27:
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
                line699()
        if ol[14] == -1:
            print('there is no way to open the parachute!')
        elif ol[27] == -1:
            print('you yank the ripcord and the')
            print("'chute comes billowing out.")
            if current_position == 32:
                current_position = 40
                line699()
            else:
                print('you land safely')
                print('congratulations on escaping!')
                escaped_flag = True
                final_stats()
        print('you hit the ground.')
        print("you have broken your neck!")
        print("you are dead.")
        exit()


# swim
def swim_command():
    global current_position
    global pool_flooded_flag
    print('24000 command')
    if current_position != 19 and current_position != 25:
        print("there's nothing here to swim in!")
    elif current_position == 19:
        print('the water is only a few inches deep.')
    elif pool_flooded_flag:
        print("in mercury?  no way!")
    else:
        print('the pool is empty.')
    line700()


# fix
def fix_command(obj):
    global current_position
    global ol
    global pt
    print('25000 command')
    if obj == 0:
        error_unknown_object('what')
    elif obj == 7:
        print("i ain't no plumber!")
    elif obj != 17:
        print("i wouldn't know how.")
    elif fna(obj) != current_position and fna(obj) != -1:
        error_not_here()
    elif ol[14] == -2:
        print("it's already fixed.")
    elif ol[17] != -1:
        print("i'll need a ripcord.")
    else:
        print("i'm no expert, but i think it'll work.")
        ol[27] = ol[14]
        ol[14] = -2
        pt[17] = 27
        ol[17] = 0
    line700()


def error_unknown_object(unknown_object):
    global help_index
    print(f'{unknown_object}?  {help_strings[help_index]}')
    help_index += 1
    if help_index >= len(help_strings):
        help_index = 0
    line700()


def error_not_here():
    print("i don't see it here")
    line700()


def error_no_path():
    print("it's impossible to go that way.")
    line700()


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
    return rl.readline(prompt)


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
    line0()
