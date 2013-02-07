import numpy as np
import matplotlib as mpl
import os
mpl.rcParams['pdf.fonttype'] = 42
import matplotlib.pyplot as plt
import sys

numreals = 1500
parfile = sys.argv[1]
pardat = open(parfile,'r').readlines()
outfilename = pardat[0].strip().split()[0]

uncompress_flag = True
os.chdir('results')
# uncompress all the output files and rename the .out file
if uncompress_flag:
    for i in np.arange(numreals):
        print 'uncompressing realization number %d' %(i)
        os.system('tar -xzf MC_%d.tar ' %(i))
        os.system('mv %s %s_%d' %(outfilename,outfilename,i))

os.chdir('..')        
# now read through the meta output to check on PHI and convergence
allPHI = []
allCONV = []
allTIME = []
for i in np.arange(numreals):
	try:
	    indat = open('results/MC_%d.mcres' %(i),'r').readlines()
	    tmp = indat[1].strip().split(',')
	    allPHI.append(float(tmp[0]))
	    allCONV.append(tmp[1])
	except:
	    print 'no dice on realization %d' %(i)
	    allPHI.append(np.nan)
	    allCONV.append(np.nan)	    
allPHI = np.array(allPHI)
allCONV = np.array(allCONV,dtype=bool)



# plot a PDF and CDF of PHI values
plt.figure()
plt.hist(allPHI[np.where(~np.isnan(allPHI))],bins=200)
plt.title('Histogram for PHI')
plt.savefig(outfilename + 'PHI_hist.pdf')

plt.figure()
PHI_sort_norm = np.sort(allPHI[np.where(~np.isnan(allPHI))])/np.max(allPHI[np.where(~np.isnan(allPHI))])
plt.plot(PHI_sort_norm)
plt.title('Empirical CDF for PHI')
plt.savefig(outfilename + 'PHI_CDF.pdf')

# truncate allPHI
medianPHI = np.median(allPHI)
allPHI[allPHI>(2*medianPHI)] = np.nan
allPHI[allPHI<(0.5*medianPHI)] = np.nan

# write out PHI into a file
ofpPHI = open('PHI_records.dat','w')
ofpPHI.write('%-16s%-16s\n' %('realization','PHI'))
for i,cPHI in enumerate(allPHI):
    if ~np.isnan(cPHI):
        ofpPHI.write('%-16d%-16e\n' %(i,cPHI))
ofpPHI.close()

allPHItrimmed = allPHI[np.where(~np.isnan(allPHI))]
# plot a PDF and CDF of PHI values
plt.figure()
plt.hist(allPHItrimmed,bins=100)
plt.title('Histogram for PHI')
plt.savefig(outfilename + 'PHI_hist_trimmed.pdf')

plt.figure()
PHI_sort_norm = np.sort(allPHItrimmed)/np.max(allPHItrimmed)
plt.plot(PHI_sort_norm)
plt.title('Empirical CDF for trimmed PHI')
plt.savefig(outfilename + 'PHI_CDF_trimmed.pdf')


# look at mass balance
plt.figure()
plt.hist(allCONV,bins=2)
plt.title('Histogram for Convergence')
plt.savefig(outfilename + 'CONV_hist.pdf')


#plt.show()