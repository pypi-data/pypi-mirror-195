# PyMathSolver - Quadratic

# Imports
from termcolor import colored
import math

# Function - About
def about():
    print(colored('\nA Quadratic Equation is an algebraic expression of the second degree in X.', 'green'))

    print(colored('\nThe standard form is ax\u00b2 + bx + c = 0. A and B are the coefficients and X is the variable.', 'green'))

    print(colored('\nPyMathSolver.Quadratic has the following functions:', 'green'))
    print(colored('\n1) findRoots() - This function finds the roots of the Quadratic Equation and returns the 2 roots as a tuple. It has 3 parameters (Integers): Values of A, B, and C.', 'green'))

# Function - Find Roots
def findRoots(a, b, c):
    newA = float(a)
    newB = float(b)
    newC = float(c)

    discriminant = math.sqrt((b**2) - (4*a*c))

    alpha = (-b + discriminant) / (2*a)
    beta = (-b - discriminant) / (2*a)

    return (alpha, beta)