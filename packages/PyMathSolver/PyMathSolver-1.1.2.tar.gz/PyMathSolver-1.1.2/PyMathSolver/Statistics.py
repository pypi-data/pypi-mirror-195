# PyMathSolver - Statistics

# Imports
from simple_colors import *

# Function - About
def about():
    print(magenta("\nStatistics is the science concerned with developing and studying methods for collecting, analyzing, interpreting, and presenting empirical data."))

    print(magenta("\nPyMathSolver.Statistics has the following functions:"))
    print(magenta("\n1) ") + magenta("mean()", ["bold", "underlined"]) + magenta(" - This function finds the mean of the data."))
    print(magenta("2) ") + magenta("mode()", ["bold", "underlined"]) + magenta(" - This function finds the mode of the data."))
    print(magenta("3) ") + magenta("median()", ["bold", "underlined"]) + magenta(" - This function finds the median of the data."))

    print(red("\nNOTE:", ["bold"]) + red(" The functions above take only one parameter. That parameter should be in the form of a list, tuple, or set."))

    print()

# Function - Mean
def mean(data):
    if (isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set)):
        if (data != None and sum(data) != 0):
            mean = sum(data) / len(data)

            return mean
        else:
            raise Exception("The data can't be null and the sum of the data can't be zero.")
    else:
        raise TypeError("The data should be in the form of a list, tuple, or set.")

# Function - Mode
def mode(data):
    if (isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set)):
        if (data != None and sum(data) != 0):
            mode = max(data)

            return mode
        else:
            raise Exception("The data can't be null and the sum of the data can't be zero.")
    else:
        raise TypeError("The data should be in the form of a list, tuple, or set.")

# Function - Median
def median(data):
    if (isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set)):
        if (data != None and sum(data) != 0):
            data.sort()
            mid = len(data) // 2
            median = (data[mid] + data[~mid]) / 2

            return median
        else:
            raise Exception("The data can't be null and the sum of the data can't be zero.")
    else:
        raise TypeError("The data should be in the form of a list, tuple, or set.")