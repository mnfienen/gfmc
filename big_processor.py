import os, shutil, re, glob


#scenarios = ['LdF_West_future','LdF_LGBK_OTB','LdF_Main_current',
#             'LdF_Main_future','LdF_SE_OTB','LdF_Diff_OTB','LdF_West_current']

scenarios = ['LdF_LGBK_OTB']


prep_delete = False
pull_files = False
parse_and_proc = True

# first remove the contents of all the scenario results files
if prep_delete:
    for cscen in scenarios:
        localdir = re.sub('LdF_','',cscen)
        cpath = os.path.join(os.getcwd(),localdir)
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

# now pull down the files from M000
if pull_files:
    for cscen in scenarios:
        localdir = re.sub('LdF_','',cscen)
        cpath = os.path.join(os.getcwd(),localdir)
        print 'retrieving files from %s' %(cscen)
        os.system('scp mnfienen@igsarmewfsM000.er.usgs.gov:%s/results/* %s' %(cscen,os.path.join(cpath,'results')))
# now run the processing 
if parse_and_proc:
    for cscen in scenarios:
        localdir = re.sub('LdF_','',cscen)
        cpath = os.path.join(os.getcwd(),localdir)
        shutil.copyfile(os.path.join(os.getcwd(),'parse_results.py'),os.path.join(cpath,'parse_results.py'))
        shutil.copyfile(os.path.join(os.getcwd(),'process_results.py'),os.path.join(cpath,'process_results.py'))
        os.chdir(cpath)
        print'\nRunning %s' %(cscen)
        os.system('python parse_results.py')
        os.system('python process_results.py')