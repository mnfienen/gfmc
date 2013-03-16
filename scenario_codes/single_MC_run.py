import numpy, sys
from getPHI import getPHI
from getMB import getMB, convergence_critera
from MC_inputs import MC_PST, SelectionFail
import os
import datetime as dt


# get the current realization number from the command line (argv)
sel_real = int(sys.argv[1])
namfile = sys.argv[2]

# set input variables here
tmp = open(namfile,'r').readlines()

indat = []
for line in tmp:
	if line.lstrip()[0] != '#':
		indat.append(line)

real_file = indat[1].strip().split('#')[0].split('=')[1].strip()     # name of the file containing all the realizations
pst_file = indat[2].strip().split('#')[0].split('=')[1].strip()    # base PST control file
MC_root = 'MC_'                 # root name for the output PST files

#
# # make the MC PST file
#
MC_PST(real_file,pst_file,MC_root,sel_real)
# ###########
print "made input files............"
#
# # run PEST
#
sttime = dt.datetime.now()
print 'running PEST............'
os.system('pest ' + MC_root + '%d' %(sel_real))
endtime = dt.datetime.now()
#
# # rip PHI
#
PHI = getPHI(MC_root,sel_real)
print 'PHI = %f' %(PHI)

#
# # rip mass balance
#
conv_crit_names = ['linesinks with_resistance','lake waterbalance ']
conv_crits = []
for cn in conv_crit_names:
    conv_crits.append(convergence_critera(cn))
    
MB, conv_crits = getMB(conv_crits,True)
# MB == True indicates that all mass balance values were acceptable
# NB conv_crits is returned for completeness but not necessarily used now

ofp = open('MC_%d.mcres' %(sel_real),'w')
ofp.write('PHI,Forward Converged\n')
ofp.write('%f,%s\n' %(PHI,MB))
ofp.write('time--> %s\n' %(endtime-sttime))
ofp.close()

print 'time--> %s\n' %(endtime-sttime)
