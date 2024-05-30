# The `oklch.colors` Submodule
The `colors` submodule defines the basic framework for color objects, as well as the conversions between them. 

## The `Color` Superclass
This submodule defines a `Color` superclass, but this should only be used for type-checking (e.g., `isinstance(color, Color)`). 

That being said, the `Color` superclass does contain a few useful members:
- `ColorDict: {string → string}` is a dictionary of all 140 extended web colors, with keys being the colors' names and values being the colors' hex codes. 
- `get_web_color(color_name): string → Hex` is a function which takes a color's name and returns a `Hex` color object with the corresponding hex code. 
- `get_random_web_color():` returns a random web color as a `Hex` object. 
- `get_nearest_web_color(color): Color → (string, OKLCH)` returns a tuple containing the name of the nearest web color to the provided color and an `OKLCH` object of that color. 

In addition, the following member functions are defined and subsequently overloaded by each subclass: 
- `__str__(self):` Overloads the `str()` function to return a string formatted according to the color type: 
    - `RGB.__str__(self): f"rgb({self.r}, {self.g}, {self.b})"`
    - `Hex.__str__(self): f"{self.hex_code}"`
    - `RGB.__str__(self): f"oklch({self.l}, {self.c}, {self.h})"`
- `__sub__(self, other):` Overloads subtraction between colors to return the euclidean distance between them in the OKLCH color space. 
- `to_RGB(self):` Converts the color to `RGB`
- `to_Hex(self):` Converts the color to `Hex`
- `to_OKLCH(self):` Converts the color to `OKLCH`
- `is_in_gamut(self):` Return `True` if the color is in-gamut and `False` otherwise. 

## The `RGB` Subclass
`RGB` objects are defined with a triplet of values `RGB(r, g, b)` where `0 ≤ r, g, b ≤ 255`. 

## The `Hex` Subclass
`Hex` objects are defined with a hex code string `Hex(hex_code)` of the format `/#?[0-9a-fA-F]{6}/`.

## The `OKLCH` Subclass
`OKLCH` objects are defined with a triplet of values `OKLCH(l, c, h)` where `0 ≤ l ≤ 1, 0 ≤ c, 0 ≤ h ≤ 360`. Although c is technically unbounded in the +∞ direction, it is practically never more than about 0.3, as a greater value that that will place it outside the gamut. 

`OKLCH` has the additional member function `css_string(self)` which return a string that is nicely formatted for css styles. 
