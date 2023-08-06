# PyMathSolver - Complex Numbers

# Imports
from simple_colors import *
import math
import cmath

# Function - About
def about():
    print(magenta("\nA ") + magenta("Complex Number", "bold") + magenta(" is a number in the form '") + magenta("z = a + ib", "italic") + magenta("'. In Python, we define a complex number as '") + magenta("z = a + bj", "italic") + magenta("'."))

    print(magenta("\nz = Complex Number"))
    print(magenta("a = Real Part"))
    print(magenta("i/j = Iota (√-1)"))
    print(magenta("b = Imaginary Part"))

    print(green("\nPyMathSolver.ComplexNumbers", "bold") + green(" has the following functions:"))

    print(green("\nAlgebra:"))
    print(green("\n1) ") + green("add()", ["bold", "underlined"]) + green(" - Parameters: 2 Complex Numbers"))
    print(green("2) ") + green("subtract()", ["bold", "underlined"]) + green(" - Parameters: 2 Complex Numbers"))
    print(green("3) ") + green("multiply()", ["bold", "underlined"]) + green(" - Parameters: 2 Complex Numbers"))
    print(green("4) ") + green("divide()", ["bold", "underlined"]) + green(" - Parameters: 2 Complex Numbers"))

    print(green("\nModulus, Conjugate, and Multiplicative Inverse:"))
    print(green("\n5) ") + green("modulus()", ["bold", "underlined"]) + green(" - Parameters: Complex Number"))
    print(green("6) ") + green("conjugate()", ["bold", "underlined"]) + green(" - Parameters: Complex Number"))
    print(green("7) ") + green("multiplicativeInverse()", ["bold", "underlined"]) + green(" - Parameters: Complex Number"))

    print(green("\nPolar Representation:"))
    print(green("\n8) ") + green("polar()", ["bold", "underlined"]) + green(" - Parameters: Complex Number"))

    print()

### ALGEBRA ###

def addition(z1, z2):
    return z1 + z2

def subtraction(z1, z2):
    return z1 - z2

def multiplication(z1, z2):
    return z1 * z2

def divide(z1, z2):
    return z1 / z2

### MODULUS, CONJUGATE, AND MULTIPLICATIVE INVERSE ###

def modulus(z):
    return abs(z)

def conjugate(z):
    return z.conjugate()

def multiplicativeInverse(z):
    conj = conjugate(z)
    mod = modulus(z)

    return conj / (math.pow(mod, 2))

### POLAR REPRESENTATION ###

def polar(z):
    return cmath.polar(z)