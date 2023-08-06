# PyMathSolver - Volume

# Imports
from simple_colors import *
import Numbers

# Function - About
def about():
    print(magenta("\nVolume is a measure of three-dimensional space. Also, the amount of space that an object occupies."))

    print(magenta("\nPyMathSolver.Volume has the following functions:"))
    print(magenta("\n1) ") + magenta("cube()", ["bold", "underlined"]) + magenta(" - Takes the length of the side as a parameter and returns the volume."))
    print(magenta("2) ") + magenta("cuboid()", ["bold", "underlined"]) + magenta(" - Takes the length, width, and height as parameters and returns the volume."))
    print(magenta("3) ") + magenta("cone()", ["bold", "underlined"]) + magenta(" - Takes the radius and height as parameters and returns the volume."))
    print(magenta("4) ") + magenta("cylinder()", ["bold", "underlined"]) + magenta(" - Takes the radius and height as parameters and returns the volume."))
    print(magenta("5) ") + magenta("sphere()", ["bold", "underlined"]) + magenta(" - Takes the radius as a parameter and returns the volume."))
    print(magenta("6) ") + magenta("hemisphere()", ["bold", "underlined"]) + magenta(" - Takes the radius as a parameter and returns the volume."))
    print(magenta("7) ") + magenta("pyramid()", ["bold", "underlined"]) + magenta(" - Takes the length, width, and height as parameters and returns the volume."))

    print()

# Function - Cube
def cube(side):
    volume = Numbers.power(side, 3)
    
    return volume

# Function - Cuboid
def cuboid(length, width, height):
    volume = length * width * height

    return volume

# Function - Cone
def cone(radius, height):
    volume = (1/3) * 3.14 * Numbers.power(radius, 2) * height

    return volume

# Function - Cylinder
def cylinder(radius, height):
    volume = 3.14 * Numbers.power(radius, 2) * height

    return volume

# Function - Sphere
def sphere(radius):
    volume = (4/3) * 3.14 * Numbers.power(radius, 3)

    return volume

# Function - Hemisphere
def hemisphere(radius):
    volume = (2/3) * 3.14 * Numbers.power(radius, 3)

    return volume

# Function - Prism
def pyramid(length, width, height):
    volume = (length * width * height) / 3

    return volume