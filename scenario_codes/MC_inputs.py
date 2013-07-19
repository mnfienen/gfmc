import numpy as np
import sys 

# ####### #
 # M A I N #
  # ####### #
def MC_PST(real_file,pst_file,MC_root,sel_real):
    
    # read in the random variables file
    invars = open(real_file,'r').readlines()
    tot_real = len(invars)
    if sel_real > tot_real:
        raise(SelectionFail(sel_real,tot_real))
    
    # read in the header and footer information
    pstdat = open(pst_file,'r').readlines()
    header = []
    footer = []
    inpardat = []
    headerflag = True
    parflag = False
    footflag = False
    
    for line in pstdat:
	if '* parameter data' in line:
	    headerflag = False
	    parflag = True
	elif '* observation groups' in line:
	    parflag = False
	    footflag = True
	if headerflag:
	    header.append(line)
	elif parflag:
	    inpardat.append(line)
	elif footflag:
	    footer.append(line)
	      
    # read in the parameter template data --> need to handle fixed and tied parameters!
    head = inpardat.pop(0)
    tied_pars_1 = []
    tied_pars_2 = []
    parnames = []
    partrans = []
    parvals = []
    parfact = []
    pargroups = []
    parscale = []
    paroffset= []
    for line in inpardat:
        tmp = line.strip().split()
        if tmp[0].lower() in tied_pars_1:
            tied_pars_2.append([tmp[0], tmp[1]])
	else:
	    if tmp[1].lower() == 'tied':
		tied_pars_1.append(tmp[0].lower())
	    parnames.append(tmp[0])
	    partrans.append(tmp[1])
	    parfact.append(tmp[2])
	    parvals.append(float(tmp[3]))
	    pargroups.append(tmp[6])
	    parscale.append(tmp[7])
	    paroffset.append(tmp[8])
	    
    # now select the realization data
    realdat = np.array(invars[sel_real].strip().split()).astype(float)
    j=-1
    for i,ctran in enumerate(partrans):
        if ctran.lower() == 'log':
	    j+=1
            parvals[i] = 10**realdat[j]
	elif ctran.lower() == 'none':
	    j+=1
            parvals[i] = realdat[j]
	
    
    # write out the PST file
    ofp = open(MC_root + '%d.pst' %(sel_real) , 'w')
    
    # header first
    for line in header:
        ofp.write(line.strip() + '\n')
        
    # now the parameter section
    ofp.write('* parameter data\n')
    for i,cp in enumerate(parnames):
        ofp.write('%12s %6s %6s %14.8e 1.0e-10 1.0e+10 %s %s %s 1\n' %(cp,
                                                                    partrans[i],
	                                                            parfact[i],
                                                                    parvals[i],
                                                                    pargroups[i],
                                                                    parscale[i],
                                                                    paroffset[i]))
    if len(tied_pars_2) > 0:
	for line in tied_pars_2:
	    for cv in line:
		ofp.write('%s ' %(cv))
	    ofp.write('\n')
    # end with the footer
    for line in footer:
        ofp.write(line.strip() + '\n')
    ofp.close()
    
# ####################### #
# Error Exception Classes #        
# ####################### #
# -- selected a realization out of range
class SelectionFail(Exception):
    def __init__(self,sel_real,tot_real):
        self.sel_real = sel_real
        self.tot_real = tot_real
    def __str__(self):
        return('\n\nSelected realization (%d) out or range of %d total realizations.\n' %(self.sel_real,self.tot_real)) 
