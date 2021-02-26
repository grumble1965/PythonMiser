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
    win_ui = miserLib.WindowsConsoleUserInterface()
    miser = miserLib.Miser(win_ui)
    win_ui.clear_screen()
    miserLib.welcome_banner(win_ui)
    miser.describe_current_position()
    miser.main_command_loop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
