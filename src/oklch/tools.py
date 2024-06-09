# vim:foldmethod=indent:foldlevel=1
from . import colors

import math
import sys

# Prints a color to terminal by setting the terminal background to that color
#   using ANSI control codes
def _print_to_term(color, CR=True):
    if isinstance(color, (list, tuple)):
        for c in color:
            if isinstance(c, (list, tuple)):
                _print_to_term(c, CR)
            else:
                _print_to_term(c, False)
        if CR:
            print('')
        return
    elif not isinstance(color, colors.RGB):
        color = color.to_RGB()
    # 0x1b is an ANSI control code
    print("\x1b[48;2;{};{};{}m \x1b[0m".format(
            color.r,
            color.g,
            color.b),
        end = '')
    if CR:
        print('')

# Several of the below functions are sourced from Björn Ottosson's blog posts
#   which originally defined the OKLAB & OKLCH color spaces. For full
#   information on how these functions work, you should read those posts. Other
#   than translation, I have made only minimal changes to them. 
#
# The original code can be found at:
# https://bottosson.github.io/posts/gamutclipping/
#   and the original license for _max_saturation(), find_cusp(), and
#   _find_gamut_intersection() is printed below:
#
###############################################################################
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

def _max_saturation(a, b):
    # Max saturation will be when one of r, g or b goes below zero.
    
    # Select different coefficients depending on which component goes below
    #   zero first
    if (-1.88170328 * a - 0.80936493 * b > 1):
        # Red component
        k0 = +1.19086277
        k1 = +1.76576728
        k2 = +0.59662641
        k3 = +0.75515197
        k4 = +0.56771245

        wl = +4.0767416621
        wm = -3.3077115913
        ws = +0.2309699292

    elif (1.81444104 * a - 1.19445276 * b > 1):
        # Green component
        k0 = +0.73956515
        k1 = -0.45954404
        k2 = +0.08285427
        k3 = +0.12541070
        k4 = +0.14503204

        wl = -1.2684380046
        wm = +2.6097574011
        ws = -0.3413193965

    else:
        # Blue component
        k0 = +1.35733652
        k1 = -0.00915799
        k2 = -1.15130210
        k3 = -0.50559606
        k4 = +0.00692167

        wl = -0.0041960863
        wm = -0.7034186147
        ws = +1.7076147010


    # Approximate max saturation using a polynomial:
    S = k0 + k1 * a + k2 * b + k3 * a * a + k4 * a * b

    # Do one step Halley's method to get closer
    # this gives an error less than 10e6, except for some blue hues where the
    #   dS/dh is close to infinite
    # this should be sufficient for most applications, otherwise do two/three
    #   steps 

    k_l = +0.3963377774 * a + 0.2158037573 * b
    k_m = -0.1055613458 * a - 0.0638541728 * b
    k_s = -0.0894841775 * a - 1.2914855480 * b

    # while True:
    l_ = 1. + S * k_l
    m_ = 1. + S * k_m
    s_ = 1. + S * k_s

    l = l_ * l_ * l_
    m = m_ * m_ * m_
    s = s_ * s_ * s_

    l_dS = 3. * k_l * l_ * l_
    m_dS = 3. * k_m * m_ * m_
    s_dS = 3. * k_s * s_ * s_

    l_dS2 = 6. * k_l * k_l * l_
    m_dS2 = 6. * k_m * k_m * m_
    s_dS2 = 6. * k_s * k_s * s_

    f  = wl * l     + wm * m     + ws * s
    f1 = wl * l_dS  + wm * m_dS  + ws * s_dS
    f2 = wl * l_dS2 + wm * m_dS2 + ws * s_dS2

    S = S - f * f1 / (f1*f1 - 0.5 * f * f2)

    return S

