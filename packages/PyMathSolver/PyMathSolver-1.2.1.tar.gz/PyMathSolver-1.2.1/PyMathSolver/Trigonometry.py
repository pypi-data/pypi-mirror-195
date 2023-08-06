# PyMathSolver - Trigonometry

# Imports
from simple_colors import *
import math

# Function - About
def about():
    print(magenta("\nTrigonometry is a branch of mathematics that deals with the relations of the sides and angles of triangles and with the relevant functions of any angles."))

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
    radians = degrees * (3.14/180)

    return radians

def radiansToDegrees(radians):
    degrees = radians * (180/3.14)
    
    return degrees

### TRIGONOMETRIC RATIOS ###

def sin(radians):
    sin = math.sin(radians)

    return sin

def cos(radians):
    cos = math.cos(radians)

    return cos

def tan(radians):
    tan = math.tan(radians)

    return tan

def cosec(radians):
    cosec = 1 / (sin(radians))

    return cosec

def sec(radians):
    sec = 1 / (cos(radians))

    return sec

def cot(radians):
    cot = 1 / (tan(radians))

    return cot