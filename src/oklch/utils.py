# vim:foldmethod=indent:foldlevel=1

# TODO: __all__

import math

from oklch import colors


# Converts an int to a hex string
def int_to_hex_string(i):
    return hex(i)[2:].upper()


# Rounds using the typical rule of [x.0, x.5) -> x; [x.5, x+1) -> x+1
def round_(f, nDigits=0):
    f *= 10**nDigits

    i = int(f)
    mod = f - i
    if (mod >= 0.5):
        i += 1

    if nDigits:
        i /= (10.**nDigits)
        return float(format(i, '.' + str(nDigits) + 'f'))
    else:
        return i


# Rounds down to the given number of digits with no floating point
# weirdness
def ceil_(f, nDigits=0):
    f = math.ceil(f * 10**nDigits) / 10.**nDigits
    return float(format(f, '.' + str(nDigits) + 'f'))


# As above, but rounding up
def floor_(f, nDigits=0):
    f = math.floor(f * 10**nDigits) / 10.**nDigits
    return float(format(f, '.' + str(nDigits) + 'f'))


# Prints a color to terminal by setting the terminal background to that
# color using ANSI control codes
def print_to_term(color, CR=True):
    # If the color is a list or tuple, we recurse through
    if isinstance(color, (list, tuple)):
        for c in color:
            if isinstance(c, (list, tuple)):
                print_to_term(c, CR)
            else:
                print_to_term(c, False)
        if CR:
            print('')
        return
    else:
        expect_color(color)
        color = color.to_RGB()
        # If the color is out-of-gamut, we print magenta instead to
        # indicate an error
        if not color.is_in_gamut():
            color = colors.RGB(0xFF, 0x00, 0xFF)

    # 0x1b is an ANSI control code
    print("\x1b[48;2;{};{};{}m \x1b[0m".format(
            color.r,
            color.g,
            color.b),
        end = '')
    if CR:
        print('')


# Checks that arg is color or raise ValueError
def expect_color(arg):
    if not isinstance(arg, colors.Color):
        raise ValueError(f"Expected color, received '{type(arg)}'!")