# Although this function is primarily a translation of Ottosson's work, it is
#   also a public function and therefore follows the convention set by the
#   other public functions found later in this script -- that convention being
#   to allow the user choice about how they provide the minimum necessary
#   information for the function. More can be found with the other public
#   functions below. 
# The minimum information needed for this function is simply a hue, which can
#   either be specified directly or inferred from a color object. 
# finds L_cusp and C_cusp for a given hue
def find_cusp(hue=None, color=None):

    # Either color or hue may be provided, but exactly one is required. 
    assert (hue == None) ^ (color == None), \
            "Exactly one of color or hue must be provided!"

    if hue != None:
        assert isinstance(hue, (float, int)), \
                f"Expected number, received {type(hue)}!"

    else:
        assert isinstance(color, colors.Color), \
                f"Expected color, received {type(color)}!"
        if not isinstance(color, colors.OKLCH):
            color = color.to_OKLCH()
        hue = color.h

    # a and b must be normalized so a^2 + b^2 == 1
    a, b = colors.OKLCH._get_normalized_ab(hue)
  
    # First, find the maximum saturation (saturation S = C/L)
    S_cusp = _max_saturation(a, b)

    # Convert to linear sRGB to find the first point where at least one of r,g,
    #   or b >= 1:
    rgb_at_max = colors.OKLAB(1, S_cusp * a, S_cusp * b).to_RGB()
    rgb_at_max.r = colors.RGB._srgb_transfer_function_inv(rgb_at_max.r/255)
    rgb_at_max.g = colors.RGB._srgb_transfer_function_inv(rgb_at_max.g/255)
    rgb_at_max.b = colors.RGB._srgb_transfer_function_inv(rgb_at_max.b/255)
    L_cusp = math.pow(1. / max(rgb_at_max.r, rgb_at_max.g, rgb_at_max.b), 1/3)
    C_cusp = L_cusp * S_cusp

    return colors.OKLCH(L_cusp, C_cusp, hue)

# I've similarly made this function more flexible for my own ease of use, even
#   if it is not intended to be user-facing. 
# The minimum information required is L1, C1, and some way of specifying hue.
#   L0 is usually not required, since it can be inferred from the method;
#   however, an option is given to provide an explicit L0 with method 'manual'. 
# Finds intersection of the line defined by 
#   L = L0 * (1 - t) + t * L1;
#   C = t * C1;
def _find_gamut_intersection(L1, C1,
                             color = None,
                             hue = None,
                             L0 = None,
                             method='hue_dependent'):

    # Either color or hue may be provided, but exactly one is required. 
    assert (color == None) ^ (hue == None), \
            "Exactly one of color or hue must be provided!"

    if hue != None:
        assert isinstance(hue, (float, int)), \
                f"Expected number, received {type(hue)}!"

    else:
        assert isinstance(color, colors.Color), \
                f"Expected color, received {type(color)}!"
        if not isinstance(color, colors.OKLCH):
            color = color.to_OKLCH()
        hue = color.h

    # a and b must be normalized so a^2 + b^2 == 1
    a, b = colors.OKLCH._get_normalized_ab(hue)

    # Find the cusp of the gamut triangle
    if abs(hue - 264) >= 1:
        cusp = find_cusp(hue=hue)
    else:
        # This handles a strange case with blues where it can converge
        #   out-of-gamut, resulting in an infinite loop.
        cusp = colors.HEX('#023BFB').to_OKLCH()

    # Manual method allows for an explicit L0 value. 
    if method == 'manual':
        assert L0 != None, \
                "L0 must be explicitly provided with method 'manual'!"
    else:
        assert L0 == None, \
                "L0 cannot be set explicitly unless using method 'manual'!"

        # The other methods specify how L0 should be set. 
        # Method 'hue_dependent' moves the color towards the point
        #   (cusp.l, 0, hue) until it intersects the gamut, which is default. 
        if method == 'hue_dependent':
            L0 = cusp.l

        # Method 'hue_independent' moves the color towards medium grey.
        elif method == 'hue_independent':
            L0 = 0.5

        # Method 'preserve_lightness' does not alter lightness as long as it's
        #   a valid value. 
        elif method == 'preserve_lightness':
            L0 = min(1, max(0, L1))

        else:
            raise ValueError(f"Unknown method: '{method}'!")

    # Find the intersection for upper and lower half separately
    if (((L1 - L0) * cusp.c - (cusp.l - L0) * C1) <= 0.):
        # Lower half

        t = cusp.c * L0 / (C1 * cusp.l + cusp.c * (L0 - L1))
        output = colors.OKLCH(L0 * (1 - t) + t * L1, t * C1, hue)
    else:
        # Upper half

        # First intersect with triangle
        t = cusp.c * (L0 - 1.) / (C1 * (cusp.l - 1.) + \
            cusp.c * (L0 - L1))

        # Then one step Halley's method
        dL = L1 - L0
        dC = C1

        k_l = +0.3963377774 * a + 0.2158037573 * b
        k_m = -0.1055613458 * a - 0.0638541728 * b
        k_s = -0.0894841775 * a - 1.2914855480 * b

        l_dt = dL + dC * k_l
        m_dt = dL + dC * k_m
        s_dt = dL + dC * k_s


        # If higher accuracy is required, 2 or 3 iterations of the following
        #   block can be used:
        output = colors.OKLCH(L0 * (1 - t) + t * L1, t * C1, hue)
        while not output.is_in_gamut():
            L = L0 * (1. - t) + t * L1
            C = t * C1

            l_ = L + C * k_l
            m_ = L + C * k_m
            s_ = L + C * k_s

            l = l_ * l_ * l_
            m = m_ * m_ * m_
            s = s_ * s_ * s_

            ldt = 3 * l_dt * l_ * l_
            mdt = 3 * m_dt * m_ * m_
            sdt = 3 * s_dt * s_ * s_

            ldt2 = 6 * l_dt * l_dt * l_
            mdt2 = 6 * m_dt * m_dt * m_
            sdt2 = 6 * s_dt * s_dt * s_

            r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s - 1
            r1 = 4.0767416621 * ldt - 3.3077115913 * mdt + 0.2309699292 * sdt
            r2 = 4.0767416621 * ldt2 - 3.3077115913 * mdt2 + \
                    0.2309699292 * sdt2

            u_r = r1 / (r1 * r1 - 0.5 * r * r2)
            t_r = -r * u_r

            g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s - 1
            g1 = -1.2684380046 * ldt + 2.6097574011 * mdt - 0.3413193965 * sdt
            g2 = -1.2684380046 * ldt2 + 2.6097574011 * mdt2 - \
                    0.3413193965 * sdt2

            u_g = g1 / (g1 * g1 - 0.5 * g * g2)
            t_g = -g * u_g

            b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s - 1
            b1 = -0.0041960863 * ldt - 0.7034186147 * mdt + 1.7076147010 * sdt
            b2 = -0.0041960863 * ldt2 - 0.7034186147 * mdt2 + \
                    1.7076147010 * sdt2

            u_b = b1 / (b1 * b1 - 0.5 * b * b2)
            t_b = -b * u_b

            t_r = t_r if u_r >= 0. else sys.float_info.max
            t_g = t_g if u_g >= 0. else sys.float_info.max
            t_b = t_b if u_b >= 0. else sys.float_info.max

            t += min(t_r, t_g, t_b)
            output = colors.OKLCH(L0 * (1 - t) + t * L1, t * C1, hue)

    return output
