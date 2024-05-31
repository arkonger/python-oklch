# Changelog

## v0.2.1
- Fixed a bug in color type checking

## v0.2.0
- Overloaded `Color.__or__(self, other)` to get euclidean distance with pipe operator
- Added `Color.get_nearest_web_color(color)` to get nearest web color
- Renamed `Hex` subclass to `HEX` for consistency with other subclasses
- Added `OKLAB` subclass
- Overloaded `Color.__add__(self, other)` to get midpoint in OKLAB
- Overloaded `Color.__neg__(self)` to get complement in OKLAB
- Overloaded `Color.__sub__(self, other)` to add `self` with `other`'s complement
- Added gamut clipping functions:
    - `gamut_clip_hue_dependent(color)`
    - `gamut_clip_hue_independent(color)`
    - `gamut_clip_preserve_lightness(color)`

## v0.1.0
Initial Release. 
- Includes `Color` superclass and `RGB`, `Hex`, and `OKLCH` subclasses, as well as conversions between them. 
- Includes `Color.ColorDict` dictionary of extended web colors, as well as function `Color.get_web_color(color_name)` and `Color.get_random_web_color()` to make working with them slightly more pleasant. 
- Includes various tools such as `find_cusp(...)`, `lighten(...)` and `darken(...)`, `chromatize(...)` and `dechromatize(...)` / `brighten(...)` and `dim(...)`, as well as `interpolate(t, color1, color2, method='shortest')`. 
