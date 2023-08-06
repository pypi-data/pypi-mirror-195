# PyMathSolver - Trigonometry

# Imports
from simple_colors import *
import math

# Function - About
def about():
    print(magenta("\nTrigonometry", "bold") + magenta(" is a branch of mathematics that deals with the relations of the sides and angles of triangles and with the relevant functions of any angles."))

    print(green("\nPyMathSolver.Trigonometry", "bold") + green(" has the following functions:"))

    print(green("\nConversions:"))
    print(green("\n1) ") + green("degreesToRadians()", ["bold", "underlined"]) + green(" - Parameters: Degrees"))
    print(green("2) ") + green("radiansToDegrees()", ["bold", "underlined"]) + green(" - Parameters: Radians"))

    print(green("\nFind Trigonometric Ratios:"))
    print(green("\n3) ") + green("sin()", ["bold", "underlined"]) + green(" - Parameters: Radians"))
    print(green("4) ") + green("cos()", ["bold", "underlined"]) + green(" - Parameters: Radians"))
    print(green("5) ") + green("tan()", ["bold", "underlined"]) + green(" - Parameters: Radians"))
    print(green("6) ") + green("cosec()", ["bold", "underlined"]) + green(" - Parameters: Radians"))
    print(green("7) ") + green("sec()", ["bold", "underlined"]) + green(" - Parameters: Radians"))
    print(green("8) ") + green("cot()", ["bold", "underlined"]) + green(" - Parameters: Radians"))

    print()

### CONVERSIONS ###

def degreesToRadians(degrees):
    return degrees * (3.14/180)

def radiansToDegrees(radians):
    return radians * (180/3.14)

### TRIGONOMETRIC RATIOS ###

def sin(radians):
    return math.sin(radians)

def cos(radians):
    return math.cos(radians)

def tan(radians):
    return math.tan(radians)

def cosec(radians):
    return 1 / (sin(radians))

def sec(radians):
    return 1 / (cos(radians))

def cot(radians):
    return 1 / (tan(radians))