###############################################################################
#
# The following two functions find the intersections of the line defined by:
#   L = color.l * (1 - t1) + t1 * L1
#   C = color.c * (1 - t1) + t1 * C1
# where either L1 == color.l or C1 == color.c. These are useful points for
#   performing lightening or saturating operations within a given hue. 
# 
# This differs from the above function in the C term, as for our purposes C0
#   may not be equal to 0. This adds an additional unknown, but when
#   considering the additional constraints:
#       (L, C) = (0, 0) * (1 - t2) + t2 * (L_cusp, C_cusp); (lower half)
#           OR
#       (L, C) = (L_cusp, C_cusp) * (1 - t2) + t2 * (1, 0); (upper half)
#   we end up with five unknowns and five functions nonetheless. 
# 
###############################################################################
#
# For the first of our two functions, we take some color with chroma color.c
#   which is less than the maximum possible in-gamut chroma for the given
#   lightness color.l and hue color.h. This can be used with the trivially
#   found minimum chroma of 0 to perform relative operations on a color's
#   chroma. 
# Therefore, this function solves for chroma C given L1 == color.l:
# => L = color.l
# then in the lower half case:
#   (color.l, C) = t2 * (L_cusp, C_cusp)
#   => t2 = (color.l, C) / (L_cusp, C_cusp) where (L_cusp, C_cusp) != 0
#   => C / C_cusp = color.l / L_cusp
#   => C = C_cusp * (color.l / L_cusp)
# and in the upper half case:
#   (color.l, C) = (L_cusp, C_cusp) * (1 - t2) + t2 * (1, 0)
#   => (color.l, C) - (L_cusp, C_cusp) = t2 * ((1, 0) - (L_cusp, C_cusp))
#   => t2 = ((color.l, C) - (L_cusp, C_cusp)) / (1 - L_cusp, -C_cusp)
#       where L_cusp != 1 && C_cusp != 0
#   => (C - C_cusp) / C_cusp = (L_cusp - color.l) / (1 - L_cusp)
#   => C = C_cusp * (L_cusp - color.l) / (1 - L_cusp) + C_cusp
#           = C_cusp * (1 + (L_cusp - color.l) / (1 - L_cusp))
#           = C_cusp * (1 - color.l) / (1 - L_cusp)
#
###############################################################################
def _find_chroma_max(color):
    # First, get the cusp
    cusp = find_cusp(color=color)

    # Next, we consider whether our lightness places us in the upper or lower
    #   half:
    if color.l <= cusp.l:
        # Lower half
        C = cusp.c * (color.l / cusp.l)
    else:
        # Upper half
        C = cusp.c * (1 - color.l) / (1 - cusp.l)

        # Correct for the concavity of the upper half. 
        C = _find_gamut_intersection(color.l, C,
                                     color=color,
                                     method='preserve_lightness').c

    return C

