# PyMathSolver - Area

# Imports
from simple_colors import *
import Numbers

# Function - About
def about():
    print(magenta("\nArea is the measure of a shape\'s size on a surface."))

    print(magenta("\nPyMathSolver.Area has the following functions:"))
    print(magenta("\n1) ") + magenta("square()", ["bold", "underlined"]) + magenta(" - Takes the length of the side as a parameter and returns the area."))
    print(magenta("2) ") + magenta("rectangle()", ["bold", "underlined"]) + magenta(" - Takes the length and width as parameters and returns the area."))
    print(magenta("3) ") + magenta("triangle()", ["bold", "underlined"]) + magenta(" - Takes the base and height as parameters and returns the area."))
    print(magenta("4) ") + magenta("circle()", ["bold", "underlined"]) + magenta(" - Takes the radius as a parameter and returns the area."))
    print(magenta("5) ") + magenta("parallelogram()", ["bold", "underlined"]) + magenta(" - Takes the base and height as parameters and returns the area."))
    print(magenta("6) ") + magenta("trapezium()", ["bold", "underlined"]) + magenta(" - Takes the length of the 2 bases and height as parameters and returns the area."))
    print(magenta("7) ") + magenta("rhombus()", ["bold", "underlined"]) + magenta(" - Takes the length of both the diagonals as parameters and returns the area."))

    print()

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
    area = 3.14 * Numbers.power(radius, 2)

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