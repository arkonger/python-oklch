# The `oklch.colors` Submodule
The `colors` submodule defines the basic framework for color objects, as well as the conversions between them. 

## The `Color` Superclass
This submodule defines a `Color` superclass, but it should normally only be used for type-checking (e.g., `isinstance(color, Color)`). 

That being said, the `Color` superclass does contain a few useful members:
- `ColorDict: {string → string}` is a dictionary of all 140 extended web colors, with its keys being the colors' names and its values being the colors' hex codes. 
- `get_web_color(color_name): string → HEX` is a function which takes a color's name and returns a `HEX` color object with the corresponding hex code. 
- `get_random_web_color(): → (string, HEX)` returns a random web color as a tuple with the color's name and a `HEX` object of the color.
- `get_nearest_web_color(color, n=1): Color → (string, OKLCH)` returns a tuple containing info about the nearest web color to the provided color ― the first element is the color's name as a string and the second element is an `OKLCH` object of that color.  
    If `n` is greater than one, a list of such tuples, sorted by distance, is returned instead.

In addition, the following member functions are defined and subsequently overloaded by each subclass: 
- `__str__(self):` Overloads the `str()` function to return a string formatted according to the color type: 
    - `RGB.__str__(self): f"rgb({self.r}, {self.g}, {self.b})"`
    - `HEX.__str__(self): f"{self.hex_code}"`
    - `OKLAB.__str(self): f"oklab({self.l}, {self.a}, {self.b})"`
    - `RGB.__str__(self): f"oklch({self.l}, {self.c}, {self.h})"`
- `__or__(self, other):` Overloads the pipe operator to return the euclidean distance between two colors in the OKLAB color space. 
- `__add__(self, other):` Overloads addition to return the midpoint of the two colors in OKLAB color space. The return type is always the type of `self` *unless* `type(self)` is `HEX` and the result would produce an out-of-gamut color (and therefore a mangled hex code); in this case, an `RGB` color is returned instead to avoid possible ambiguity. 
- `__neg__(self):` Overloads negation to get the complement in OKLAB color space (that is, the color `OKLAB(1-L, -a, -b)`). The return type is always the type of `self` *unless* `type(self)` is `HEX` and the result would produce an out-of-gamut color (and therefore a mangled hex code); in this case, an `RGB` color is returned instead to avoid possible ambiguity. 
- `__sub__(self, other):` Overloads subtraction to return the midpoint in OKLAB color space of `self` and the complement of `other`. The return type is always the type of `self` *unless* `type(self)` is `HEX` and the result would produce an out-of-gamut color (and therefore a mangled hex code); in this case, an `RGB` color is returned instead to avoid possible ambiguity. 
- `is_close(other):` Returns true if self and other would be represented with the same hex code
- `to_RGB(self):` Converts the color to `RGB`
- `to_HEX(self):` Converts the color to `HEX`
- `to_OKLAB(self):` Converts the color to `OKLAB`
- `to_OKLCH(self):` Converts the color to `OKLCH`
- `is_in_gamut(self):` Return `True` if the color is in-gamut and `False` otherwise. 

## The `RGB` Subclass
`RGB` objects are defined with a triplet of values `RGB(r, g, b)` where `0 ≤ r, g, b ≤ 255`. 

## The `HEX` Subclass
`HEX` objects are defined with a hex code string `HEX(hex_code)` of the format `/#?[0-9a-fA-F]{6}/`.

## The `OKLAB` Subclass
`OKLAB` objects are defined with a triple of values `OKLAB(l, a, b)` where `0 ≤ l ≤ 1`. Although `a` and `b` are technically unbounded, `a` practically lies in approximately the range `[-0.16, 0.26]` and `b` practically lies in approximately the range `[-0.30, 0.18]`, as a greater value than those will place it outside the gamut. 

## The `OKLCH` Subclass
`OKLCH` objects are defined with a triplet of values `OKLCH(l, c, h)` where `0 ≤ l ≤ 1, 0 ≤ c, 0 ≤ h ≤ 360`. Although `c` is technically unbounded in the +∞ direction, it is practically never more than about `0.3`, as a greater value that that will place it outside the gamut. 

`OKLCH` has the additional member function `css_string(self)` which return a string that is nicely formatted for css styles. 
