# PyMathSolver - Numbers

# Imports
from simple_colors import *

# Function - About
def about():
    print(green("\nPyMathSolver.Numbers", "bold") + green(" has the following functions:"))
    print(green("\n1) ") + green("hcf()", ["bold", "underlined"]) + green(" - Takes 2 numbers as parameters and returns the HCF."))
    print(green("2) ") + green("lcm()", ["bold", "underlined"]) + green(" - Takes 2 numbers as parameters and returns the LCM."))
    print(green("3) ") + green("prime()", ["bold", "underlined"]) + green(" - Takes a number as a parameter and checks if the number is a prime or not. It returns a boolean."))
    print(green("4) ") + green("power()", ["bold", "underlined"]) + green(" - Takes a number and exponent as parameters and returns the raised number to it\'s exponent."))
    print(green("5) ") + green("square()", ["bold", "underlined"]) + green(" - Takes a number as a parameter and returns the square of that number."))
    print(green("6) ") + green("cube()", ["bold", "underlined"]) + green(" - Takes a number as a parameter and returns the cube of that number."))
    print(green("7) ") + green("squareRoot()", ["bold", "underlined"]) + green(" - Takes a number as a parameter and returns the square root of that number."))

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
    return power(number, 2)

# Function - Cube
def cube(number):
    return power(number, 3)

# Function - Square Root
def squareRoot(number):
    return number ** 0.5