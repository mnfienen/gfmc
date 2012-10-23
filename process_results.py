import numpy as np
import matplotlib as mpl
import os
mpl.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import shapefile
import sys


parfile = 'parse_proc.in'
pardat = open(parfile,'r').readlines()
outfilename = pardat[0].strip().split()[0]
inPHIfile = pardat[1].strip().split()[0]
difftol = 0.001

realizs = np.genfromtxt(inPHIfile,names=True,dtype=None)

allreals = realizs['realization']

# set up X, Y, Z, and Z_old
X,Y,Z = np.loadtxt('results/%s_%d' %(outfilename,allreals[0]),skiprows=1,delimiter=',',unpack=True)
Z_old = np.ones_like(Z)
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
        junkx,junky,inreal = np.loadtxt(infile,skiprows=1,delimiter=',',unpack=True)
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
pshape = shapefile.Writer(shapefile.POINT)        #set up the point shapefile
pshape.field('plume')
for i in np.arange(len(X)):
    pshape.point(X[i],Y[i])    # write to the shapefile
    pshape.record(cprob[i])
# save the shapefile
outshape = outfilename[:-4] + 'shape'
pshape.save(outshape)

# plot the convergence of probability discrepancies
alldiff = np.array(alldiff)
plt.figure()
plt.plot(np.arange(len(alldiff)),alldiff)
plt.title('Evolution of Max Prob Difference')
plt.xlabel('Realization Number')
plt.ylabel('Max Discrepancy of Prob')
plt.yscale('Log')
plt.savefig('Probability_history.pdf')
#plt.show()
