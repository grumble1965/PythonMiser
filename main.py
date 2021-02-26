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


class GameUI(miserLib.IUserInterface):
    @staticmethod
    def mp(*args, sep=' ', end='\n'):
        if len(args) == 0:
            print(end=end)
        else:
            for arg in args:
                print(arg, end=sep)
            print(end=end)


def main():
    ui = GameUI()
    miser = miserLib.Miser(ui)
    miserLib.clear_screen()
    welcome_banner(ui)
    miser.describe_current_position()
    miser.main_command_loop()


def welcome_banner(ui):
    ui.mp(f'{miserLib.PROGRAM_NAME:>12} by m.j. lansing')
    ui.mp(f'   cursor # {miserLib.CURSOR_ISSUE}  copyright (c) 1981')
    ui.mp('*' * 40)
    ui.mp("explore the miser's house   (needs 16k)")
    ui.mp('\n\n\npress return to begin')
    miserLib.wait_for_keypress()
    ui.mp('\n\none moment please...')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
