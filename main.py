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

import miserLib


def main():
    miser = miserLib.Miser()
    miserLib.clear_screen()
    welcome_banner()
    miser.describe_current_position()
    miser.main_command_loop()


def welcome_banner():
    print(f'{miserLib.PROGRAM_NAME:>12} by m.j. lansing')
    print(f'   cursor # {miserLib.CURSOR_ISSUE}  copyright (c) 1981')
    print('*' * 40)
    print("explore the miser's house   (needs 16k)")
    print('\n\n\npress return to begin')
    miserLib.wait_for_keypress()
    print('\n\none moment please...')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
