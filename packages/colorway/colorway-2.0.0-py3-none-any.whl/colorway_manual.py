"""
Colorway
https://github.com/xhelphin/colorway

Python package to change the text color of the python console.

Manual formatting package
"""

# Import and call os.system to initialise color support on windows
from multiprocessing.sharedctypes import Value
import os
if os.name == 'nt':
    os.system("")

class format:
    """
    Class for misc formatting codes
    """
    clear = "\033[0m"

class foreground:
    """
    Class for foreground formatting codes
    """

    black = "\033[0;30m"
    red = "\033[0;31m"
    green = "\033[0;32m"
    yellow = "\033[0;33m"
    blue = "\033[0;34m"
    purple = "\033[0;35m"
    cyan = "\033[0;36m"
    white = "\033[0;37m"

    class bold:
        black = "\033[1;30m"
        red = "\033[1;31m"
        green = "\033[1;32m"
        yellow = "\033[1;33m"
        blue = "\033[1;34m"
        purple = "\033[1;35m"
        cyan = "\033[1;36m"
        white = "\033[1;37m"

    class underline:
        black = "\033[4;30m"
        red = "\033[4;31m"
        green = "\033[4;32m"
        yellow = "\033[4;33m"
        blue = "\033[4;34m"
        purple = "\033[4;35m"
        cyan = "\033[4;36m"
        white = "\033[4;37m"

    class highintensity:
        black = "\033[0;90m"
        red = "\033[0;91m"
        green = "\033[0;92m"
        yellow = "\033[0;93m"
        blue = "\033[0;94m"
        purple = "\033[0;95m"
        cyan = "\033[0;96m"
        white = "\033[0;97m"

        class bold:
            black = "\033[1;90m"
            red = "\033[1;91m"
            green = "\033[1;92m"
            yellow = "\033[1;93m"
            blue = "\033[1;94m"
            purple = "\033[1;95m"
            cyan = "\033[1;96m"
            white = "\033[1;97m"

    def custom(red, green, blue):
        """
        Return a formatting code for a custom color
        Arguments:
        - red -> integer 0 to 255
        - green -> integer 0 to 255
        - blue -> integer 0 to 255
        """
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
            if red < 0 or red > 255:
                raise ValueError
            if green < 0 or green > 255:
                raise ValueError
            if blue < 0 or blue > 255:
                raise ValueError
        except ValueError:
            print("Colorways: Arguments red, green & blue need to be integers between 0 and 255.")
        else:
            return f"\033[38;2;{red};{green};{blue}m"

class background:
    """
    Class for background formatting codes
    """

    black = "\033[40m"
    red = "\033[41m"
    green = "\033[42m"
    yellow = "\033[43m"
    blue = "\033[44m"
    purple = "\033[45m"
    cyan = "\033[46m"
    white = "\033[47m"

    class highintensity:
        black = "\033[0;100m"
        red = "\033[0;101m"
        green = "\033[0;102m"
        yellow = "\033[0;103m"
        blue = "\033[0;104m"
        purple = "\033[0;105m"
        cyan = "\033[0;106m"
        white = "\033[0;107m"

    def custom(red, green, blue):
        """
        Return a formatting code for a custom color
        Arguments:
        - red -> integer 0 to 255
        - green -> integer 0 to 255
        - blue -> integer 0 to 255
        """
        try:
            red = int(red)
            green = int(green)
            blue = int(blue)
            if red < 0 or red > 255:
                raise ValueError
            if green < 0 or green > 255:
                raise ValueError
            if blue < 0 or blue > 255:
                raise ValueError
        except ValueError:
            print("Colorways: Arguments red, green & blue need to be integers between 0 and 255.")
        else:
            return f"\033[48;2;{red};{green};{blue}m"