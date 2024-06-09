# The `oklch.tools` Submodule
The `tools` submodule defines a whole suite of useful functions which operate on the OKLAB and OKLCH color spaces to perform tasks such as maximizing saturation, lightening and darkening, toning and detoning, etc. All of the below functions return an `OKLCH` color object unless otherwise specified.

These functions are designed with the key design goal of allowing for as much flexibility as possible without compromising the stability of the code. As such, it is frequently possible to provide a piece of information in multiple ways; for example, you may provide a function with the argument `hue=354.66`, or you may equivalently provide it with the argument `color=colors.OKLCH(.4981, 0.2, 354.66)`, and the function will do the work of determining if the information you provided it is both sufficient and unambiguous.  

In this example, the function would know that it requires a hue component, and would scrape it from the `OKLCH` object if you provided it none. **Caution should be taken, however, to avoid providing ambiguous information** ― if you were to provide both a hue and a color, it would be unclear to the function which to use and an exception would be thrown. 

## `find_cusp(hue=None, color=None)`
Finds and returns an `OKLCH` object corresponding to the cusp of the triangle for a given hue; that is, the most saturated color for a given hue. 

## `lighten(t, color=None, hue=None, chroma=None, method='relative')`
Linearly interpolates between the provided color and the maximum in-gamut lightness for the color's hue and chroma. 

- The `t` parameter, which can be in the range `[-1,1]` for the relative method or `[0,1]` for the absolute method, determines what percent of the way to lighten towards the maximum. A negative value instead darkens towards the minimum. 
- The `color` parameter gives the hue and chroma needed to find the lightness extrema. When using the relative method, it also provides the starting lightness for interpolation. 
- The `hue` and `chroma` parameters can also be passed explicitly instead, but only while using the absolute method, since there would be no means to specify the starting lightness. 
- The `method` parameter specifies whether to lighten from the provided color to the maximum ("relative" method) or to lighten from the minimum to the maximum ("absolute" method)

## `darken(t, color=None, hue=None, chroma=None, method='relative')`
The `darken` function essentially operates identically to the `lighten(...)` function (see above), but with the direction reversed. 

## `chromatize(t, color=None, hue=None, lightness=None, method='relative')`
Linearly interpolates between the provided color and the maximum in-gamut chroma for that color's hue and lightness.  
While "chromatize" was the most accurate term I could come up with, it's also not very appealing; for this reason, `detone(...)` is provided as an alias if you prefer.

- The `t` parameter, which can be in the range `[-1,1]` for the relative method or `[0,1]` for the absolute method, determines what percent of the way to chromatize towards the maximum. A negative value instead dechromatizes towards the minimum. 
- The `color` parameter gives the hue and lightness needed to find the chroma extrema. When using the relative method, it also provides the starting chroma for interpolation. 
- The `hue` and `lightness` parameters can also be passed explicitly instead, but only while using the absolute method, since there would be no means to specify the starting chroma. 
- The `method` parameter specifies whether to chromatize from the provided color to the maximum ("relative" method) or to chromatize from the minimum to the maximum ("absolute" method)

## `dechromatize(t, color=None, hue=None, lightness=None, method='relative')`
The `dechromatize` function essentially operates identically to the `chromatize(...)` function (see above), but with the direction reversed.  
While "dechromatize" was the most accurate term I could come up with, it's also not very appealing; for this reason, `tone(...)` is provided as an alias if you prefer.

## `interpolate(t, color1, color2, method='shortest')`
Linearly interpolates between two colors component-wise. 

- The `t` parameter, which can be in the range `[0,1]`, determines what percent of the way to interpolate from the first color to the second color.
- The `color1` and `color2` parameters provide the two colors for interpolation. 
- The `method` parameter determines how to interpolate the hues. There are five possible methods:
    - `'shortest'`: Take the shortest path; for example, if the endpoints were `color1.h=5` and `color2.h=355`, then `360` would be added to `color1.h` to instead get `color1.h=365`. 
    - `'longest'`: Take the longest path; for example, if the endpoints were `color1.h=5` and `color2.h=15`, then `360` would be added to `color1.h` to instead get `color1.h=365`. 
    - `'increasing'`: Ensure the hue only ever increases; for example, if the endpoints were `color1.h=45` and `color2.h=30`, then `360` would be added to `color1.h` to instead get `color1.h=405`. 
    - `'decreasing'`: Ensure the hue only ever decreases; for example, if the endpoints were `color1.h=30` and `color2.h=45`, then `360` would be added to `color1.h` to instead get `color1.h=390`. 
    - `'use_OKLAB'`: Unlike the other four methods, this method operates in the rectangular OKLAB color space, rather than the cylindrical OKLCH color space. In practice, this will result in a more traditional gradient where, for example, complementary colors will pass through grey as opposed to processing around the lightness axis through each interstitial hue. 

## Gamut Clipping Functions
The below three functions "clip" an out-of-gamut color back into gamut. This process involves finding the intersection between the edge of the gamut and the line passing through the points `(color.l, color.c)` and `(L0, 0)`. Each function makes a different choice about the value of `L0`. 

If the provided color is already in-gamut, it is returned unmodified. 

### `gamut_clip_hue_dependent(color)`
This function sets `L0=L_cusp` where `L_cusp` is the lightness of the cusp. This means that the color is clipped towards the center of the hue triangle for its specific hue. 

### `gamut_clip_hue_independent(color)`
This function sets `L0=0.5`. This means that the color is clipped towards medium grey regardless of the shape of its particular hue triangle. 

### `gamut_clip_preserve_lightness(color)`
This function sets `L0=color.l` as long as `color.l` is in the range `[0,1]`. If `color.l` is out-of-bounds, it is clamped to the nearest bound. 
