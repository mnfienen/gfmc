# Expanded upon "GFLOW_bkptl.py" so that now it will either match particles
# to a polygon, as per the original code, or to a specified element (LS, or well)
#
# Determines whether a particle ends at a location of interest.
# To be used for mapping probablility of a
# particle entering an area given numerous runs of a GFLOW simulation

import sys
import numpy as np
import time
from In_n_out import eval_point_in_poly

echo = False
dat_echo = False
t_start = time.time()
# ####################### #
# Error Exception Classes #        
# ####################### #
# -- cannot read/write/open/close file
class FileFail(Exception):
    def __init__(self,filename,filetype):
        self.filename=filename
        self.ft = filetype
    def __str__(self):
        return('\n\nProblem with ' + self.ft +': ' + self.filename + ' \n' +
            "Either it can't be opened or closed, can't be read from or written to, or doesn't exist") 
    
# -- wrong number of lines in cal file
class CalFail(Exception):
    def __init__(self,nlines,fn):
        self.nlines=nlines
        self.fn = fn
    def __str__(self):
        return('\n\nCal File: ' + self.fn + ' has wrong number of lines. \n' +
               'Read ' + str(self.nlines) + ' lines in the file')

# -- Failure parsing the input data file
class ParseFail(Exception):
    def __init__(self,offending_line):
        self.offending_line = offending_line
    def __str__(self):
        return('\n\nThere was a problem parsing a line in your data file. \n' +
               'The offending line was:\n' +
               '"' + self.offending_line + '"')

# start of code; read in the namefile from the command prompt.
# the namefile points to the files with input data.
try:
    namfile = sys.argv[1]
    lines = open(namfile,'r').readlines()
    method = lines[2].strip().split()[0]
    outfilename = lines[3].strip().split()[0]
    ptlfilename = lines[4].strip().split()[0].upper()
    datfilename = lines[5].strip().split()[0]
    if method.lower() == 'element':
        elementfile = lines[6].strip().split()[0]
    else:
        sourcefilename = lines[6].strip().split()[0]
        dtol = float(lines[7].strip().split()[0])
  
except:
    raise(FileFail(namfile,'name (*.nam) file'))

# open output file 
try:
    output_file = open(outfilename,'w')
except:
    raise(FileFail(outfilename,'output file'))


# ###########################
# GFLOW dat file info block #
# ###########################
DATA = []
# open the dat file
try:
    dat_file = open(datfilename,'r').readlines()
except:
    raise(FileFail(datfilename,'dat file'))

for each_line in dat_file:
    DATA = each_line.split()  # splits a string at whitespaces    
    DATA = DATA[:] + [1]
    if DATA[0] == 'modelorigin': # Origin coordinates are in meters, all else in feet
        X_ORIG = float(DATA[1])
        Y_ORIG = float(DATA[2])
        break
    
if method.lower() == 'element':  # if an element is listed, evaluate by that element name    
# ###########################
# Element file info block   #
# ###########################
    element = []
    # open the dat file
    try:
        ele_file = open(elementfile,'r').readlines()
    except:
        raise(FileFail(elementfile,'element file'))
    
    for ele_line in ele_file:
        element.append(ele_line.strip('\n'))    # need to strip the \n off of the matchelement

    
# ##########################
# Pathline file info block #
# ##########################
DATA= []
STATUS = []
Ps = []
Pe = []
PCOORDstr = []   
PCOORDend = []   
PATHLINE = 0
Pelement = []
# open particle path file 
try:
    ptl_file = open(ptlfilename,'r')
except:
    raise(FileFail(ptlfilename,'particle file'))

for each_line in ptl_file:
    DATA = each_line.split()  # splits a string at whitespaces
    STATUS = DATA[0]  #starting point, intermediate point, or ending point
    if STATUS == 'START':
        Xstart = ((float(DATA[1]) / 3.28083) + X_ORIG)   # convert particle coordinates from feet to meter and add origin offset       
        Ystart = ((float(DATA[2]) / 3.28083) + Y_ORIG) 
        Ps.append(Xstart)
        Ps.append(Ystart)
        PCOORDstr.append(np.array([Ps[0],Ps[1]]))
        Ps = []  
    elif STATUS == 'END':
        Xend = ((float(DATA[1]) / 3.28083) + X_ORIG)   # convert particle coordinates from feet to meter and add origin offset 
        Yend = ((float(DATA[2]) / 3.28083) + Y_ORIG)    
        Pe.append(Xend)
        Pe.append(Yend)
        PCOORDend.append(np.array([Pe[0],Pe[1]]))
        Pe = [] 
        Pelement.append(DATA[8])
    else:
        ()
PCOORDstr = np.array(PCOORDstr)
PCOORDend = np.array(PCOORDend)

# ##############################################
# Check if end point is in polygon of interest #
# ##############################################
Endpt_outstring = '  X   ' + '   Y   ' + '    In/Out    ' + '\n' 
output_file.write(Endpt_outstring)    # write to the output files 


if method == 'element':  # if an element is listed, evaluate by that element name
    Z = []
    Z = np.zeros(len(PCOORDstr))
    
    for I, test_pt in enumerate (PCOORDend[:]):    
        for matchelement in element:
            if matchelement == Pelement[I]:  
                Z[I] += 1     
            
    for i, coord in enumerate (PCOORDstr[:]):
        X = coord[0]
        Y = coord[1]    
        Endpt_outstring = str(X) + ', ' + str(Y) + ', ' + str(Z[i]) + '\n' 
        output_file.write(Endpt_outstring)             

        
# if an element isn't listed, perform evaluation based on polygon
elif method == 'polygon':    
    Z = []
    infile_root = sourcefilename.strip('.csv')
    verts_file = infile_root + '.dat'
    points_file = infile_root + '.csv'
    Z = np.zeros(len(PCOORDstr))
    
    verts = np.loadtxt(verts_file).astype(int)
    points = np.loadtxt(points_file,delimiter=',',skiprows=1)
    
    for I, test_pt in enumerate (PCOORDend[:]):    
        inout = eval_point_in_poly(verts,points,test_pt,dtol)
        if inout:
            Z[I] += 1     

    for i, coord in enumerate (PCOORDstr[:]):
        X = coord[0]
        Y = coord[1]    
        Endpt_outstring = str(X) + ', ' + str(Y) + ', ' + str(Z[i]) + '\n' 
        output_file.write(Endpt_outstring)    # write to the output files               

        
else:
    print 'There is a problem with the specified "capture" method. \n'
    print 'At the top of the Name file, please specifiy "element" if particle \n'
    print 'capture will be evaluated relative to a specific AE element \n'
    print '(a well or linesink), and then specify the file containing the list \n'
    print 'of elements.  Please specify "polygon" if particle capture will \n'
    print 'be evaluated relative to a specific polygon shape.'
        
# close output file    
try:
    output_file.close()
except:
    raise(FileFail(outfilename,'output file'))

#get the elapsed time in seconds
t_end = time.time()-t_start

print 'took %f seconds to run this puppy' %(t_end)