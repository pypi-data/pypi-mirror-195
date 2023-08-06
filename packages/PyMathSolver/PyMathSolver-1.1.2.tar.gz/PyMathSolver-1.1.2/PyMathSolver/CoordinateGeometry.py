# PyMathSolver - Coordinate Geometry

# Imports
from simple_colors import *
import Numbers

# Function - About
def about():
    print(magenta("\nCoordinate Geometry is the study of geometry using the coordinate points and planes. There are 3 axes: X-Axis, Y-Axis, and Z-Axis. Hence, there are also 3 planes: XY-Plane, YZ-Place, and XZ-Plane."))

    print(magenta("\nX-Coordinate - Abscissa"))
    print(magenta("Y-Coordinate - Ordinate"))
    print(magenta("Z-Coordinate - Applicate"))

    print(magenta("\nPyMathSolver.CoordinateGeometry has the following functions:"))
    print(magenta("\n1) ") + magenta("distance()", ["bold", "underlined"]) + magenta(" - Takes the coordinates of Point 1 and Point 2 as parameters and returns the distance."))
    print(magenta("2) ") + magenta("collinear()", ["bold", "underlined"]) + magenta(" - Takes the coordinates of Point 1, Point 2, and Point 3 and checks if the 3 points are collinear. It returns a boolean."))
    print(magenta("3) ") + magenta("section()", ["bold", "underlined"]) + magenta(" - Takes the coordinates of Point 1, Point 2, the Ratio, and 'typeOfSection' as parameters. 'typeOfSection' is either 'Internal' or 'External'. It returns the coordinates of the point which divides the given coordinates in the given ratio."))

    print(red("\nNOTE:", "bold") + red(" The coordinates of a point should be in the form of a tuple. Both points should be in the form (x₁, y₁) and (x₂, y₂) or (x₁, y₁, z₁) and (x₂, y₂, z₂). The ratio should be in the form (m, n)."))

    print()

# Function - Distance
def distance(point1, point2):
    distance = None

    if (isinstance(point1, tuple) and  isinstance(point2, tuple)):
        if (len(point1) == 2 and len(point2) == 2 or len(point1) == 3 and len(point2) == 3):
            x1 = point1[0]
            x2 = point2[0]

            y1 = point1[1]
            y2 = point2[1]

            newX = x2 - x1
            newY = y2 - y1

            if (len(point1) == 2 and len(point2) == 2): # 2D
                distance = Numbers.squareRoot(Numbers.power(newX, 2) + Numbers.power(newY, 2))
            else: # 3D
                z1 = point1[2]
                z2 = point2[2]

                newZ = z2 - z1

                distance = Numbers.squareRoot(Numbers.power(newX, 2) + Numbers.power(newY, 2) + Numbers.power(newZ, 2))

            return distance
        else:
            raise Exception("Both tuples should be in the form (x₁, y₁) and (x₂, y₂) or (x₁, y₁, z₁) and (x₂, y₂, z₂).")
    else:
        raise TypeError("Both Point 1 and Point 2 should be in the form of a tuple.")

# Function - Collinear
def collinear(point1, point2, point3):
    isCollinear = False

    if (isinstance(point1, tuple) and isinstance(point2, tuple) and isinstance(point2, tuple)):
        if (len(point1) == 2 and len(point2) == 2 or len(point1) == 3 and len(point2) == 3):
            point1point2 = distance(point1, point2)
            point2point3 = distance(point2, point3)
            point1point3 = distance(point1, point3)

            if (point1point3 == point1point2 + point2point3):
                isCollinear = True
            else:
                isCollinear = False
            
            return isCollinear
        else:
            raise Exception("The 3 tuples should be in the form (x₁, y₁) and (x₂, y₂) or (x₁, y₁, z₁) and (x₂, y₂, z₂).")
    else:
        raise TypeError("The 3 points should be in the form of a tuple.")

# Function - Section
def section(point1, point2, ratio, typeOfSection="Internal"):
    section = None

    if (typeOfSection == "Internal" or typeOfSection == "External"):
        if (isinstance(point1, tuple) and  isinstance(point2, tuple) and isinstance(ratio, tuple)):
            if (len(point1) == 2 and len(point2) == 2 or len(point1) == 3 and len(point2) == 3):
                x1 = point1[0]
                x2 = point2[0]
    
                y1 = point1[1]
                y2 = point2[1]
    
                m = ratio[0]
                n = ratio[1]
    
                if (len(point1) == 2 and len(point2) == 2): # 2D
                    if (typeOfSection == "Internal"):
                        section1 = ((m * x2) + (n * x1)) / (m + n)
                        section2 = ((m * y2) + (n * y1)) / (m + n)
                    elif (typeOfSection == "External"):
                        section1 = ((m * x2) - (n * x1)) / (m - n)
                        section2 = ((m * y2) - (n * y1)) / (m - n)

                    section = (section1, section2)
                else: # 3D
                    z1 = point1[2]
                    z2 = point2[2]

                    if (typeOfSection == "Internal"):
                        section1 = ((m * x2) + (n * x1)) / (m + n)
                        section2 = ((m * y2) + (n * y1)) / (m + n)
                        section3 = ((m * z2) + (n * z1)) / (m + n)
                    elif (typeOfSection == "External"):
                        section1 = ((m * x2) - (n * x1)) / (m - n)
                        section2 = ((m * y2) - (n * y1)) / (m - n)
                        section3 = ((m * z2) - (n * z1)) / (m - n)

                    section = (section1, section2, section3)

                return section
            else:
                raise Exception("Both tuples should be in the form (x₁, y₁) and (x₂, y₂) or (x₁, y₁, z₁) and (x₂, y₂, z₂). The ratio should be in the form (m, n).")
        else:
            raise TypeError("Point 1, Point 2, and the Ratio should be in the form of a tuple.")
    else:
        raise Exception("The paramater 'typeOfSection' should be either Internal or External.")