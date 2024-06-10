# vim:foldmethod=indent:foldlevel=1
from .tools import find_cusp

import math
from random import choice
from sys import maxsize
import heapq

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
    # These return a dummy color just so to eliminate an annoying warning. 
    def to_RGB(self): 
        return RGB(0, 0, 0)
    def to_HEX(self):
        return HEX('#000000')
    def to_OKLAB(self):
        return OKLAB(0, 0, 0)
    def to_OKLCH(self):
        return OKLCH(0, 0, 0)

    def is_in_gamut(self):
        return self.to_RGB().is_in_gamut()

    def __str__(self): return ""

    # Checks that arg is color
    @staticmethod
    def _is_color(arg):
        if not isinstance(arg, Color):
            raise ValueError(f"Expected color, received '{type(arg)}'!")
    # Checks that two colors are close
    def is_close(self, other):
        return self.to_HEX().hex_code == other.to_HEX().hex_code
    # Addition gives the midpoint of the two colors in OKLAB space
    def __add__(self, other):
        self._is_color(other)

        return self.to_OKLAB() + other.to_OKLAB()
    # Negation gives the complement in OKLAB space
    def __neg__(self):
        return self.to_OKLAB().__neg__()
    # Subtraction gives the midpoint of self and complement of other
    def __sub__(self, other):
        self._is_color(other)

        return self.to_OKLAB() - other.to_OKLAB()

    # Pipe operator yields the euclidean distance between two colors
    def __or__(self, other):
        self._is_color(other)

        # Convert both colors to oklab:
        self = self.to_OKLAB()
        other = other.to_OKLAB()

        return math.pow((self.l - other.l) ** 2 \
                            + (self.a - other.a) ** 2 \
                            + (self.b - other.b) ** 2,
                        0.5)

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

    @staticmethod
    def get_web_color(color_name):
        return HEX(Color.ColorDict[color_name])
    @staticmethod
    def get_random_web_color():
        name = choice(list(Color.ColorDict.keys()))
        return name, Color.get_web_color(name)
    @staticmethod
    def get_nearest_web_color(color, n=1):
        if not isinstance(color, Color):
            raise ValueError(f"Expected color, received '{type(color)}'!")
        if not (isinstance(n, int) and n > 0):
            raise ValueError("Expected a positive integer," \
                                + f" received '{type(n)}'!")
        color = color.to_OKLCH()

        # When n == 1, we can get the result faster by skipping the heap
        if n == 1:
            ret = (maxsize, None, None)
            for k, v in Color.ColorDict.items():
                c = HEX(v).to_OKLCH()
                ret = min(ret, (color | c, k, c))
            return (ret[1], ret[2])
        else:
            # Build minheap of the web colors by distance
            heap = []
            for k, v in Color.ColorDict.items():
                c = HEX(v).to_OKLCH()
                heapq.heappush(heap, (color | c, k, c))

            ret = []
            for _ in range(n):
                t = heapq.heappop(heap)
                ret.append((t[1], t[2]))
            return ret

###############################################################################
#
# Original license for:
#   - RGB.to_OKLAB()
#   - RGB._srgb_transfer_function()
#   - RGB._srgb_transfer_function_inv()
#   - OKLAB.to_RGB()
#
#   Copyright (c) 2021 Björn Ottosson
#   
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#   
#       The above copyright notice and this permission notice shall be
#       included in all copies or substantial portions of the Software.
#   
#       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#       EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#       MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#       IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#       CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#       TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#       SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
###############################################################################

# RGB colors represented as triplets
class RGB(Color):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return "rgb({}, {}, {})".format(self.r, self.g, self.b)

    def is_close(self, other):
        return super().is_close(other)
    # Return type for addition and subtraction is type of first operand
    def __add__(self, other):
        return super().__add__(other).to_RGB()
    def __neg__(self):
        return super().__neg__().to_RGB()
    def __sub__(self, other):
        return super().__sub__(other).to_RGB()

    def __or__(self, other):
        return super().__or__(other)

    # Type Conversions
    def to_RGB(self):
        return self
    def to_HEX(self):
        return HEX("#{:0>2}{:0>2}{:0>2}".format(
                _hex(self.r),
                _hex(self.g),
                _hex(self.b)))

    # Functions for converting to linear RGB from standard RGB and vice versa
    @staticmethod
    def _srgb_transfer_function(x):
        if (x >= 0.0031308):
            return (1.055) * math.pow(x, 1.0/2.4) - 0.055
        else:
            return 12.92 * x
    @staticmethod
    def _srgb_transfer_function_inv(x):
        if (x >= 0.04045):
            return math.pow((x + 0.055)/(1 + 0.055), 2.4)
        else:
            return x / 12.92

    def to_OKLAB(self):
        l = 0.4122214708 * self._srgb_transfer_function_inv(self.r/255) \
                + 0.5363325363 * self._srgb_transfer_function_inv(self.g/255) \
                + 0.0514459929 * self._srgb_transfer_function_inv(self.b/255)
        m = 0.2119034982 * self._srgb_transfer_function_inv(self.r/255) \
                + 0.6806995451 * self._srgb_transfer_function_inv(self.g/255) \
                + 0.1073969566 * self._srgb_transfer_function_inv(self.b/255)
        s = 0.0883024619 * self._srgb_transfer_function_inv(self.r/255) \
                + 0.2817188376 * self._srgb_transfer_function_inv(self.g/255) \
                + 0.6299787005 * self._srgb_transfer_function_inv(self.b/255)

        l_ = math.pow(l, 1/3)
        m_ = math.pow(m, 1/3)
        s_ = math.pow(s, 1/3)

        return OKLAB(
            0.2104542553*l_ + 0.7936177850*m_ - 0.0040720468*s_,
            1.9779984951*l_ - 2.4285922050*m_ + 0.4505937099*s_,
            0.0259040371*l_ + 0.7827717662*m_ - 0.8086757660*s_)
    def to_OKLCH(self):
        return self.to_OKLAB().to_OKLCH()

    # Check whether the color is in-gamut
    def is_in_gamut(self):
        return max(self.r, self.g, self.b) <= 255 and \
                min(self.r, self.g, self.b) >= 0

