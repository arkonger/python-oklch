# python-oklch
A module for python implementing the OKLCH color space as described by [Björn Ottosson](https://bottosson.github.io/posts/), along with various tools for manipulating color objects. 

## Current Features: 
- Create and use color objects in RGB, Hex, or OKLCH with the ability to easily convert between them. 
- Find information about the shape of the OKLCH color space for a given hue such as the hue's cusp (point of maximum saturation), the maximum chroma for a given lightness, or the lightness extrema for a given chroma. 
- Use that shape information to perform relative operations on a color, such as lerping between its current and maximum possible chroma. 
- Interpolate between colors to produce more perceptually-smooth gradients. 

## Todo:
- [x] ~~Create documentation~~
- [ ] Read up on python module structure (is this layout in-line with best practices?)
- [ ] Flesh out color objects with operators and such
    - [ ] Comparison (which method(s)?)
    - [x] ~~Subtraction for euclidean distance~~
    - [ ] Add an actual OKLAB subclass to make it easier to work in rectangular space
- [ ] Add additional tools, such as hue rotation, palette generation, nearest web color, etc
    - [ ] hue rotation
    - [ ] palette generation
    - [x] ~~nearest web color~~
- [ ] Do more testing on the interpolate() function to see if there are improvements to be made
    - [ ] Add a `use_oklab` parameter or similar to allow true blending instead of rotating around
- [ ] Standardize errors more (change `AssertionError`s to `ValueError`s?)
- [ ] Is file IO beyond the scope of this project? Does an existing module sufficiently address the problem already? 
