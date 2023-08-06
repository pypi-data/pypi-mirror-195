# PyMathSolver - Lateral Surface Area

# Imports
from termcolor import colored
import math

# Function - About
def about():
    print(colored('\nLateral Surface Area of a solid object is a measure of the total area that the surface of the object occupies, except the areas of the base and the top.', 'green'))

    print(colored('\nPyMathSolver.LateralSurfaceArea has the following functions:', 'green'))
    print(colored('\n1) cube() - Takes the length of the side as a parameter and returns the lateral surface area.', 'green'))
    print(colored('2) cuboid() - Takes the length, width, and height as parameters and returns the lateral surface area.', 'green'))
    print(colored('3) cone() - Takes the radius and height as parameters and returns the lateral surface area.', 'green'))
    print(colored('4) cylinder() - Takes the radius and height as parameters and returns the lateral surface area.', 'green'))
    print(colored('5) sphere() - Takes the radius as a parameter and returns the lateral surface area.', 'green'))
    print(colored('6) hemisphere() - Takes the radius as a parameter and returns the lateral surface area.', 'green'))

# Function - Cube
def cube(side):
    area = 4 * math.pow(side, 2)

    return area

# Function - Cuboid
def cuboid(length, width, height):
    area = 2 * height * (length + width)

    return area

# Function - Cone
def cone(radius, height):
    slantHeight = math.sqrt(math.pow(radius, 2) + math.pow(height, 2))
    
    area = 3.14 * radius * slantHeight

    return area

# Function - Cylinder
def cylinder(radius, height):
    area = 2 * 3.14 * radius * height

    return area

# Function - Sphere
def sphere(radius):
    area = 4 * 3.14 * math.pow(radius, 2)

    return area

# Function - Hemisphere
def hemisphere(radius):
    area = 2 * 3.14 * math.pow(radius, 2)

    return area