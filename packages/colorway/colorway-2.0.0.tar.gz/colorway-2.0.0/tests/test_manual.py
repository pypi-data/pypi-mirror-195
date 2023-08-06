import colorway_manual as format

def test_format_clear():
    assert format.format.clear == '\x1b[0m'

def test_foreground_black():
    assert format.foreground.black == '\x1b[0;30m'

def test_foreground_red():
    assert format.foreground.red == '\x1b[0;31m'

def test_foreground_green():
    assert format.foreground.green == '\x1b[0;32m'

def test_foreground_yellow():
    assert format.foreground.yellow == '\x1b[0;33m'

def test_foreground_blue():
    assert format.foreground.blue == '\x1b[0;34m'

def test_foreground_purple():
    assert format.foreground.purple == '\x1b[0;35m'

def test_foreground_cyan():
    assert format.foreground.cyan == '\x1b[0;36m'

def test_foreground_white():
    assert format.foreground.white == '\x1b[0;37m'

##

def test_foreground_bold_black():
    assert format.foreground.bold.black == '\x1b[1;30m'

def test_foreground_bold_red():
    assert format.foreground.bold.red == '\x1b[1;31m'

def test_foreground_bold_green():
    assert format.foreground.bold.green == '\x1b[1;32m'

def test_foreground_bold_yellow():
    assert format.foreground.bold.yellow == '\x1b[1;33m'

def test_foreground_bold_blue():
    assert format.foreground.bold.blue == '\x1b[1;34m'

def test_foreground_bold_purple():
    assert format.foreground.bold.purple == '\x1b[1;35m'

def test_foreground_bold_cyan():
    assert format.foreground.bold.cyan == '\x1b[1;36m'

def test_foreground_bold_white():
    assert format.foreground.bold.white == '\x1b[1;37m'

##

def test_foreground_underline_black():
    assert format.foreground.underline.black == '\x1b[4;30m'

def test_foreground_underline_red():
    assert format.foreground.underline.red == '\x1b[4;31m'

def test_foreground_underline_green():
    assert format.foreground.underline.green == '\x1b[4;32m'

def test_foreground_underline_yellow():
    assert format.foreground.underline.yellow == '\x1b[4;33m'

def test_foreground_underline_blue():
    assert format.foreground.underline.blue == '\x1b[4;34m'

def test_foreground_underline_purple():
    assert format.foreground.underline.purple == '\x1b[4;35m'

def test_foreground_underline_cyan():
    assert format.foreground.underline.cyan == '\x1b[4;36m'

def test_foreground_underline_white():
    assert format.foreground.underline.white == '\x1b[4;37m'

##

def test_foreground_highintensity_black():
    assert format.foreground.highintensity.black == '\x1b[0;90m'

def test_foreground_highintensity_red():
    assert format.foreground.highintensity.red == '\x1b[0;91m'

def test_foreground_highintensity_green():
    assert format.foreground.highintensity.green == '\x1b[0;92m'

def test_foreground_highintensity_yellow():
    assert format.foreground.highintensity.yellow == '\x1b[0;93m'

def test_foreground_highintensity_blue():
    assert format.foreground.highintensity.blue == '\x1b[0;94m'

def test_foreground_highintensity_purple():
    assert format.foreground.highintensity.purple == '\x1b[0;95m'

def test_foreground_highintensity_cyan():
    assert format.foreground.highintensity.cyan == '\x1b[0;96m'

def test_foreground_highintensity_white():
    assert format.foreground.highintensity.white == '\x1b[0;97m'

##

def test_foreground_highintensity_bold_black():
    assert format.foreground.highintensity.bold.black == '\x1b[1;90m'

def test_foreground_highintensity_bold_red():
    assert format.foreground.highintensity.bold.red == '\x1b[1;91m'

def test_foreground_highintensity_bold_green():
    assert format.foreground.highintensity.bold.green == '\x1b[1;92m'

def test_foreground_highintensity_bold_yellow():
    assert format.foreground.highintensity.bold.yellow == '\x1b[1;93m'

def test_foreground_highintensity_bold_blue():
    assert format.foreground.highintensity.bold.blue == '\x1b[1;94m'

def test_foreground_highintensity_bold_purple():
    assert format.foreground.highintensity.bold.purple == '\x1b[1;95m'

def test_foreground_highintensity_bold_cyan():
    assert format.foreground.highintensity.bold.cyan == '\x1b[1;96m'

def test_foreground_highintensity_bold_white():
    assert format.foreground.highintensity.bold.white == '\x1b[1;97m'

##

def test_foreground_custom():
    assert format.foreground.custom(1,2,3) == '\x1b[38;2;1;2;3m'

##

def test_background_black():
    assert format.background.black == '\x1b[40m'

def test_background_red():
    assert format.background.red == '\x1b[41m'

def test_background_green():
    assert format.background.green == '\x1b[42m'

def test_background_yellow():
    assert format.background.yellow == '\x1b[43m'

def test_background_blue():
    assert format.background.blue == '\x1b[44m'

def test_background_purple():
    assert format.background.purple == '\x1b[45m'

def test_background_cyan():
    assert format.background.cyan == '\x1b[46m'

def test_background_white():
    assert format.background.white == '\x1b[47m'

##

def test_background_highintensity_black():
    assert format.background.highintensity.black == '\x1b[0;100m'

def test_background_highintensity_red():
    assert format.background.highintensity.red == '\x1b[0;101m'

def test_background_highintensity_green():
    assert format.background.highintensity.green == '\x1b[0;102m'

def test_background_highintensity_yellow():
    assert format.background.highintensity.yellow == '\x1b[0;103m'

def test_background_highintensity_blue():
    assert format.background.highintensity.blue == '\x1b[0;104m'

def test_background_highintensity_purple():
    assert format.background.highintensity.purple == '\x1b[0;105m'

def test_background_highintensity_cyan():
    assert format.background.highintensity.cyan == '\x1b[0;106m'

def test_background_highintensity_white():
    assert format.background.highintensity.white == '\x1b[0;107m'

##

def test_background_custom():
    assert format.background.custom(1,2,3) == '\x1b[48;2;1;2;3m'