###############################################################################
#
# For the second of our two functions, we take some color with lightness
#   color.l which is between the minimum and maximum possible in-gamut
#   lightness for the given chroma color.c and hue color.h. These can be used
#   to perform relative operations on a color's lightness. 
# Therefore, this function solves for lightness L given C1 == color.c:
# => C = color.c
# then in the lower half case:
#   (L, color.c) = t2 * (L_cusp, C_cusp)
#   => t2 = (L, color.c) / (L_cusp, C_cusp) where (L_cusp, C_cusp) != 0
#   => L / L_cusp = color.c / C_cusp
#   => L = L_cusp * (color.c / C_cusp)
# and in the upper half case:
#   (L, color.c) = (L_cusp, C_cusp) * (1 - t2) + t2 * (1, 0)
#   => (L, color.c) - (L_cusp, C_cusp) = t2 * ((1, 0) - (L_cusp, C_cusp))
#   => t2 = ((L, color.c) - (L_cusp, C_cusp)) / (1 - L_cusp, -C_cusp)
#           where L_cusp != 1 && C_cusp != 0
#   => (L - L_cusp) / (1 - L_cusp) = (C_cusp - color.c) / C_cusp
#                                   = 1 - color.c / C_cusp
#   => L = (1 - L_cusp) * (1 - color.c / C_cusp) + L_cusp
#   => L = 1 - (1 - L_cusp) * (color.c / C_cusp)
#
# Since the lightness intersects at two points, we are interested in both the
#   lower half and the upper half. 
#
###############################################################################
def _find_lightness_bounds(color):
    # First, get the cusp
    cusp = find_cusp(color=color)

    # Lower half
    L1 = cusp.l * (color.c / cusp.c)

    # Upper half
    L2 = 1 - (1 - cusp.l) * (color.c / cusp.c)

    # Correct for the concavity of the upper half. 
    # By manually setting L0 to an arbitrarily large negative number, we can
    #   easily approximate moving horizontally. 
    L2 = _find_gamut_intersection(L2, color.c,
                                  color=color,
                                  method='manual',
                                  L0=-1000).l

    return (L1, L2)

# A simple lerp
def _lerp(t, a, b):
    return a * (1 - t) + b * t

###############################################################################
#
# Public Functions
#
###############################################################################
#
# All of the below functions implement a similar function header and type
#   checking process so that users are able to specify the necessary
#   information in whatever format is convenient to them, without compromising
#   the stability of the code.  
# Generally speaking, a function which requires lightness, hue, or chroma can
#   receive either explicit values for each, or a color object with the
#   desired properties. A color object need not be OKLCH, and thus is the
#   intended way to pass RGB/HEX colors. Many of the functions essentially
#   exist to tweak one of the characteristics of an OKLCH color by
#   interpolating within certain bounds, and when that is the case the first
#   argument is always the parameter for that lerp. Furthermore, a method can
#   often be specified between relative, which operates from the provided
#   color to the extremum in-gamut color for the given axis, and absolute,
#   which only considers the extrema. 
#
###############################################################################

# Type-checking used for all of the below:
def __get_OKLCH_if_color(arg):
    colors.Color._is_color(arg)
    return arg.to_OKLCH()

