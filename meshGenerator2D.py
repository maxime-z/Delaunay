from geometry2D import Geometry2D
from mesh2D import Mesh2D
from sympy.geometry import *
from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt


class MeshGenerator2D(object):
    def __init__(self, geometry2D):
        self.domain = geometry2D

    def generateMesh(self):
        pass

# Delaynay mesh generation version 1:
#   Combining the function numpy.meshgrid to locate the interior point.
#   Then call the scipy.spatial.Delaunay on the point cloud to do the triangulation.
class DelaunayGridMeshGenerator(MeshGenerator2D):

    def __init__(self,geometry2D,finess=None):
        # MeshGenerator2D(geometry2D)
        self.geometry2D = geometry2D
        self.finess = finess

    def generateMesh(self):
        points = self.generatePointCloud()
        tri = Delaunay(points)
        tri.simplices = self.filterTriangles(tri)
        self.plotMesh(points,tri)
        return Mesh2D(tri.points,tri.simplices)
        print("Generate Mesh Done")

    def generatePointCloud(self):
        xmin, ymin, xmax, ymax = map(float,self.geometry2D.outerBounds());

        x_size = xmax-xmin
        y_size = ymax-ymin
        if self.finess == None:
            dl = max(x_size,y_size)/10
        else:
            dl = self.finess
        nx = round(x_size / dl)
        ny = round(y_size / dl)
        x = np.linspace(float(xmin),float(xmax),num=nx)
        y = np.linspace(float(ymin),float(ymax),num=ny)
        x0, y0 = np.meshgrid(x, y)
        innerPoints = np.vstack((x0.ravel(),y0.ravel())).T
        innerPoints = self.filterPoints(innerPoints)

        #points on the boundaries(exterior & interior)
        grid_lines = list()
        for xi in x:
            # if not (np.isclose(xi,xmin) or np.isclose(xi,xmax)):
            grid_lines.append(Line(Point(xi,ymin),Point(xi,ymax)))
        for yi in y:
            # if not (np.isclose(yi,ymin) or np.isclose(yi,ymax)):
            grid_lines.append(Line(Point(xmin,yi),Point(xmax,yi)))

        edgeIntersects = self.geometry2D.intersections(grid_lines)
        xx = list()
        yy = list()
        for p in edgeIntersects:
            if isinstance(p, Point) and not self.geometry2D.enclosedByInteriorBoundaries(p):
                xx.append(float(p.x))
                yy.append(float(p.y))
        edgePoints = np.vstack((xx,yy)).T

        points = np.vstack((innerPoints,edgePoints))
        return np.unique(points,axis=0)
        # return np.unique(points)

    def filterPoints(self,points):
        nPoints = points.shape[0]
        index = list()
        for i in range(nPoints):
            p = points[i]
            if self.geometry2D.enclosedByInteriorBoundaries(Point(p[0],p[1])):
                index.append(i)
            elif not self.geometry2D.enclosedByExteriorBoundaries(Point(p[0],p[1])):
                index.append(i)

        ans = np.delete(points,index,axis=0)
        return ans

    def filterTriangles(self,tris):
        index = list()
        for j, s in enumerate(tris.simplices):
            p = tris.points[s].mean(axis=0)
            if self.geometry2D.enclosedByInteriorBoundaries(Point(p[0],p[1])):
                index.append(j)
        return np.delete(tris.simplices,index,axis=0)

    def plotMesh(self,points,tri):
        plt.triplot(points[:, 0], points[:, 1], tri.simplices.copy())
        plt.plot(points[:, 0], points[:, 1], 'o')
        mng = plt.get_current_fig_manager()
        # mng.full_screen_toggle()
        plt.show()



if __name__ == '__main__':
    # test cases
    print("To be continued...")

