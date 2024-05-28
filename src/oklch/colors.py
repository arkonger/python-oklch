# vim:foldmethod=indent:foldlevel=1
from .tools import find_cusp

import math

# Converts an int to a hex string
def _hex(i):
    return hex(i)[2:].upper()

# Rounds using the typical rule of [x.0, x.5) -> x; [x.5, x+1) -> x+1
def _round(f, nDigits=0):
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
# Rounds down to the given number of digits with no floating point weirdness
def _ceil(f, nDigits=0):
    f = math.ceil(f * 10**nDigits) / 10.**nDigits
    return float(format(f, '.' + str(nDigits) + 'f'))
# As above, but rounding up
def _floor(f, nDigits=0):
    f = math.floor(f * 10**nDigits) / 10.**nDigits
    return float(format(f, '.' + str(nDigits) + 'f'))

# The superclass is only used for type-checking and should not be used directly
class Color: 
    def to_RGB(self): 
        return RGB(0, 0, 0)
    def to_Hex(self):
        return Hex('#000000')
    def to_OKLCH(self):
        return OKLCH(0, 0, 0)

    def is_in_gamut(self): pass

    ColorDict = { \
        'MediumVioletRed':      '#C71585',
        'DeepPink':             '#FF1493',
        'PaleVioletRed':        '#DB7093',
        'HotPink':              '#FF69B4',
        'LightPink':            '#FFB6C1',
        'Pink':                 '#FFC0CB',
        'DarkRed':              '#8B0000',
        'Red':                  '#FF0000',
        'Firebrick':            '#B22222',
        'Crimson':              '#DC143C',
        'IndianRed':            '#CD5C5C',
        'LightCoral':           '#F08080',
        'Salmon':               '#FA8072',
        'DarkSalmon':           '#E9967A',
        'LightSalmon':          '#FFA07A',
        'OrangeRed':            '#FF4500',
        'Tomato':               '#FF6347',
        'DarkOrange':           '#FF8C00',
        'Coral':                '#FF7F50',
        'Orange':               '#FFA500',
        'DarkKhaki':            '#BDB76B',
        'Gold':                 '#FFD700',
        'Khaki':                '#F0E68C',
        'PeachPuff':            '#FFDAB9',
        'Yellow':               '#FFFF00',
        'PaleGoldenrod':        '#EEE8AA',
        'Moccasin':             '#FFE4B5',
        'PapayaWhip':           '#FFEFD5',
        'LightGoldenrodYellow': '#FAFAD2',
        'LemonChiffon':         '#FFFACD',
        'LightYellow':          '#FFFFE0',
        'Maroon':               '#800000',
        'Brown':                '#A52A2A',
        'SaddleBrown':          '#8B4513',
        'Sienna':               '#A0522D',
        'Chocolate':            '#D2691E',
        'DarkGoldenrod':        '#B8860B',
        'Peru':                 '#CD853F',
        'RosyBrown':            '#BC8F8F',
        'Goldenrod':            '#DAA520',
        'SandyBrown':           '#F4A460',
        'Tan':                  '#D2B48C',
        'Burlywood':            '#DEB887',
        'Wheat':                '#F5DEB3',
        'NavajoWhite':          '#FFDEAD',
        'Bisque':               '#FFE4C4',
        'BlanchedAlmond':       '#FFEBCD',
        'Cornsilk':             '#FFF8DC',
        'Indigo':               '#4B0082',
        'Purple':               '#800080',
        'DarkMagenta':          '#8B008B',
        'DarkViolet':           '#9400D3',
        'DarkSlateBlue':        '#483D8B',
        'BlueViolet':           '#8A2BE2',
        'DarkOrchid':           '#9932CC',
        'Fuchsia':              '#FF00FF',
        'Magenta':              '#FF00FF',
        'SlateBlue':            '#6A5ACD',
        'MediumSlateBlue':      '#7B68EE',
        'MediumOrchid':         '#BA55D3',
        'MediumPurple':         '#9370DB',
        'Orchid':               '#DA70D6',
        'Violet':               '#EE82EE',
        'Plum':                 '#DDA0DD',
        'Thistle':              '#D8BFD8',
        'Lavender':             '#E6E6FA',
        'MidnightBlue':         '#191970',
        'Navy':                 '#000080',
        'DarkBlue':             '#00008B',
        'MediumBlue':           '#0000CD',
        'Blue':                 '#0000FF',
        'RoyalBlue':            '#4169E1',
        'SteelBlue':            '#4682B4',
        'DodgerBlue':           '#1E90FF',
        'DeepSkyBlue':          '#00BFFF',
        'CornflowerBlue':       '#6495ED',
        'SkyBlue':              '#87CEEB',
        'LightSkyBlue':         '#87CEFA',
        'LightSteelBlue':       '#B0C4DE',
        'LightBlue':            '#ADD8E6',
        'PowderBlue':           '#B0E0E6',
        'Teal':                 '#008080',
        'DarkCyan':             '#008B8B',
        'LightSeaGreen':        '#20B2AA',
        'CadetBlue':            '#5F9EA0',
        'DarkTurquoise':        '#00CED1',
        'MediumTurquoise':      '#48D1CC',
        'Turquoise':            '#40E0D0',
        'Aqua':                 '#00FFFF',
        'Cyan':                 '#00FFFF',
        'Aquamarine':           '#7FFFD4',
        'PaleTurquoise':        '#AFEEEE',
        'LightCyan':            '#E0FFFF',
        'DarkGreen':            '#006400',
        'Green':                '#008000',
        'DarkOliveGreen':       '#556B2F',
        'ForestGreen':          '#228B22',
        'SeaGreen':             '#2E8B57',
        'Olive':                '#808000',
        'OliveDrab':            '#6B8E23',
        'MediumSeaGreen':       '#3CB371',
        'LimeGreen':            '#32CD32',
        'Lime':                 '#00FF00',
        'SpringGreen':          '#00FF7F',
        'MediumSpringGreen':    '#00FA9A',
        'DarkSeaGreen':         '#8FBC8F',
        'MediumAquamarine':     '#66CDAA',
        'YellowGreen':          '#9ACD32',
        'LawnGreen':            '#7CFC00',
        'Chartreuse':           '#7FFF00',
        'LightGreen':           '#90EE90',
        'GreenYellow':          '#ADFF2F',
        'PaleGreen':            '#98FB98',
        'MistyRose':            '#FFE4E1',
        'AntiqueWhite':         '#FAEBD7',
        'Linen':                '#FAF0E6',
        'Beige':                '#F5F5DC',
        'WhiteSmoke':           '#F5F5F5',
        'LavenderBlush':        '#FFF0F5',
        'OldLace':              '#FDF5E6',
        'AliceBlue':            '#F0F8FF',
        'Seashell':             '#FFF5EE',
        'GhostWhite':           '#F8F8FF',
        'Honeydew':             '#F0FFF0',
        'FloralWhite':          '#FFFAF0',
        'Azure':                '#F0FFFF',
        'MintCream':            '#F5FFFA',
        'Snow':                 '#FFFAFA',
        'Ivory':                '#FFFFF0',
        'White':                '#FFFFFF',
        'Black':                '#000000',
        'DarkSlateGray':        '#2F4F4F',
        'DimGray':              '#696969',
        'SlateGray':            '#708090',
        'Gray':                 '#808080',
        'LightSlateGray':       '#778899',
        'DarkGray':             '#A9A9A9',
        'Silver':               '#C0C0C0',
        'LightGray':            '#D3D3D3',
        'Gainsboro':            '#DCDCDC'
    }

