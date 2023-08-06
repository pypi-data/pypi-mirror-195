# PyMathSolver - Numbers

# Imports
from simple_colors import *

# Function - About
def about():
    print(magenta("\nPyMathSolver.Numbers has the following functions:"))
    print(magenta("\n1) ") + magenta("hcf()", ["bold", "underlined"]) + magenta(" - Takes 2 numbers as parameters and returns the HCF."))
    print(magenta("2) ") + magenta("lcm()", ["bold", "underlined"]) + magenta(" - Takes 2 numbers as parameters and returns the LCM."))
    print(magenta("3) ") + magenta("prime()", ["bold", "underlined"]) + magenta(" - Takes a number as a parameter and checks if the number is a prime or not. It returns a boolean."))
    print(magenta("4) ") + magenta("power()", ["bold", "underlined"]) + magenta(" - Takes a number and exponent as parameters and returns the raised number to it\'s exponent."))
    print(magenta("5) ") + magenta("square()", ["bold", "underlined"]) + magenta(" - Takes a number as a parameter and returns the square of that number."))
    print(magenta("6) ") + magenta("cube()", ["bold", "underlined"]) + magenta(" - Takes a number as a parameter and returns the cube of that number."))
    print(magenta("7) ") + magenta("squareRoot()", ["bold", "underlined"]) + magenta(" - Takes a number as a parameter and returns the square root of that number."))

    print()

# Function - HCF
def hcf(num1, num2):
    hcf = 1

    for i in range(1, min(num1, num2)):
        if num1 % i == 0 and num2 % i == 0:
            hcf = i
    
    return hcf

# Function - LCM
def lcm(num1, num2):
    if (num1 > num2):
        greater = num1
    else:
        greater = num2
    
    while True:
        if ((greater % num1 == 0) and (greater % num2 == 0)):
            lcm = greater
            break
        greater += 1
    
    return lcm

# Function - Prime
def prime(number):
    isPrime = False

    if (number < 1):
        isPrime = False
    else:
        for i in range(2, int(number/2) + 1):
            if (number % i == 0):
                isPrime = False
                break
        else:
            isPrime = True

    return isPrime

# Function - Power
def power(base, exponent):
    num = 1

    for i in range(exponent, 0, -1):
        num *= base

    return num

# Function - Square
def square(number):
    num = power(number, 2)

    return num

# Function - Cube
def cube(number):
    num = power(number, 3)

    return num

# Function - Square Root
def squareRoot(number):
    num = number ** 0.5

    return num