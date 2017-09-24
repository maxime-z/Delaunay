from sympy import *
from sympy.geometry import Point, Circle

x = Point(0,0)
y = Point(1,1)
z = Point(2,2)

a = Point.is_collinear(x,y,z)

print(a)

c = Circle(x,5)