# RGB colors represented as triplets
class RGB(Color):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return "rgb({}, {}, {})".format(self.r, self.g, self.b)

    def to_Hex(self):
        return Hex("#{:0>2}{:0>2}{:0>2}".format(
                _hex(self.r),
                _hex(self.g),
                _hex(self.b)))

    def to_OKLCH(self):
        l = 0.4122214708 * OKLCH._f_inv(self.r/255) + \
            0.5363325363 * OKLCH._f_inv(self.g/255) + \
            0.0514459929 * OKLCH._f_inv(self.b/255)
        m = 0.2119034982 * OKLCH._f_inv(self.r/255) + \
            0.6806995451 * OKLCH._f_inv(self.g/255) + \
            0.1073969566 * OKLCH._f_inv(self.b/255)
        s = 0.0883024619 * OKLCH._f_inv(self.r/255) + \
            0.2817188376 * OKLCH._f_inv(self.g/255) + \
            0.6299787005 * OKLCH._f_inv(self.b/255)

        l_ = math.pow(l, 1/3)
        m_ = math.pow(m, 1/3)
        s_ = math.pow(s, 1/3)

        return OKLCH._polarize(
            0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_,
            1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_,
            0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_)

    # Check whether the color is in-gamut
    def is_in_gamut(self):
        return max(self.r, self.g, self.b) <= 255 and \
                min(self.r, self.g, self.b) >= 0