# Lerps the chroma for the given color. Negative t dechromatizes if the method
#   is relative
def chromatize(t, 
               color = None,
               hue = None,
               lightness = None,
               method = 'relative'):

    assert (color == None) ^ (hue == None), \
            "Exactly one of color or hue must be provided!"

    if hue != None:
        if not isinstance(hue, (float, int)):
            raise ValueError(f"Expected number, received {type(lightness)}!")

        assert lightness != None, \
                "Lightness must be specified with explicit hue!"
        if not isinstance(lightness, (float, int)):
            raise ValueError(f"Expected number, received {type(lightness)}!")

        assert method == 'absolute', \
                "Explicit hue can only be specified with method 'relative'!"
        # Generate a color object with the given parameters
        color = colors.OKLCH(lightness, 0., hue)

    else:
        color = __get_OKLCH_if_color(color)

    # Find max chroma
    max = _find_chroma_max(color)

    if method == 'relative':
        if t < -1 or t > 1:
            raise ValueError(
                    "t should be in the range [-1,1] for method 'relative'!")

        # Interpolate between current c and maximum
        if t >= 0:
            C = _lerp(t, color.c, max)

        # Negative t means we interpolate towards the minimum (0) instead
        else:
            C = _lerp(-t, color.c, 0)

    elif method == 'absolute':
        if t < 0 or t > 1:
            raise ValueError(
                    "t should be in the range [0,1] for method 'absolute'!")

        # In absolute mode we interpolate between minimum (0) and max
        C = _lerp(t, 0, max)

    else:
        raise ValueError(f"""Unknown method: '{method}'!
Valid methods are 'relative' and 'absolute'.""")

    ret = colors.OKLCH(color.l, C, color.h)
    # Make sure that the color is in-gamut
    if ret.is_in_gamut():
        return ret
    else:
        # Clip it into gamut
        return gamut_clip_preserve_lightness(ret)

# Simply reverses the direction of chromatize
def dechromatize(t, 
                 color = None,
                 hue = None,
                 lightness = None,
                 method = 'relative'):

    # Negate t and chromatize
    if method == 'relative':
        return chromatize(-t,
                          color=color,
                          hue=hue,
                          lightness=lightness)

    # Reverse t and chromatize
    elif method == 'absolute':
        return chromatize(1 - t,
                          color=color,
                          hue=hue,
                          lightness=lightness,
                          method='absolute')

    else:
        raise ValueError(f"""Unknown method: '{method}'!
Valid methods are 'relative' and 'absolute'.""")

# Chromatize, while technically more correct, is not a very appealing name, so
#   detone and tone are provided as aliases.
def detone(t,
             color = None,
             hue = None,
             lightness = None,
             method = 'relative'):

    return chromatize(t,
                      color=color,
                      hue=hue,
                      lightness=lightness,
                      method=method)

def tone(t,
        color = None,
        hue = None,
        lightness = None,
        method = 'relative'):

    return dechromatize(t,
                        color=color,
                        hue=hue,
                        lightness=lightness,
                        method=method)

# Lerps the lightness for the given color. Negative t darkens if the method is
#   relative
def lighten(t, 
            color = None,
            hue = None,
            chroma = None,
            method = 'relative'):

    assert (color == None) ^ (hue == None), \
            "Exactly one of color or hue must be provided!"

    if hue != None:
        if not isinstance(hue, (float, int)):
            raise ValueError(f"Expected number, received {type(chroma)}!")

        assert chroma != None, \
                "Lightness must be specified with explicit hue!"
        if not isinstance(chroma, (float, int)):
            raise ValueError(f"Expected number, received {type(chroma)}!")

        assert method == 'absolute', \
                "Explicit hue can only be specified with method 'relative'!"
        # Generate a color object with the given parameters
        color = colors.OKLCH(0.5, chroma, hue)

    else:
        color = __get_OKLCH_if_color(color)

    # Find the min and max lightness
    bounds = _find_lightness_bounds(color)

    if method == 'relative':
        if t < -1 or t > 1:
            raise ValueError(
                    "t should be in the range [-1,1] for method 'relative'!")

        # Interpolate between current l and maximum
        if t >= 0:
            L = _lerp(t, color.l, bounds[1])

        # Negative t means we interpolate towards the minimum instead
        else:
            L = _lerp(-t, color.l, bounds[0])

    elif method == 'absolute':
        if t < 0 or t > 1:
            raise ValueError(
                    "t should be in the range [0,1] for method 'absolute'!")

        # In absolute mode we interpolate between minimum and max
        L = _lerp(t, bounds[0], bounds[1])

    else:
        raise ValueError(f"""Unknown method: '{method}'!
Valid methods are 'relative' and 'absolute'.""")

    ret = colors.OKLCH(L, color.c, color.h)
    # Make sure that the color is in-gamut
    if ret.is_in_gamut():
        return ret
    else:
        # Clip it into gamut
        return _find_gamut_intersection(L, color.c, hue=color.h)

