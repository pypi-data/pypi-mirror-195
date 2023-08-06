# PyMathSolver - Geometry

# Imports
from simple_colors import *
import math

# Function - About
def about():
    print(magenta("\nGeometry", "bold") + magenta(" is the branch of science and mathematics that is concerned with properties of of space such as the distance, shape, volume, area, size, and relative position of figures."))

    print(magenta("\nArea", ["bold", "underlined"]) + magenta(" is the measure of a shape\'s size on a surface. ") + magenta("Volume", ["bold", "underlined"]) + magenta(" is a measure of three-dimensional space. Also, the amount of space that an object occupies."))

    print(magenta("\nSurface Area", ["bold", "underlined"]) + magenta(" of a solid object is the measure of the total area that the surface of the object occupies. ") + magenta("Lateral Surface Area", ["bold", "underlined"]) + magenta(" is the surface area of the object, except the areas of the top and bottom."))

    print(green("\nPyMathSolver.Geometry", "bold") + green(" has the following functions:"))

    print(green("\nTo Find Area:"))
    print(green("\n1) ") + green("squareArea()", ["bold", "underlined"]) + green(" - Parameters: Length of the Side"))
    print(green("2) ") + green("rectangleArea()", ["bold", "underlined"]) + green(" - Parameters: Length and Width"))
    print(green("3) ") + green("triangleArea()", ["bold", "underlined"]) + green(" - Parameters: Base and Height"))
    print(green("4) ") + green("circleArea()", ["bold", "underlined"]) + green(" - Parameters: Radius"))
    print(green("5) ") + green("parallelogramArea()", ["bold", "underlined"]) + green(" - Parameters: Base and Height"))
    print(green("6) ") + green("trapeziumArea()", ["bold", "underlined"]) + green(" - Parameters: Length of 2 Bases and Height"))
    print(green("7) ") + green("rhombusArea()", ["bold", "underlined"]) + green(" - Parameters: Length of Both Diagonals"))

    print(green("\nTo Find Volume:"))
    print(green("\n8) ") + green("cubeVolume()", ["bold", "underlined"]) + green(" - Parameters: Length of the Side"))
    print(green("9) ") + green("cuboidVolume()", ["bold", "underlined"]) + green(" - Parameters: Length, Width, and Height"))
    print(green("10) ") + green("coneVolume()", ["bold", "underlined"]) + green(" - Parameters: Radius and Height"))
    print(green("11) ") + green("cylinderVolume()", ["bold", "underlined"]) + green(" - Parameters: Radius and Height"))
    print(green("12) ") + green("sphereVolume()", ["bold", "underlined"]) + green(" - Parameters: Radius"))
    print(green("13) ") + green("hemisphereVolume()", ["bold", "underlined"]) + green(" - Parameters: Radius"))
    print(green("14) ") + green("pyramidVolume()", ["bold", "underlined"]) + green(" - Parameters: Length, Width, and Height"))

    print(green("\nTo Find Surface Area:"))
    print(green("\n15) ") + green("cubeSA()", ["bold", "underlined"]) + green(" - Parameters: Length of the Side"))
    print(green("16) ") + green("cuboidSA()", ["bold", "underlined"]) + green(" - Parameters: Length, Width, and Height"))
    print(green("17) ") + green("coneSA()", ["bold", "underlined"]) + green(" - Parameters: Radius and Height"))
    print(green("18) ") + green("cylinderSA()", ["bold", "underlined"]) + green(" - Parameters: Radius and Height"))
    print(green("19) ") + green("sphereSA()", ["bold", "underlined"]) + green(" - Parameters: Radius"))
    print(green("20) ") + green("hemisphereSA()", ["bold", "underlined"]) + green(" - Parameters: Radius"))

    print(red("\nNOTE:", ["bold", "underlined"]) + red(" To find the Lateral Surface Area of an object, pass the parameter 'lateral=True' in the functions 15-20."))

    print(green("\nMiscellaneous:"))
    print(green("\n21) ") + green("circumference()", ["bold", "underlined"]) + green(" - Parameters: Radius"))
    print(green("22) ") + green("hypotenuse()", ["bold", "underlined"]) + green(" - Parameters: Length of Other 2 Sides"))
    print(green("23) ") + green("heronsFormula()", ["bold", "underlined"]) + green(" - Parameters: Length of 3 Sides of Triangle"))
    print(green("24) ") + green("arclength()", ["bold", "underlined"]) + green(" - Parameters: Angle (in Radians) and Length of Radius"))

    print()

### AREA ###

def squareArea(side):
    return side * side

def rectangleArea(length, width):
    return length * width

def triangleArea(base, height):
    return 0.5 * base * height

def circleArea(radius):
    return 3.14 * math.pow(radius, 2)

def parallelogramArea(base, height):
    return base * height

def trapeziumArea(base1, base2, height):
    return 0.5 * height * (base1 + base2)

def rhombusArea(diagonal1, diagonal2):
    return (diagonal1 * diagonal2) / 2

### VOLUME ###

def cubeVolume(side):
    return math.pow(side, 3)

def cuboidVolume(length, width, height):
    return length * width * height

def coneVolume(radius, height):
    return (1/3) * 3.14 * math.pow(radius, 2) * height

def cylinderVolume(radius, height):
    return 3.14 * math.pow(radius, 2) * height

def sphereVolume(radius):
    return (4/3) * 3.14 * math.pow(radius, 3)

def hemisphereVolume(radius):
    return (2/3) * 3.14 * math.pow(radius, 3)

def pyramidVolume(length, width, height):
    return (length * width * height) / 3

### SURFACE AREA ###

def cubeSA(side, lateral=False):
    if (lateral == False):
        area = 6 * math.pow(side, 2)
    else:
        area = 4 * math.pow(side, 2)

    return area

def cuboidSA(length, width, height, lateral=False):
    if (lateral == False):
        area = 2 * ((length * width) + (width * height) + (length * height))
    else:
        area = 2 * height * (length + width)

    return area

def coneSA(radius, height, lateral=False):
    slantHeight = math.sqrt(math.pow(radius, 2) + math.pow(height, 2))

    if (lateral == False):
        area = 3.14 * radius * (slantHeight + radius)
    else:
        area = 3.14 * radius * slantHeight

    return area

def cylinderSA(radius, height, lateral=False):
    if (lateral == False):
        area = 2 * 3.14 * radius * (radius + height)
    else:
        area = 2 * 3.14 * radius * height

    return area

def sphereSA(radius, lateral=False):
    if (lateral == False):
        area = 4 * 3.14 * math.pow(radius, 2)
    else:
        area = 4 * 3.14 * math.pow(radius, 2)

    return area

def hemisphereSA(radius, lateral=False):
    if (lateral == False):
        area = 3 * 3.14 * math.pow(radius, 2)
    else:
        area = 2 * 3.14 * math.pow(radius, 2)

    return area

### MISCELLANEOUS ###

def circumference(radius):
    return 2 * 3.14 * radius

def hypotenuse(side1, side2):
    return math.sqrt(math.pow(side1, 2) + math.pow(side2, 2))

def heronsFormula(side1, side2, side3):
    semiPerimeter = (side1 + side2 + side3) / 2

    return math.sqrt(semiPerimeter * (semiPerimeter - side1) * (semiPerimeter - side2) * (semiPerimeter - side3))

def arcLength(angle, radius):
    return radius * angle