# RGB colors represented as hex code
class Hex(Color):
    def __init__(self, hex_code):
        if not hex_code[0] == '#':
            hex_code = '#' + hex_code
        self.hex_code = hex_code.upper()

    def __str__(self):
        return self.hex_code

    def to_RGB(self):
        return RGB(
            int(self.hex_code[1:3], 16),
            int(self.hex_code[3:5], 16),
            int(self.hex_code[5:7], 16))

    def to_OKLCH(self):
        return self.to_RGB().to_OKLCH()

    # Check whether the color is in-gamut
    def is_in_gamut(self):
        return self.to_RGB().is_in_gamut()

# OKLCH colors represented as triplets
class OKLCH(Color):
    def __init__(self, l, c, h):
        self.l = l
        self.c = c
        self.h = h

    def __str__(self):
        return "oklch({}, {}, {})".format(self.l, self.c, self.h)

    # Functions for converting to linear RGB from standard RGB and vice versa
    @staticmethod
    def _f(x):
        if (x >= 0.0031308):
            return (1.055) * math.pow(x, 1.0/2.4) - 0.055
        else:
            return 12.92 * x
    @staticmethod
    def _f_inv(x):
        if (x >= 0.04045):
            return math.pow((x + 0.055)/(1 + 0.055), 2.4)
        else:
            return x / 12.92

    # Convert from OKLAB
    @staticmethod
    def _polarize(l, a, b):
        c = math.pow(a*a + b*b, 1/2)
        h = math.degrees(math.atan2(b, a))
        if h < 0:
            h += 360

        return OKLCH(l, c, h)
    # Convert back to rectangular coords; this function leaves a&b normalized
    @staticmethod
    def _rect_normal(hue):
        a = math.cos(math.radians(hue))
        b = math.sin(math.radians(hue))

        return a, b
    # Multiply by c to get OKLAB components
    def _rect(self):
        a, b = self._rect_normal(self.h)

        return a * self.c, b * self.c

    def to_RGB(self):
        a, b = self._rect()

        l_ = self.l + 0.3963377774 * a + 0.2158037573 * b
        m_ = self.l - 0.1055613458 * a - 0.0638541728 * b
        s_ = self.l - 0.0894841775 * a - 1.2914855480 * b

        l = l_*l_*l_
        m = m_*m_*m_
        s = s_*s_*s_

        return RGB(
            _round(OKLCH._f(+4.0767416621 * l \
                    - 3.3077115913 * m \
                    + 0.2309699292 * s) * 255),
            _round(OKLCH._f(-1.2684380046 * l \
                    + 2.6097574011 * m \
                    - 0.3413193965 * s) * 255),
            _round(OKLCH._f(-0.0041960863 * l \
                    - 0.7034186147 * m \
                    + 1.7076147010 * s) * 255))

    def to_Hex(self):
        return self.to_RGB().to_Hex()

    # Check whether the color is in-gamut
    def is_in_gamut(self):
        return self.to_RGB().is_in_gamut()

    # Returns a css string which rounds in such a way as to guarantee an
    #   in-gamut color (presuming the original color was in-gamut, of course)
    def css_string(self):
        # Find which way is safe to round l
        cusp = find_cusp(hue=self.h)
        if self.l > cusp.l:
            l = _floor(self.l, 4)
        else:
            l = _ceil(self.l, 4)

        # Always safe to floor c
        c = _floor(self.c, 3)

        # Doesn't matter how h is rounded; it can go directly in format string
        return "oklch({:.2%} {:.3f} {:.2f})".format(l, c, self.h)
