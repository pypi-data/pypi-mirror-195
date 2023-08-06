# PyMathSolver - Numbers

# Imports
from termcolor import colored
import math

# Function - About
def about():
    print(colored('\nPyMathSolver.Numbers has the following functions:', 'green'))
    print(colored('\n1) hcf() - Takes 2 numbers as parameters and returns the HCF.', 'green'))
    print(colored('2) lcm() - Takes 2 numbers as parameters and returns the LCM.', 'green'))
    print(colored('3) prime() - Takes a number as a parameter and checks if the number is a prime or not. It returns a boolean.', 'green'))
    print(colored('4) power() - Takes a number and exponent as parameters and returns the raised number to it\'s exponent.', 'green'))
    print(colored('5) square() - Takes a number as a parameter and returns the square of that number.', 'green'))
    print(colored('6) cube() - Takes a number as a parameter and returns the cube of that number.', 'green'))

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
def power(number, exponent):
    num = math.pow(number, exponent)

    return num

# Function - Square
def square(number):
    num = math.pow(number, 2)

    return num

# Function - Cube
def cube(number):
    num = math.pow(number, 3)

    return num