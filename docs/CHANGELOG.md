# Changelog

## v0.1.0
Initial Release. 
- Includes `Color` superclass and `RGB`, `Hex`, and `OKLCH` subclasses, as well as conversions between them. 
- Includes `Color.ColorDict` dictionary of extended web colors, as well as function `Color.get_web_color(color_name)` and `Color.get_random_web_color()` to make working with them slightly more pleasant. 
- Includes various tools such as `find_cusp(...)`, `lighten(...)` and `darken(...)`, `chromatize(...)` and `dechromatize(...)` / `brighten(...)` and `dim(...)`, as well as `interpolate(t, color1, color2, method='shortest')`. 
