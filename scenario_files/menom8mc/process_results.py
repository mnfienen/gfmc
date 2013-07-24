import numpy as np
import matplotlib as mpl
import os
mpl.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import shapefile
import sys

def readfile(infile):
    indat = open(infile,'r').readlines()
    junkheader = indat.pop(0)
    inreal = list()
    for line in indat:
        inreal.append(line.strip().split()[-1].strip())
    inreal = np.array(inreal,dtype=float)
    return inreal


def write_lineshapefile(lshape,parts,name,Z):   
    lshape.line(parts)    # write to the line shapefile with model coordinates
    lshape.record(name,Z) 

parfile = sys.argv[1]
pardat = open(parfile,'r').readlines()
outfilename = pardat[0].strip().split()[0]
inPHIfile = pardat[1].strip().split()[0]
points_or_elements = pardat[2].strip().split()[0].lower()
difftol = 0.001

realizs = np.genfromtxt(inPHIfile,names=True,dtype=None)

allreals = realizs['realization']

# set up X, Y, Z, and Z_old
print 'opening --> results/%s_%d' %(outfilename,allreals[0])
if points_or_elements == 'p':
    X,Y,Z = np.loadtxt('results/%s_%d' %(outfilename,allreals[0]),skiprows=1,unpack=True)
    Z_old = np.ones_like(Z)
else:
    tmp = open('results/%s_%d' %(outfilename,allreals[0]),'r').readlines()
    Z_old = np.ones(len(tmp)-1)
Z = np.zeros_like(Z_old)
creal = 0
total_reals = 0
alldiff = []
# go through all realizations until reach the tolerance of discrepancies
for i in allreals:
    creal += 1

    # read in the latest in/out array
    infile = 'results/%s_%d' %(outfilename,i)
    try:
        inreal = readfile(infile)
        total_reals += 1
        Z += inreal
        cprob = Z / np.float(total_reals)
        print 'max prob = %f' %(np.max(cprob))
        # check the maximum difference in probabilities
        cdiff = np.max(np.abs(cprob-Z_old))
        alldiff.append(cdiff)
        print 'rockin realization %d of %d --> cdiff = %f' %(creal,len(allreals),cdiff)
        if cdiff < difftol:
            break
        else:
            Z_old = cprob.copy()
    except:
        
        continue
# make a shapefile of the probability maps
if points_or_elements == 'p':
    pshape = shapefile.Writer(shapefile.POINT)        #set up the point shapefile
    pshape.field('plume')
    for i in np.arange(len(X)):
        pshape.point(X[i],Y[i])    # write to the shapefile
        pshape.record(cprob[i])
    # save the shapefile
    outshape = outfilename[:-4] + 'shape_pts'
    pshape.save(outshape)
else:
    pshape = shapefile.Writer(shapefile.POLYLINE)        #set up the point shapefile
    pshape.field('elname')
    pshape.field('plume')
    indat = open('results/%s_%d' %(outfilename,allreals[0]),'r').readlines()
    junkus = indat.pop(0)
    X1 = list()
    Y1 = list()
    X2 = list()
    Y2 = list()
    ElName = list()
    for i,line in enumerate(indat):
        tmp = line.strip().split()
        X1.append(float(tmp[0].strip()))
        X2.append(float(tmp[2].strip()))
        Y1.append(float(tmp[1].strip()))                        
        Y2.append(float(tmp[3].strip()))
        ElName.append(tmp[4].strip())
        pshape.line([[[X1[i],Y1[i]],[X2[i],Y2[i]]]])
        pshape.record(ElName[i],cprob[i])   
    outshape = outfilename[:-4] + 'shape_polylines'
    pshape.save(outshape)
    
# plot the convergence of probability discrepancies
alldiff = np.array(alldiff)
plt.figure()
plt.plot(np.arange(len(alldiff)),alldiff)
plt.title('Evolution of Max Prob Difference')
plt.xlabel('Realization Number')
plt.ylabel('Max Discrepancy of Prob')
plt.yscale('Log')
plt.savefig(outfilename + 'Probability_history.pdf')
#plt.show()
