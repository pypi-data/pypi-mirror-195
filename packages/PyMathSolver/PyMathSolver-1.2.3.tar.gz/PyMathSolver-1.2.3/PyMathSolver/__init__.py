# PyMathSolver - Init

# Imports
from simple_colors import *

# Constants
pi = 3.141592653589793
euler = 2.718288182845
goldenRatio = 1.61803398875
planck = "The Planck's Constant is 6.626068 x 10⁻³⁴."
avagadro = "The Avagadro's Constant is 6.0221515 x 10⁻²³."
speedOfLight = "The speed of light is 299,792,458 m/s."
gravitationalConstant = "The Gravitational Constant is 6.67300 x 10⁻¹¹."
boltzmannConstant = "The Boltzmann's Constant is 1.380650 x 10²³."
iota = "Iota, which is also referred to as 'i'. It's value is √-1."
eulerIdentity = "The Euler's Identity is eⁱˣᴾⁱ + 1 = 0. 'e' is the Euler's Number and 'i' is √-1."

# Function - About
def about():
    print(magenta("\nWelcome to PyMathSolver!"))
    print(magenta("\nPyMathSolver is a Python module to solve math problems and work on calculations."))

    print(magenta("\nThis module has the following sub-modules:"))
    print(magenta("\n1) ") + magenta("Quadratic", ["bold", "underlined"]) + magenta(" - Find the roots of a quadratic equation."))
    print(magenta("2) ") + magenta("Numbers", ["bold", "underlined"]) + magenta(" - Find the HCF, LCM, square, square root, cube, and much more."))
    print(magenta("3) ") + magenta("Geometry", ["bold", "underlined"]) + magenta(" - Find areas, volumes, surface areas, lateral surface areas, and much more."))
    print(magenta("4) ") + magenta("CoordinateGeometry", ["bold", "underlined"]) + magenta(" - Find the distance between 2 points, use the section formula, and find the collinearity of points on a plane."))
    print(magenta("5) ") + magenta("Statistics", ["bold", "underlined"]) + magenta(" - Find the mean, median, and mode of ungrouped data."))
    print(magenta("6) ") + magenta("Trigonometry", ["bold", "underlined"]) + magenta(" - Convert degrees to radians, radians to degrees, and find trigonometric ratios."))
    print(magenta("7) ") + magenta("ComplexNumbers", ["bold", "underlined"]) + magenta(" - Algebra of complex numbers. Find the modulus, conjugate, multiplicative inverse, and polar form of a complex number."))

    print(magenta("\nMany more are on their way!"))

    print(red("\nNOTE:", ["bold", "underlined"]) + red(" To know more about each sub-module, use:"))
    print(red("\nfrom PyMathSolver import ") + red("sub-module", "italic"))
    print(red("sub-module", "italic") + red(".about()"))

    print(green("\nName", "bold") + green(" - PyMathSolver"))
    print(green("Version", "bold") + green(" - 1.2.3"))
    print(green("Description", "bold") + green(" - PyMathSolver is a Python module to solve math problems and work on calculations."))
    print(green("Author", "bold") + green(" - Aniketh Chavare"))
    print(green("Author's Email", "bold") + green(" - anikethchavare@outlook.com"))
    print(green("GitHub URL", "bold") + green(" - https://github.com/Anikethc/PyMathSolver"))
    print(green("Pypi.org URL", "bold") + green(" - https://pypi.org/project/pymathsolver"))

    print()