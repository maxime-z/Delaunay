from meshGenerator2D import *
from sympy.geometry import *


class Mesh2D(object):
    def __init__(self,vertices,triNums):
        self.vertices = vertices
        self.triNums = triNums


if __name__ == '__main__':
    # test case
    ## outer boundary
    # a = 3
    # x1, x2, x3, x4 = map(Point, [(-a, -a), (a, -a), (a, a), (-a, a)])
    # outBoundary = Polygon(x1, x2, x3, x4)
    outBoundary = Circle(Point(0,0), 4)

    ## inner boundary
    innerBoundaries = [Circle(Point(0, 0), 2)]
    # innerBoundaries = [Circle(Point(-0.5, 0.5), 2), Circle(Point(1, -0.5), 1.5)]

    ## Domain definition
    d = Geometry2D(outBoundary, innerBoundaries)
    meshGenerator = DelaunayGridMeshGenerator(d, 0.7)
    a = meshGenerator.generateMesh()

    print('Mesh generation done')