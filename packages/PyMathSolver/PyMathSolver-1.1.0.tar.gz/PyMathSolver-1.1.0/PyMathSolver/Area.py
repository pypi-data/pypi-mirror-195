# PyMathSolver - Area

# Imports
from termcolor import colored
import math

# Function - About
def about():
    print(colored('\nArea is the measure of a shape\'s size on a surface.', 'green'))

    print(colored('\nPyMathSolver.Area has the following functions:', 'green'))
    print(colored('\n1) square() - Takes the length of the side as a parameter and returns the area.', 'green'))
    print(colored('2) rectangle() - Takes the length and width as parameters and returns the area.', 'green'))
    print(colored('3) triangle() - Takes the base and height as parameters and returns the area.', 'green'))
    print(colored('4) circle() - Takes the radius as a parameter and returns the area.', 'green'))
    print(colored('5) parallelogram() - Takes the base and height as parameters and returns the area.', 'green'))
    print(colored('6) trapezium() - Takes the length of the 2 bases and height as parameters and returns the area.', 'green'))
    print(colored('7) rhombus() - Takes the length of both the diagonals as parameters and returns the area.', 'green'))

# Function - Square
def square(side):
    area = side * side

    return area

# Function - Rectangle
def rectange(length, width):
    area = length * width

    return area

# Function - Triangle
def triangle(base, height):
    area = 0.5 * base * height

    return area

# Function - Circle
def circle(radius):
    area = 3.14 * math.pow(radius, 2)

    return area

# Function - Parallelogram
def parallelogram(base, height):
    area = base * height

    return area

# Function - Trapezium
def trapezium(base1, base2, height):
    area = 0.5 * height * (base1 + base2)

    return area

# Function - Rhombus
def rhombus(diagonal1, diagonal2):
    area = (diagonal1 * diagonal2) / 2

    return area