# RGB colors represented as hex code
class HEX(Color):
    def __init__(self, hex_code):
        if not hex_code[0] == '#':
            hex_code = '#' + hex_code
        self.hex_code = hex_code.upper()

    def __str__(self):
        return self.hex_code

    def is_close(self, other):
        return super().is_close(other)
    # Return type for addition and subtraction is type of first operand, unless
    #   the result is an invalid color, as this could result in a mangled hex
    #   code which is ambiguous. Therefore, these are left as RGB. 
    # The below function sorts this out:
    @staticmethod
    def __get_valid_hex_or_rgb(color):
        if color.is_in_gamut():
            return color.to_HEX()
        else: return color.to_RGB()
    def __add__(self, other):
        return self.__get_valid_hex_or_rgb(super().__add__(other))
    def __neg__(self):
        return self.__get_valid_hex_or_rgb(super().__neg__())
    def __sub__(self, other):
        return self.__get_valid_hex_or_rgb(super().__sub__(other))

    def __or__(self, other):
        return super().__or__(other)

    # Type Conversions
    def to_RGB(self):
        return RGB(
            int(self.hex_code[1:3], 16),
            int(self.hex_code[3:5], 16),
            int(self.hex_code[5:7], 16))
    def to_HEX(self):
        return self
    def to_OKLAB(self):
        return self.to_RGB().to_OKLAB()
    def to_OKLCH(self):
        return self.to_RGB().to_OKLCH()

    # Check whether the color is in-gamut
    def is_in_gamut(self):
        return super().is_in_gamut()

# OKLAB colors represented as triplets
class OKLAB(Color):
    def __init__(self, l, a, b):
        self.l = l
        self.a = a
        self.b = b

    def __str__(self):
        return f"oklab({self.l}, {self.a}, {self.b})"

    def is_close(self, other):
        return super().is_close(other)
    # Return type for addition and subtraction is type of first operand
    def __add__(self, other):
        l = 0.5*(self.l + other.l)
        a = 0.5*(self.a + other.a)
        b = 0.5*(self.b + other.b)

        return OKLAB(l, a, b)
    def __neg__(self):
        return OKLAB(1-self.l, -self.a, -self.b)
    def __sub__(self, other):
        return self + other.__neg__()

    def __or__(self, other):
        return super().__or__(other)

    # Type Conversions
    def to_RGB(self):
        l_ = self.l + 0.3963377774 * self.a + 0.2158037573 * self.b
        m_ = self.l - 0.1055613458 * self.a - 0.0638541728 * self.b
        s_ = self.l - 0.0894841775 * self.a - 1.2914855480 * self.b

        l = l_*l_*l_
        m = m_*m_*m_
        s = s_*s_*s_

        return RGB(
            _round(RGB._srgb_transfer_function(+4.0767416621 * l \
                    - 3.3077115913 * m \
                    + 0.2309699292 * s) * 255),
            _round(RGB._srgb_transfer_function(-1.2684380046 * l \
                    + 2.6097574011 * m \
                    - 0.3413193965 * s) * 255),
            _round(RGB._srgb_transfer_function(-0.0041960863 * l \
                    - 0.7034186147 * m \
                    + 1.7076147010 * s) * 255))
    def to_HEX(self):
        return self.to_RGB().to_HEX()
    def to_OKLAB(self):
        return self
    def to_OKLCH(self):
        c = math.pow(self.a ** 2 + self.b ** 2, 0.5)
        h = math.degrees(math.atan2(self.b, self.a))
        if h < 0:
            h += 360

        return OKLCH(self.l, c, h)

    def is_in_gamut(self):
        return super().is_in_gamut()

# OKLCH colors represented as triplets
class OKLCH(Color):
    def __init__(self, l, c, h):
        self.l = l
        self.c = c
        self.h = h

    def __str__(self):
        return "oklch({}, {}, {})".format(self.l, self.c, self.h)

    def is_close(self, other):
        return super().is_close(other)
    # Return type for addition and subtraction is type of first operand
    def __add__(self, other):
        return super().__add__(other).to_OKLCH()
    def __neg__(self):
        return super().__neg__().to_OKLCH()
    def __sub__(self, other):
        return super().__sub__(other).to_OKLCH()

    def __or__(self, other):
        return super().__or__(other)

    # Type Conversions
    def to_RGB(self):
        return self.to_OKLAB().to_RGB()
    def to_HEX(self):
        return self.to_RGB().to_HEX()

    @staticmethod
    def _get_normalized_ab(hue):
        a = math.cos(math.radians(hue))
        b = math.sin(math.radians(hue))

        return a, b
    def to_OKLAB(self):
        a, b = self._get_normalized_ab(self.h)

        return OKLAB(self.l, a * self.c, b * self.c)
    def to_OKLCH(self):
        return self

    # Check whether the color is in-gamut
    def is_in_gamut(self):
        return super().is_in_gamut()

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
