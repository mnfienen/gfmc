import os, shutil, re, glob

# troll through all the data files below and parse all the name files

def readnamefile(namfile):
    # set input variables here
    tmp = open(namfile,'r').readlines()
    
    indat = []
    varnames = []
    values = []
    for line in tmp:
	if line.lstrip()[0] != '#':
	    cline = line.split('#')[0].split('=')
	    varnames.append(cline[0].strip())
	    values.append(cline[1].strip())
    namdata = dict(zip(varnames,values))
    return namdata


# #### #
# MAIN #
# #### #
scenarios_file = 'scenarios_names.dat'
outfile = 'big_processor.par'

ofp = open(outfile,'w')
scenarios = []
# read in the scenario names
for line in open(scenarios_file,'r').readlines():
    scenarios.append(line.strip())
    
    
for cscen in scenarios:
    ofp.write('%s ' %(cscen))
    cpath = os.path.join(os.getcwd(),cscen)
    namfiles = glob.glob(os.path.join(cpath,'data','*nam'))
    for cnam in namfiles:
	namdata = readnamefile(cnam)
	if int(namdata['method']) == 2:
	    cinfile = '%selement.in' %(namdata['eleoutfilename'][:-4])
	    ofp.write('%s ' %(cinfile))
	    ofpinfile = open(os.path.join(cpath,cinfile),'w')
	    ofpinfile.write('%s #plumefile\n' %(namdata['eleoutfilename']))
	    ofpinfile.write('PHI_records.dat     # PHI file\n' )
	    ifpinfile.write("e                  # 'p' for point file, 'e' for element file\n")
	    ofpinfile.close()
	elif int(namdata['method']) == 3:
	    cinfile = '%sgrid.in' %(namdata['gridoutfilename'][:-4])
	    ofp.write('%s ' %(cinfile))
	    ofpinfile = open(os.path.join(cpath,cinfile),'w')
	    ofpinfile.write('%s #plumefile\n' %(namdata['gridoutfilename']))
	    ofpinfile.write('PHI_records.dat     # PHI file\n' )
	    ofpinfile.write("p                  # 'p' for point file, 'e' for element file\n")
	    ofpinfile.close()	    
	elif int(namdata['method']) == 4:
	    cinfile = '%sgrid.in' %(namdata['gridoutfilename'][:-4])
	    ofp.write('%s ' %(cinfile))
	    ofpinfile = open(os.path.join(cpath,cinfile),'w')
	    ofpinfile.write('%s #plumefile\n' %(namdata['gridoutfilename']))
	    ofpinfile.write('PHI_records.dat     # PHI file\n' )
	    ofpinfile.write("p                  # 'p' for point file, 'e' for element file\n")
	    ofpinfile.close()	    
	    cinfile = '%selement.in' %(namdata['eleoutfilename'][:-4])
	    ofp.write('%s ' %(cinfile))
	    ofpinfile = open(os.path.join(cpath,cinfile),'w')
	    ofpinfile.write('%s #plumefile\n' %(namdata['eleoutfilename']))
	    ofpinfile.write('PHI_records.dat     # PHI file\n' )
	    ofpinfile.write("e                  # 'p' for point file, 'e' for element file\n")
	    ofpinfile.close()	  
	elif int(namdata['method']) == 1:
	    cinfile = '%s.in' %(namdata['AcrOutFileName'][:-4])
	    ofp.write('%s ' %(cinfile))
	    ofpinfile = open(os.path.join(cpath,cinfile),'w')
	    ofpinfile.write('%s #plumefile\n' %(namdata['AcrOutFileName']))
	    ofpinfile.write('PHI_records.dat     # PHI file\n' )
	    ofpinfile.write("p                  # 'p' for point file, 'e' for element file\n")
	    ofpinfile.close()	    
		
	
    ofp.write('\n')
ofp.close()
