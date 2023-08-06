# PyMathSolver - Quadratic

# Imports
from simple_colors import *
import Numbers

# Function - About
def about():
    print(magenta("\nA Quadratic Equation is an algebraic expression of the second degree in X."))

    print(magenta("\nThe standard form is ax\u00b2 + bx + c = 0. A and B are the coefficients and X is the variable."))

    print(magenta("\nPyMathSolver.Quadratic has the following functions:"))
    print(magenta("\n1) ") + magenta("findRoots()", ["bold", "underlined"]) + magenta(" - This finds the roots of the Quadratic Equation and returns the 2 roots as a tuple. It has 3 parameters (Integers): Values of A, B, and C."))

    print()

# Function - Find Roots
def findRoots(a, b, c):
    newA = float(a)
    newB = float(b)
    newC = float(c)

    discriminant = Numbers.squareRoot((b**2) - (4*a*c))

    alpha = (-b + discriminant) / (2*a)
    beta = (-b - discriminant) / (2*a)

    return (alpha, beta)