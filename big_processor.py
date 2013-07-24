import os, shutil, re, glob



def prep_and_delete(scenarios):
    for cscen in scenarios:
	    localdir = re.sub('LdF_','',cscen)
	    cpath = os.path.join(os.getcwd(),localdir)
	    if not os.path.exists(os.path.join(cpath,'results')):
			os.mkdir(os.path.join(cpath,'results'))
	    files = glob.glob(os.path.join(cpath,'results','*'))
	    print 'removing all contents of %s ' %(os.path.join(cpath,'results'))
	    for f in files:
		os.remove(f)
	    print 'Verifying that the files were removed'
	    cf = os.listdir(os.path.join(cpath,'results'))
	    if len(cf)==0:
		print 'All files removed from %s ' %(os.path.join(cpath,'results'))
	    else:
		print 'Not all files removed'
		for line in cf:
		    print '%s --> remains' %(line)    


parfile = 'big_processor.par'

inputfiles = []
scenarios = []
for line in open(parfile,'r').readlines():
    scenarios.append(line.strip().split()[0])
    inputfiles.append(line.strip().split()[1:])


prep_delete = True
pull_files = True
parse_and_proc = True
cover_tracks = True

# first remove the contents of all the scenario results files
if prep_delete:
    prep_and_delete(scenarios)

# now pull down the files from M000
for i,cscen in enumerate(scenarios):
    if pull_files:
        localdir = re.sub('LdF_','',cscen)
        cpath = os.path.join(os.getcwd(),localdir)
        print 'retrieving files from %s' %(cscen)
        os.system('scp mnfienen@igsarmewfsM000.er.usgs.gov:MONTE_CARLO_MENOM/%s/results/* %s' %(cscen,os.path.join(cpath,'results')))
# now run the processing 
    if parse_and_proc:
	homedir = os.getcwd()
	localdir = re.sub('LdF_','',cscen)
	cpath = os.path.join(os.getcwd(),localdir)
	shutil.copyfile(os.path.join(os.getcwd(),'parse_results.py'),os.path.join(cpath,'parse_results.py'))
	shutil.copyfile(os.path.join(os.getcwd(),'process_results.py'),os.path.join(cpath,'process_results.py'))
	os.chdir(cpath)
	for cinputfile in inputfiles[i]:
	    print'\nRunning %s with input file --> %s' %(cscen,cinputfile)
	    os.system('python parse_results.py %s' %(cinputfile))
	    os.system('python process_results.py %s'  %(cinputfile))
	os.chdir(homedir)
	
    if cover_tracks:
	prep_and_delete([cscen])