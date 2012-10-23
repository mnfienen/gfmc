import numpy as np
from scipy.spatial import Delaunay
inroot = 'Diffuser'
points = np.loadtxt(inroot + '.csv',delimiter =',',skiprows=1)

tri = Delaunay(points)

edge_points = []
edges = set()

def add_edge(i, j):
    """Add a line between the i-th and j-th points, if not in the list already"""
    if (i, j) in edges or (j, i) in edges:
        # already added
        return
    edges.add( (i, j) )
    edge_points.append(points[ [i, j] ])

# loop over triangles: 
# ia, ib, ic = indices of corner points of the triangle
for ia, ib, ic in tri.vertices:
    add_edge(ia, ib)
    add_edge(ib, ic)
    add_edge(ic, ia)

# plot it: the LineCollection is just a (maybe) faster way to plot lots of
# lines at once
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

lines = LineCollection(edge_points)
plt.figure()
plt.title('Delaunay triangulation')
plt.gca().add_collection(lines)
plt.plot(points[:,0], points[:,1], 'o', hold=1)
for i,x in enumerate(points):
    plt.text(x[0],x[1],'%d' %(i))
plt.gca().set_aspect('equal')
plt.savefig('triangles.pdf')
plt.show()

ofp = open(inroot + '.dat','w')
for line in tri.vertices:
    ofp.write('%d %d %d\n' %(line[0],line[1],line[2]))
ofp.close()
