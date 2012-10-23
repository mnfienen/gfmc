import os, re, shutil,glob

nruns = 1
chome = os.getcwd()

scenarios = ['LdF_West_future','LdF_LGBK_OTB','LdF_Main_current',
             'LdF_Main_future','LdF_SE_OTB','LdF_Diff_OTB','LdF_West_current']

for cscen in scenarios:
    # kill the log and results files and the data.tar file
    print "cleaning up for %s" %(cscen)
    cpath = os.path.join(os.getcwd(),cscen,'data')
    files = glob.glob(os.path.join(cpath,'*'))
    for cf in files:
        if 'footer_pst' in cf:
            print 'removing %s' %(cf)
            os.remove(cf)
        elif 'header_pst' in cf:
            print 'removing %s' %(cf)
            os.remove(cf)
        elif 'par_data' in cf:
            print 'removing %s' %(cf)
            os.remove(cf)
            
    