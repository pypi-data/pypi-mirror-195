# PyMathSolver - Surface Area

# Imports
from simple_colors import *
import Numbers

# Function - About
def about():
    print(magenta("\nSurface Area of a solid object is a measure of the total area that the surface of the object occupies."))

    print(magenta("\nPyMathSolver.SurfaceArea has the following functions:"))
    print(magenta("\n1) ") + magenta("cube()", ["bold", "underlined"]) + magenta(" - Takes the length of the side as a parameter and returns the surface area."))
    print(magenta("2) ") + magenta("cuboid()", ["bold", "underlined"]) + magenta(" - Takes the length, width, and height as parameters and returns the surface area."))
    print(magenta("3) ") + magenta("cone()", ["bold", "underlined"]) + magenta(" - Takes the radius and height as parameters and returns the surface area."))
    print(magenta("4) ") + magenta("cylinder()", ["bold", "underlined"]) + magenta(" - Takes the radius and height as parameters and returns the surface area."))
    print(magenta("5) ") + magenta("sphere()", ["bold", "underlined"]) + magenta(" - Takes the radius as a parameter and returns the surface area."))
    print(magenta("6) ") + magenta("hemisphere()", ["bold", "underlined"]) + magenta(" - Takes the radius as a parameter and returns the surface area."))

    print(red("\nNOTE:", "bold") + red(" In all the functions above, you can pass a parameter 'lateral=True' that will give you the lateral surface area."))

    print()

# Function - Cube
def cube(side, lateral=False):
    if (lateral == False):
        area = 6 * Numbers.power(side, 2)
    else:
        area = 4 * Numbers.power(side, 2)

    return area

# Function - Cuboid
def cuboid(length, width, height, lateral=False):
    if (lateral == False):
        area = 2 * ((length * width) + (width * height) + (length * height))
    else:
        area = 2 * height * (length + width)

    return area

# Function - Cone
def cone(radius, height, lateral=False):
    slantHeight = Numbers.squareRoot(Numbers.power(radius, 2) + Numbers.power(height, 2))

    if (lateral == False):
        area = 3.14 * radius * (slantHeight + radius)
    else:
        area = 3.14 * radius * slantHeight

    return area

# Function - Cylinder
def cylinder(radius, height, lateral=False):
    if (lateral == False):
        area = 2 * 3.14 * radius * (radius + height)
    else:
        area = 2 * 3.14 * radius * height

    return area

# Function - Sphere
def sphere(radius):
    area = 4 * 3.14 * Numbers.power(radius, 2)

    return area

# Function - Hemisphere
def hemisphere(radius, lateral=False):
    if (lateral == False):
        area = 3 * 3.14 * Numbers.power(radius, 2)
    else:
        area = 2 * 3.14 * Numbers.power(radius, 2)

    return area