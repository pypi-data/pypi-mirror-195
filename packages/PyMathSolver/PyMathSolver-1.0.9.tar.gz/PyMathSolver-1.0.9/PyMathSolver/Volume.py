# PyMathSolver - Volume

# Imports
from termcolor import colored
import math

# Function - About
def about():
    print(colored('\nVolume is a measure of three-dimensional space. Also, the amount of space that an object occupies.', 'green'))

    print(colored('\nPyMathSolver.Volume has the following functions:', 'green'))
    print(colored('\n1) cube() - Takes the length of the side as a parameter and returns the volume.', 'green'))
    print(colored('2) cuboid() - Takes the length, width, and height as parameters and returns the volume.', 'green'))
    print(colored('3) cone() - Takes the radius and height as parameters and returns the volume.', 'green'))
    print(colored('4) cylinder() - Takes the radius and height as parameters and returns the volume.', 'green'))
    print(colored('5) sphere() - Takes the radius as a parameter and returns the volume.', 'green'))
    print(colored('6) hemisphere() - Takes the radius as a parameter and returns the volume.', 'green'))
    print(colored('7) pyramid() - Takes the length, width, and height as parameters and returns the volume.', 'green'))

# Function - Cube
def cube(side):
    volume = math.pow(side, 3)
    
    return volume

# Function - Cuboid
def cuboid(length, width, height):
    volume = length * width * height

    return volume

# Function - Cone
def cone(radius, height):
    volume = (1/3) * 3.14 * math.pow(radius, 2) * height

    return volume

# Function - Cylinder
def cylinder(radius, height):
    volume = 3.14 * math.pow(radius, 2) * height

    return volume

# Function - Sphere
def sphere(radius):
    volume = (4/3) * 3.14 * math.pow(radius, 3)

    return volume

# Function - Hemisphere
def hemisphere(radius):
    volume = (2/3) * 3.14 * math.pow(radius, 3)

    return volume

# Function - Prism
def pyramid(length, width, height):
    volume = (length * width * height) / 3

    return volume