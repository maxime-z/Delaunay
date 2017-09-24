# Geometric description for domain


from sympy.geometry import *



class Geometry2D(object):

    def __init__(self,outer,inner=None):

        self.outer = outer
        self.inner = inner
        if not self.domainCheck():
            self.ogouter = None
            self.inner = None
        else:
            print('Domain created successfully.')

    def domainCheck(self):
        if self.inner == None:
            return True
        else:
            for entity in self.inner:
                if intersection(entity,self.outer):
                    raise ValueError('Outer boundary intersects with inner boundaries!')
            return True

    def isPointIn(self, p):
        if not self.outer.encloses(p):
            return False
        else:
            return not self.enclosedByInteriorBoundaries(p)

    def enclosedByInteriorBoundaries(self,p):
        if self.inner == None:
            return False
        else:
            for entity in self.inner:
                if entity.encloses(p):
                    return True
            return False

    def enclosedByExteriorBoundaries(self,p):
        if self.outer.encloses(p):
            return True
        else:
            return False

    # Return a tuple (xmin, ymin, xmax, ymax) representing the bounding rectangle
    # for the geometric figure.
    def outerBounds(self):
        return self.outer.bounds

    def intersections(self,entities):
        intersects = list()
        for ent in entities:
            intersects = intersects + self.outer.intersection(ent)
            for innerBound in self.inner:
                intersects = intersects + innerBound.intersection(ent)
        return intersects


if __name__ == '__main__':

    # test cases
    ## outer boundary
    x1,x2,x3,x4 = map(Point,[(-2,-2),(2,-2),(2,2),(-2,2)])
    outBoundary = Polygon(x1,x2,x3,x4)

    ## inner boundary
    innerBoundary = [Circle(Point(0,0),1)]

    d = Geometry2D(outBoundary,innerBoundary)

    print(d.outerBounds())

    ## Test point enclosed or not
    print(d.isPointIn(Point(-1.9,-1.9)))
    print(d.isPointIn(Point(1.5,0)))