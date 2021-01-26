# This is a Python port of the Miser's House BASIC adventure.

# useful functions
def clear_screen():
    pass

def wait_for_keypress():
    _ = input()

# variables
pg, nm = '', ''
ol = pt = []
wd = 0
rStr = ['']
rInt = [[]]
om = ol = []
v = o = pt = []
em = pf = fb = 0
h = []

def line0():
    global pg
    pg = 'miser'
    global nm
    nm = '27'
    line62000()

def fna(x):
    global ol
    global pt
    return ol[pt[x]]

def line20():
    global wd
    wd = 80
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
    h = ['what?', 'i don''t understand that']
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
    for (xx, yy) in r_int_r_str_data:
        rInt.append(xx)
        rStr.append(yy)

    v = ['get', 'take', 'move', 'slid', 'push', 'open', 'read', 'inve', 'quit']
    v += ['drop', 'say', 'pour', 'fill', 'unlo', 'lock']
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
    for (xx, yy) in o_pt_data:
        o.append(xx)
        pt.append(yy)

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
    for (xx, yy) in om_ol_data:
        om.append(xx)
        ol.append(yy)

    clear_screen()
    line14000()

def line14000():
    print('line 14000 - fix me');

def line60500():
    print(f'*')
    pass

def line62000():
    print(f'{pg:>12} by m.j. lansing')
    print(f'   cursor # {nm}  copyright (c) 1981')
    line60500()
    print('explore the miser''s house   (needs 16k)')
    print('\n\n\npress return to begin')
    wait_for_keypress()
    print('\n\none moment please...')
    line20()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    line0()

