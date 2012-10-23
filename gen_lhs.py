'''gen_lhs generates random variables using the corrleation
matrix from either UCODE or MODFLOW-2000.  The distribution of each 
parameter is divided into "Number of quantiles" regions of equal
probability. Each of those regions is sampled "Number of repetitions"
times.  The correlation structure is preserved by mimicing the rank
correlation matrix (Iman, R.L. and Connover, W.J., 1982, A distribution 
free approach to inducing rank correlation among input variables: 
Communications in Statistics--Simulation and Computation, v. 11, n. 3, 
p. 311-334)'''
import numpy as np
from numpy import random
from numpy import linalg
from scipy import stats

test=False
if test:
    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # Example data from Iman and Connover, 1982.  
    # Read external matrix R.txt
    success=True
    NumQuan=15
    NumRep=1
    NVar=6
    Cstar=np.identity(NVar)
    Cstar[3,4]=.75
    Cstar[3,5]=-.7
    Cstar[4,3]=.75
    Cstar[4,5]=-.95
    Cstar[5,3]=-.7
    Cstar[5,4]=-.95
    R=np.loadtxt('R.txt')
    OptPar=np.zeros((NVar))
    StDev=np.ones((NVar))
    fname='I_and_C_test'
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Routine to read optimal parameters and log transform as necessary
# You get three tries for each item of input to do it right
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
if not test:
    for tri in range(3):
        success=True
        model=raw_input('Model File Type: MF2K, UCode, or PEST?  ')
        model=model.upper()
        if model=="UCODE":
            TranCol=4
            OptCol=1
            SkipRow=1           
        elif model=="MF2K":
            TranCol=1
            OptCol=2
            SkipRow=0
        elif model=="PEST":
            TranCol=0
            OptCol=1
            SkipRow=0
        else:
            print 'You entered an invalid Model File Type.  Please try again.'
            success=False
        if success:break
    if success:
        for tri in range(3):
            success=True
            fname=raw_input('Root name?  ')
            OptName=fname+"._pc"
            try:
                Trans,OptPar=np.loadtxt(OptName,skiprows=SkipRow,usecols=(TranCol,OptCol),unpack=True)
                McName=fname+"._mc"
                MvName=fname+"._mv"
                Cstar=np.loadtxt(McName,skiprows=1)
                Mv=np.loadtxt(MvName,skiprows=1)
                StDev=np.sqrt(np.diagonal(Mv))
                NVar=Mv.shape[0]
                OptPar[Trans==1]=np.log10(OptPar[Trans==1])
            except (NameError,IOError):
                print 'You entered the name of an invalid Root name file or'
                print '_pc, _mc, or _mv is invalid.  Please try again.'
                success=False
            if success:break
    if success:
        for tri in range(3):
            success=True
            try:
                NumQuan=raw_input('Number of quantiles?  ')
                NumQuan=int(NumQuan)
                NumRep=raw_input('Number of repetitions?  ')
                NumRep=int(NumRep)
            except ValueError:
                print 'Please enter an integer'
                success=False
            if success:break
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Try to modify a matrix that is "almost" positive definite such
# that it is. This is useful mainly if the user creates a matrix 
# manually that turns out not to be positive definite.
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def CholDecomp(amatrix):
    # Routine from "An iterative algorithm to produce
    # a positive definite correlation matrix from an
    # approximate correlation matrix" Iman and 
    # Davenport, 1982 (Sandia report SAND81-1376)
    EigVal=(linalg.eig(amatrix)[0])
    EigVec=(linalg.eig(amatrix)[1])
    epsilon=np.array(EigVal<=0,dtype='i')*0.001
    if np.sum(epsilon)>0:
        for i in range(10):
            EigVal=EigVal+epsilon
            EigValMat=np.diag(EigVal)
            amatrix=np.dot(EigVec,EigValMat)
            amatrix=np.dot(amatrix,transpose(EigVec))
            EigVal=(linalg.eig(amatrix)[0])
            EigVec=(linalg.eig(amatrix)[1])
            epsilon=np.array(EigVal<=0,dtype='i')*0.001
            if np.sum(epsilon)==0:break
    decompmatrix=linalg.cholesky(amatrix)
    #need to scale decompmatrix so that diagonals equal 1
    #simply setting them to one is preferred--see Method A in 
    #Iman and Davenport
    step=NVar+1
    decompmatrix.flat[::step]=1.0
    return decompmatrix

if success:
    outfile=fname+".ranvar"
    RVFinal=np.zeros((NumQuan*NumRep,NVar))
    m=np.arange(1.,NumQuan+1.)
    temp=m/(NumQuan+1.)
    vdWscores=stats.norm.ppf(temp,0,1)
    try:
        P=linalg.cholesky(Cstar)
    except LinAlgError:
        print 'Correlation matrix is not positive definite. Will try to correct it.'
        P=CholDecomp(Cstar)
    Pt=np.transpose(P)
    for Rep in range(NumRep):
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # Generate uncorrelated RandomVariables and uncorrelated 
        # randomized van der Waerden scores (R)
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        RandonVariables=np.zeros((NumQuan,NVar))
        R=np.zeros((NumQuan,NVar))
        for i in range(NVar):
            Um=random.uniform(size=NumQuan)
            Pm=Um*(1./NumQuan)+(m-1)/NumQuan
            RandonVariables[:,i]=stats.norm.ppf(Pm,OptPar[i],StDev[i])
            random.shuffle(vdWscores)
            R[:,i]=vdWscores
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # Routine to induce rank correlation
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        if test:
            R=np.loadtxt('R.txt')
            RandomVariable=R
        T=np.corrcoef(R,rowvar=0)    
        Q=linalg.cholesky(T)
        Qinv=linalg.inv(Q)
        S=np.dot(P,Qinv)
        St=np.transpose(S)
        RBstar=np.dot(R,St)
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # Sort RandomVariables by ranks of RBstar to have 
        # the proper correlation and add to final matrix
        #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        RBstarrank=np.argsort(np.argsort(RBstar,axis=0),axis=0)
        mesh=np.meshgrid(np.arange(NVar),np.arange(NumQuan))
        column=mesh[0]
        strow=Rep*NumQuan
        enrow=strow+NumQuan
        RVFinal[strow:enrow,:]=RandonVariables[RBstarrank,column]
    np.savetxt(outfile,RVFinal)
    print "Done with", Rep+1, "repetitions of", NVar, "variables"    
    maxdiff=np.amax(np.corrcoef(RVFinal,rowvar=0)-Cstar)
    print "Maximum element-wise difference between input and output correlation matrices:", maxdiff
else:
    print "You entered something that was invalid.  Please check you input and start again."
