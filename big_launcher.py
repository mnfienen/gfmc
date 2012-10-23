import os, re, shutil,glob

nruns = 1
chome = os.getcwd()

scenarios = ['LdF_West_future','LdF_LGBK_OTB','LdF_Main_current',
             'LdF_Main_future','LdF_SE_OTB','LdF_Diff_OTB','LdF_West_current']

for cscen in scenarios:
    # kill the log and results files and the data.tar file
    print "cleaning up for %s" %(cscen)
    cpath = os.path.join(os.getcwd(),cscen)
    if os.path.exists(os.path.join(cpath,'data.tar')):
        os.remove(os.path.join(cpath,'data.tar'))
    files = glob.glob(os.path.join(cpath,'results','*'))
    for cf in files:
        os.remove(cf)
    files = glob.glob(os.path.join(cpath,'log','*'))
    for cf in files:
        os.remove(cf)
    print 'making data.tar'
    os.chdir(cpath)
    os.system('tar czf data.tar data')
    print 'fixing the sub file'
    indat = open('ldf_mc.sub','r').readlines()
    ofp = open('ldf_mc.sub','w')
    for line in indat:
        if 'queue' not in line:
            ofp.write(line)
        else:
            ofp.write('queue %d\n' %(nruns))
    ofp.close()
    print 'submitting the file'
    os.system('condor_submit ldf_mc.sub')
    os.chdir(chome)