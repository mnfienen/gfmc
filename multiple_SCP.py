import os, shutil, re, glob


scenarios = ['LdF_West_future','LdF_LGBK_OTB','LdF_Main_current',
             'LdF_Main_future','LdF_SE_OTB','LdF_Diff_OTB','LdF_West_current']





for cscen in scenarios:
    print 'moving files for %s' %(cscen)
    os.system('scp %s mnfienen@igsarmewfsM000.er.usgs.gov:%s/data/.' %(os.path.join(os.getcwd(),'tmp','*'),cscen))