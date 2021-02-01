# This is a Python port of the Miser's House BASIC adventure.

# useful functions
def clear_screen():
    pass


def wait_for_keypress():
    _ = input()


def delay():
    pass


# variables
program_name, cursor_issue = '', ''
ol = pt = []
screen_width = 0
rStr = []
rInt = []
om = []
v = o = []
em = pf = fb = vo = fv = du = kc = bf = gt = gg = es = ch = ps = jm = po = 0
h = []
in_str = ''
cp = 0


def line0():
    global program_name
    program_name = 'miser'
    global cursor_issue
    cursor_issue = '27'
    line62000()


def fna(x):
    global ol
    global pt
    return ol[pt[x]]


def line20():
    global screen_width
    screen_width = 80
    global rStr
    global rInt
    global om
    global ol
    global v
    global o
    global pt
    global em
    em = 1
    global pf
    pf = 1
    global fb
    fb = 1
    global h
    h = ['what?', "i don't understand that"]
    r_int_r_str_data = [
        ([1, 0, 0, 0], 'front porch'),
        ([2, 0, 0, 12], 'foyer to a large house.  dust is everywhere'),
        ([3, 1, 0, 0], 'great hall.  suits of armor line th walls'),
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

    v = ['get', 'take', 'move', 'slid', 'push', 'open', 'read', 'inve', 'quit']
    v += ['drop', 'say', 'pour', 'fill', 'unlo', 'look']
    v += ['go', 'nort', 'n', 'sout', 's', 'east', 'e', 'west', 'w', 'scor', 'turn']
    v += ['jump', 'swim', 'i', 'fix']

    o_pt_data = [
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
        ('plastic bucket', 26), ('vicious snake', 4), ('charmed snake', -2), ('*golden leaf*', 45),
        ('*bulging moneybag*', 46), ('>$<', -2), ('*diamond ring*', 48), ('*rare painting*', 39),
        ('sword', 13), ('mat', 0), ('rusty cross', 23), ('penny', 28), ('piece of paper', 31),
        ('parachute with no ripcord', 34), ('oriental rug', 6), ('trapdoor marked ''danger''', -2),
        ('parachute ripcord', -2), ('portal in north wall', -2), ('pair of *ruby slippers*', -2),
        ('brass door key', -2), ('majestic staircase leading up', 2),
        ('majestic staircase leading down', 27), ('battered book', 11), ('organ in the corner', 21),
        ('open organ in the corner', -2), ('cabinet on rollers against one wall over', 5),
        ('repaired parachute', -2), ('sign saying ''drop coins for luck''', 19)
    ]
    l1 = []
    l2 = []
    for (xx, yy) in om_ol_data:
        # print('xx = ', xx, 'yy = ', yy)
        l1.append(xx)
        l2.append(yy)
    om = l1
    ol = l2

    clear_screen()
    line699()


def line699():
    line14000()


def line700():
    print('')
    sc = sf = 0
    line60000()
    in_str.strip()
    parse = in_str.split()
    if len(parse) < 1 or len(parse) > 2:
        print('please type a one or two world command')
        line700()
    cv = parse[0]
    if len(cv) > 4:
        cv = cv[0:4]
    i = -1
    for x in range(len(v)):
        if cv == v[x]:
            print(f'command {v[x]} {x}')
            i = x
    if i == -1:
        line50000(cv)
        line700()

    if len(parse) == 1:
        j = 0
    else:
        co = parse[1]
        if len(co) > 4:
            co = co[0:4]
        j = -1
        for x in range(len(o)):
            if co == o[x]:
                print(f'object {o[x]} {x}')
                j = x + 1
        if j == -1:
            line50000(co)
            line700()
    if i == 0 or i == 1:
        line1000(j)
    elif i == 2 or i == 3 or i == 4:
        line2000(j)
    elif i == 5:
        line4000(j)
    elif i == 6:
        line5000(j)
    elif i == 7:
        line6000()
    elif i == 8:
        line7000()
    elif i == 9:
        line8000(j)
    elif i == 10:
        line9000(j, co)
    elif i == 11:
        line10000(j)
    elif i == 12:
        line11000(j)
    elif i == 13:
        line12000(j)
    elif i == 14:
        line14000()
    elif i == 15:
        line15000(j)
    elif i == 16 or i == 17:
        line16000()
    elif i == 18 or i == 19:
        line17000()
    elif i == 20 or i == 21:
        line17010()
    elif i == 22 or i == 23:
        line19000()
    elif i == 24:
        line20000()
    elif i == 25:
        line21000(j)
    elif i == 26:
        line22000()
    elif i == 27:
        line24000()
    elif i == 28:
        line6000()
    elif i == 29:
        line25000(j)

    line700()


# get, take object
def line1000(obj):
    global pt
    global cp
    global ol
    global gt
    if obj == 0:
        line50000('what?')
    if pt[obj] == -1:
        print('i am unable to do that.')
        line700()
    elif fna(obj) == -1:
        print("you're already carrying it")
        line700()
    elif fna(obj) != cp:
        line51000()

    # print('obj = ', obj)
    # print('pt = ', pt)
    # print('ol = ', ol)
    ol[pt[obj - 1]] = -1
    print('ok')

    # line 1030
    if (3 < pt[obj] < 9) or pt[obj] == 19:
        print('you got a treasure!')
        gt += 1
    # line 1040
    if obj == 2 and ol[20] == -2:
        print('you find a door key!')
        ol[20] = 0
    line700()


# move, slide, push
def line2000(obj):
    global cp
    global rInt
    global pt
    global ol
    global fv
    print('2000 command')
    if obj == 0:
        line50000('move what?')
    elif obj == 13 and cp == 5 and rInt[5][3] == 0:
        print('behind the cabinet is a vault!')
        fv = 1
        line699()
    elif pt[obj] == -1:
        print('that item stays put.')
    elif fna(obj) != cp and fna(obj) != -1:
        line51000()
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
def line4000(obj):
    global in_str
    print('4000 command')
    if obj == 0:
        line50000('open what?')
    elif obj != 11:
        line4030(obj)
    elif fna[obj] != cp and fna(obj) != -1:
        line4030(obj)
    else:
        in_str = "scrawled in blood on the inside front cover is the message,"
        line53000()
        print("''victory' is a prize-winning word'.")
    line700()


def line4030(obj):
    global cp
    global du
    global in_str
    print('line4030')
    if obj == 7:
        print('try turning it.')
        line700()
    elif obj != 12:
        line4120(obj)
    elif cp == 0 and du == 0:
        print('sorry, the door is locked.')
        line700()
    elif cp == 0 and du == 1:
        print("it's already open.")
        line700()
    elif cp != 6:
        line51000()
    else:
        in_str = 'you open the door. you lean over to peer in, and you fall in!'
        line53000()
        cp = 47
        line699()


def line4120(obj):
    global cp
    global in_str
    if obj != 13:
        line4160(obj)
    elif ol[26] != cp:
        line51000()
    else:
        print('the cabinet is empty and dusty.')
        in_str = "scribbled in the dust on one shelf are the words, 'behind me'."
        line53000()
    line700()


def line4160(obj):
    global cp
    if obj != 22:
        line4190(obj)
    elif fna(obj) != cp and fna(obj) != -1:
        line51000()
    else:
        print('the bag is knotted securely.')
        print("it won't open.")
        line700()


def line4190(obj):
    global cp
    global fv
    if obj != 27:
        line4230(obj)
    elif cp != 5 or fv == 0:
        line51000()
    elif vo == 1:
        print("it's already open.")
    else:
        print("i can't, it's locked.")
    line700()


def line4230(obj):
    global gg
    global ol
    if obj != 16:
        print("i don't know how to open that.")
    elif cp != 21:
        line51000()
    elif gg == 0:
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
def line5000(obj):
    print('5000 command')
    global cp
    global kc
    if obj == 0:
        line50000('read what?')
    if pt[obj] > -1 and fna(obj) != cp and fna(obj) != -1:
        line51000()
    elif pt[obj] == -1:
        print("there's nothing written on that.")
    elif obj != 3 and obj != 11:
        print("there's nothing written on that.")
    elif obj == 11:
        print('the front cover is inscribed in greek.')
    else:
        print("it says, '12-35-6'.")
        print('hmm.. looks like a combination.')
        kc = 1
    line700()


# inventory
def line6000():
    global ol
    global om
    global bf
    print('you are carrying the following:')
    fi = 0
    # print('ol = ', ol)
    # print('om = ', om)
    for x in range(len(ol)):
        if ol[x] == -1:
            print(om[x - 1])
            fi = 1
        if x == 1 and bf == 1 and ol[1] == -1:
            print('  the bucket is full of water.')
        if x == 14 and ol[14] == -1:
            print('   (better fix it)')
    if fi == 0:
        print('nothing at all.')
    line700()


# quit
def line7000():
    global in_str
    print('7000 command')
    print('do you indeed wish to quit now?')
    line60000()
    if in_str[0].lower() != 'y':
        print('ok')
        line700()
    else:
        clear_screen()
        line7010()


def line7010():
    global gt
    global es
    print('7010 command')
    print('you accumulated', gt, 'treasures,')
    print('for a score of', gt * 20, 'points.')
    print('(100 possible)')
    if es == 0:
        print('however, you did not escape.')
    print('this puts you in a class of:')
    if es == 1:
        gt += 1
    if gt == 0:
        print('<beginner adventurer>')
    elif gt == 1:
        print('<amateur adventurer>')
    elif gt == 2:
        print('<journeyman adventurer>')
    elif gt == 3:
        print('<experienced adventurer>')
    elif gt == 4:
        print('<professional adventurer>')
    elif gt == 5:
        print('<master adventurer>')
    else:
        print('<grandmaster adventurer>')
    if gt < 6:
        print('better luck next time!')
    exit(0)


# drop
def line8000(obj):
    global cp
    global ol
    global om
    global pt
    global in_str
    global rInt
    global rStr
    global gg
    print('8000 command')
    if fna(obj) != -1:
        print("ou aren't carrying it!")
    else:
        x = pt[obj]
        if (3 < x < 9) or x == 19:
            print("don't drop *treasures*!")
        elif cp == 19 and obj == 19:
            in_str = 'as the penny sinks below the surface of the pool, a fleeting image of'
            line53000()
            print('a chapel with dancers appears.')
            rInt[21][3] = 22
            ol[12] = -2
        elif cp == 22 and obj == 20:
            in_str = 'even before it hits the ground, the cross fades away!'
            line53000()
            print('the tablet has disintegrated.')
            print('you hear music from the organ.')
            gg = 1
            ol[11] = -2
            rStr[22] = 'chapel'
            om[24] = 'closed organ playing music in the corner'
        else:
            ol[pt[obj]] = cp
            print('ok')
    line700()


# say
def line9000(obj, word):
    global cp
    global ch
    global in_str
    global ol
    global po
    global rInt
    print('9000 command')
    if obj == 0:
        print('say what???')
    elif obj == 14:
        if cp != 4 or ch == 1:
            print('nothing happens.')
        else:
            in_str = 'the snake is charmed by the very utterance of your words.'
            line53000()
            ch = 1
            ol[2] = -2
            ol[3] = 4
    elif obj == 15:
        #line9200()
        if cp != 8 or po == 1:
            print('nothing happens.')
        else:
            print('a portal has opened in the north wall!!')
            po = 1
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
def line10000(obj):
    global ol
    global cp
    global bf
    global fb
    print('10000 command')
    if j != 4:
        print("i wouldn't know how.")
    elif ol[1] != -1 and ol[1] != cp:
        line51000()
    elif bf == 0:
        print('the bucket is already empty')
    elif cp == 19:
        print('ok')
    elif cp != 10 or fb == 0:
        print('the water disappears quickly.')
        bf = 0
    else:
        print('congratulations! you have vanquished')
        print('the flames!')
        fb = 0
        bf = 0
        line699()
    line700()


# fill
def line11000(obj):
    global pt
    global cp
    global bf
    global pf
    print('11000 command')
    if obj == 0:
        line50000()
    elif pt[obj] == -1:
        print("that wouldn't hold anything.")
    elif fna(obj) != cp and fna(obj) != -1:
        line51000()
    elif obj != 4:
        print("that wouldn't hold anything.")
    elif bf == 1:
        print("it's already full.")
    elif cp == 25 and pf == 1:
        print("i'd rather stay away from the mercury.")
    elif cp != 23 and cp != 19:
        print("i don't see any water here.")
    else:
        print('your bucket is now full.')
        bf = 1
    line700()


# unlock object
def line12000(obj):
    global cp
    global ol
    print('12000 command')
    if obj == 0:
        line50000('what?')
    elif obj != 12 and obj != 27:
        print("i wouldn't know how to unlock one.")
        line700()
    elif cp != 0 and cp != 5 and cp != 6:
        line51000()
    elif cp == 0 and obj == 12:
        line12200()
    elif cp == 5 and obj == 27:
        line12300()
    elif cp != 6 or obj != 12 or ol[16] != -2:
        line51000()
    else:
        print('the trapdoor has no lock')
    line700()


def line12200():
    global du
    global ol
    if du == 1:
        print("it's already unlocked.")
        line700()
    elif ol[20] != -1:
        print('i need a key.')
        line700()
    else:
        print('the door easily unlocks and swings open.')
        du = 1
        line14000()


def line12300():
    global vo
    global fv
    global kc
    global rInt
    if vo == 1:
        print("it's already open.")
        line700()
    elif fv == 0:
        line51000()
    elif kc == 0:
        print('i don''t know the combination.')
        line700()
    else:
        print("ok, let's see.  12..35..6..")
        print('<click!> the door swings open.')
        vo = 1
        rInt[5][2] = 46
        line14000()


# look
def line14000():
    global in_str
    global cp
    in_str = f'you are in the {rStr[cp]}'
    line53000()
    line14010()


def line14010():
    for x in ol:
        if x == cp:
            global in_str
            in_str = f'there is a {om[x]} here'
            line53000()
        elif x == 1 and ol[1] == cp:
            print("the pool is full of water")
    if cp == 25:
        if pf == 1:
            print('the pool is full of liquid mercury')
        elif fb != 0:
            print('the pool''s empty')
            if ol[7] == 48:
                print('i see something shiny in the pool!')
    if cp == 10 and fb == 1:
        print('there is a hot fire on the south wall!')
        print('if I go that way I''ll burn to death!')
    if cp == 16:
        in_str = 'a rich, full voice says, ''ritnew is a charming world''.'
        line53000()
    if cp == 26:
        print('there is a valve on one of the pipes.')
    if cp == 23:
        print('there is a leaky faucet nearby.')
    if cp == 10 and fb == 0:
        print('there is evidence of a recent fire here.')
    if cp == 5 and fv == 1:
        print('there is a vault in the east wall.')
    if cp == 5 and vo == 1:
        print('the vault is open')
    if cp == 0 and du == 1:
        print('an open door leads north.')
    if cp != 48:
        print('obvious exits:')
        if rInt[cp][0] > 0:
            print('n ', end='')
        if rInt[cp][1] > 0:
            print('s ', end='')
        if rInt[cp][2] > 0:
            print('e ', end='')
        if rInt[cp][3] > 0:
            print('w ', end='')
        print('')
    line700()


# go
def line15000(obj):
    global cp
    global ol
    global in_str
    print('15000 command')
    if obj != 8 and obj != 18 and obj != 28:
        line50000('what?')
    elif (obj == 8 and cp != 48) or (obj == 18 and cp != 2 and cp != 27) or (obj == 28 and cp != 25):
        line51000()
    elif obj == 8:
        cp = 25
        line699()
    elif obj == 28 and pf == 1:
        print('the pool is full of mercury!')
        line700()
    elif obj == 28:
        cp = 48
        line700()
    elif cp == 27:
        cp = 2
        line699()
    elif ol[9] == -1:
        print('the suits of armor try to stop you,')
        print('but you fight them off with your sword.')
        cp = 27
        line699()
    else:
        in_str = 'the suits of armor prevent you from going up!'
        line53000()
        line700()


# north
def line16000():
    global cp
    global du
    global rInt
    if cp == 0 and du == 0:
        print('the door is locked shut.')
        line700()
    elif rInt[cp][0] == 0:
        line52000()
    elif cp == 0:
        print('the door slams shut behind you!')
    cp = rInt[cp][0]
    line14000()


# south
def line17000():
    global cp
    global fb
    print('17000 command')
    if cp == 10 and fb == 0:
        print('you have burnt to a crisp!')
        exit()

    if rInt[cp][1] == 0:
        line52000()
    else:
        cp = rInt[cp][1]
        line699()


# east
def line17010():
    global cp
    global ch
    global ps
    global d
    global rInt
    print('17010 command')
    if cp == 4 and ch == 0 and ps == 0:
        print('the snake is about to attack!')
        ps = 1
        line700()
    elif cp == 4 and ch == 0:
        print('the snake bites you!')
        print('you are dead.')
        exit()

    if rInt[cp][2] == 0:
        line52000()
    else:
        cp = rInt[cp][2]
        line699()


# west
def line19000():
    global cp
    global rInt
    print('19000 command')
    if rInt[cp][3] == 0:
        line52000()
    else:
        cp = rInt[cp][3]
        line699()


# score
def line20000():
    global gt
    global in_str
    print('20000 command')
    print('if you were to quit now,')
    print('you would have a score of')
    print(gt * 20, 'points.')
    print('(100 possible)')
    while True:
        print('do you indeed wish to quit now?')
        line60000()
        if in_str[0].lower() == 'y':
            line7010()
        elif in_str[0].lower() == 'n':
            print('ok')
            print()
            break
    line700()


# turn
def line21000(obj):
    global cp
    global in_str
    global pf
    global ol
    print('21000 command')
    if obj != 7:
        print("i don't know how to turn such a thing.")
        line699()
    elif cp != 26:
        line51000()
    else:
        in_str = 'with much effort, you turn the valve 5 times.  you hear the sound of liquid '
        line53000()
        print('flowing through the pipes.')
        pf = 1 - pf
        if pf == 0 and ol[7] == -3:
            ol[7] = 25
            line700()
        elif pf == 1 and ol[7] == 25:
            ol[7] = -3
            line700()
        else:
            line700()


# jump
def line22000():
    global cp
    global es
    global jm
    print('22000 command')
    if cp != 27 and cp != 29 and cp != 32:
        print("there's nowhere to jump.")
        line700()
    else:
        print('you jump..')
        if cp == 27:
            if jm == 1:
                print("now you've done it.  you ignored")
                print("my warning, and as a result")
                print("you have broken your neck!")
                print("you are dead.")
                exit()
            else:
                print('you have landed down-stairs,')
                print('and narrowly escaped serious')
                print("injury.  please don't try it again.")
                jm = 1
                cp = 2
                line699()
        if ol[14] == -1:
            print('there is no way to open the parachute!')
        elif ol[27] == -1:
            print('you yank the ripcord and the')
            print("'chute comes billowing out.")
            if cp == 32:
                cp = 40
                line699()
            else:
                print('you land safely')
                print('congratulations on escapting!')
                es = 1
                line7010()
        print('you hit the ground.')
        print("you have broken your neck!")
        print("you are dead.")
        exit()


# swim
def line24000():
    global cp
    global pf
    print('24000 command')
    if cp != 19 and cp != 25:
        print("there's nothing here to swim in!")
    elif cp == 19:
        print('the water is only a few inches deep.')
    elif pf == 1:
        print("in mercury?  no way!")
    else:
        print('the pool is empty.')
    line700()


# fix
def line25000(obj):
    global cp
    global ol
    global pt
    print('25000 command')
    if obj == 0:
        line50000('what')
    elif obj == 7:
        print("i ain't no plumber!")
    elif obj != 17:
        print("i wouldn't know how.")
    elif fna(obj) != cp and fna(obj) != -1:
        line51000()
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


def line50000(unknown_object):
    global em
    print(f'{unknown_object}?  {h[em]}')
    em = 1 - em
    line700()


def line51000():
    print("i don't see it here")
    line700()


def line52000():
    print("it's impossible to go that way.")
    line700()


def line53000():
    global in_str
    global screen_width
    if len(in_str) < screen_width:
        print(in_str)
    else:
        last_space_index = in_str.rfind(' ', 0, screen_width)
        print(in_str[:last_space_index])
        print(in_str[last_space_index + 1:])


def line60000():
    global in_str
    in_str = input()


def line60500():
    print('*' * 40)


def line62000():
    print(f'{program_name:>12} by m.j. lansing')
    print(f'   cursor # {cursor_issue}  copyright (c) 1981')
    line60500()
    print("explore the miser's house   (needs 16k)")
    print('\n\n\npress return to begin')
    wait_for_keypress()
    print('\n\none moment please...')
    line20()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    line0()
