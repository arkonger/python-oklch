# python-oklch
A module for python implementing the OKLCH color space as described by [Björn Ottosson](https://bottosson.github.io/posts/), along with various tools for manipulating color objects. 

## Current Features: 
- Create and use color objects in RGB, Hex, or OKLCH with the ability to easily convert between them. 
- Find information about the shape of the OKLCH color space for a given hue such as the hue's cusp (point of maximum saturation), the maximum chroma for a given pair of hue and lightness, or the lightness extrema for a given pair of hue and chroma. 
- Use that shape information to perform relative operations on a color, such as lerping between its current and maximum possible chroma. 
- Interpolate between colors to produce generally perceptually-smooth gradients. 

## Todo:
- [x] ~~Create documentation~~
- [ ] Read up on python module structure (is this layout in-line with best practices?)
- [ ] Flesh out color objects with operators and such
- [ ] Add additional tools, such as hue rotation, palette generation, nearest web color, etc
- [ ] Do more testing on the interpolate() function to see if there are improvements to be made
- [ ] Standardize errors more (change `AssertionError`s to `ValueError`s?)
- [ ] Is file IO beyond the scope of this project? Does an existing module sufficiently address the problem already? 