# Simply reverses the direction of chromatize
def darken(t, 
           color = None,
           hue = None,
           chroma = None,
           method = 'relative'):

    # Negate t and lighten
    if method == 'relative':
        return lighten(-t,
                       color=color,
                       hue=hue,
                       chroma=chroma)

    # Reverse t and lighten
    elif method == 'absolute':
        return lighten(1 - t,
                       color=color,
                       hue=hue,
                       chroma=chroma,
                       method='absolute')

    else:
        raise ValueError(f"""Unknown method: '{method}'!
Valid methods are 'relative' and 'absolute'.""")

# Linearly interpolate between two colors
# Hue path is determined by method parameter
def interpolate(t, color1, color2,
                method = 'shortest'):
    color1 = __get_OKLCH_if_color(color1)
    color2 = __get_OKLCH_if_color(color2)

    # Get the lerped parameters
    l = _lerp(t, color1.l, color2.l)
    c = _lerp(t, color1.c, color2.c)

    # Hue path is determined by method
    if method == 'shortest':
        # Ensures hue takes the shortest path
        if color2.h - color1.h > 180:
            h = _lerp(t, color1.h + 360, color2.h)
        elif color2.h - color1.h < -180:
            h = _lerp(t, color1.h, color2.h + 360)
        else:
            h = _lerp(t, color1.h, color2.h)
    elif method == 'longest':
        # Ensures hue takes the longest path
        if 0 < color2.h - color1.h < 180:
            h = _lerp(t, color1.h + 360, color2.h)
        elif -180 < color2.h - color1.h <= 0:
            h = _lerp(t, color1.h, color2.h + 360)
        else:
            h = _lerp(t, color1.h, color2.h)
    elif method == 'increasing':
        # Ensures hue is strictly increasing
        if color2.h < color1.h:
            h = _lerp(t, color1.h, color2.h + 360)
        else:
            h = _lerp(t, color1.h, color2.h)
    elif method == 'decreasing':
        # Ensures hue is strictly decreasing
        if color1.h < color2.h:
            h = _lerp(t, color1.h + 360, color2.h)
        else:
            h = _lerp(t, color1.h, color2.h)
    elif method == 'use_OKLAB':
        color1 = color1.to_OKLAB()
        color2 = color2.to_OKLAB()

        a = _lerp(t, color1.a, color2.a)
        b = _lerp(t, color1.b, color2.b)
        result = colors.OKLAB(l, a, b).to_OKLCH()

        c = result.c
        h = result.h
    else:
        raise ValueError(f"""Unknown method '{method}'! Valid methods are:
'shortest', 'longest', 'increasing', 'decreasing', and 'use_OKLAB'.""")

    ret = colors.OKLCH(l, c, h)
    # Make sure that the color is in-gamut
    if ret.is_in_gamut():
        return ret
    else:
        # Clip it into gamut
        return gamut_clip_preserve_lightness(ret)

# Gamut clipping:
def gamut_clip_hue_dependent(color):
    _color = __get_OKLCH_if_color(color)
    if color.is_in_gamut(): return color

    return _find_gamut_intersection(_color.l, _color.c, color=_color)

def gamut_clip_hue_independent(color):
    _color = __get_OKLCH_if_color(color)
    if color.is_in_gamut(): return color

    return _find_gamut_intersection(_color.l, _color.c,
                                    color=_color,
                                    method='hue_dependent')

def gamut_clip_preserve_lightness(color):
    _color = __get_OKLCH_if_color(color)
    if color.is_in_gamut(): return color

    return _find_gamut_intersection(_color.l, _color.c,
                                    color=_color,
                                    method='preserve_lightness')
