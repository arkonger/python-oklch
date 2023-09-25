import math

def _hex(i):
    return hex(i)[2:].upper()

def _round(f, nDigits=0):
    f *= 10**nDigits

    i = int(f)
    mod = f - i

    if (mod >= 0.5):
        return (i+1) / (10**nDigits)
    else:
        return i / (10**nDigits)

# RGB colors represented as triplets
class RGB:
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

# RGB colors represented as hex code
class Hex:
    def __init__(self, hex_code):
        self.hex_code = hex_code

    def __str__(self):
        return self.hex_code

    def to_RGB(self):
        return RGB(
            int(self.hex_code[1:3], 16),
            int(self.hex_code[3:5], 16),
            int(self.hex_code[5:7], 16))

    def to_OKLCH(self):
        return self.to_RGB().to_OKLCH()

# OKLCH colors represented as triplets
class OKLCH:
    def __init__(self, l, c, h):
        self.l = l
        self.c = c
        self.h = h

    def __str__(self):
        return "oklch({}, {}, {})".format(self.l, self.c, self.h)

    # Functions for converting to linear RGB from standard RGB and vice versa
    def _f(x):
        if (x >= 0.0031308):
            return (1.055) * math.pow(x, 1.0/2.4) - 0.055
        else:
            return 12.92 * x
    def _f_inv(x):
        if (x >= 0.04045):
            return math.pow((x + 0.055)/(1 + 0.055), 2.4)
        else:
            return x / 12.92

    def _polarize(l, a, b):
        c = math.pow(a*a + b*b, 1/2)
        h = math.degrees(math.atan2(b, a))
        if h < 0:
            h += 360

        return OKLCH(l, c, h)

    def to_RGB(self):
        a = self.c * math.cos(math.radians(self.h))
        b = self.c * math.sin(math.radians(self.h))

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

    def to_css_string(self):
        return "oklch({:.2%} {:.3f} {:.2f})".format(self.l, self.c, self.h)
