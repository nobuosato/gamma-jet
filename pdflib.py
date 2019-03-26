#!/usr/bin/env python
import sys,os
import numpy as np
from scipy.interpolate import RectBivariateSpline,interp1d

class PDFLIB:

    def __init__(self,fname,infofile):
 
        #--interpolate pdf grid
        L=open(fname).readlines()
        x=[float(val) for val in L[3].split()]
        Q=[float(val) for val in L[4].split()]
        iflav=[int(val) for val in L[5].split()]
        L=[l.split() for l in L[6:] if '---' not in l]
        data=[[float(val) for val in l] for l in L]
        data=np.transpose(data)
  
        nx=len(x)
        nQ=len(Q)
        nf=len(iflav)
  
        self.T={}
  
        for i in range(nf): 
          table=np.zeros((nx,nQ))
          cnt=-1
          for ix in range(nx):
            for iQ in range(nQ):
              cnt+=1
              table[ix,iQ]=data[i][cnt]
  
          self.T[iflav[i]]=RectBivariateSpline(x,Q,table)

        #--interpolate alphaS grid
        L=open(infofile).readlines()
        Qs=[l for l in L if l.startswith('AlphaS_Qs')][0].split(':')[1]
        Vals=[l for l in L if l.startswith('AlphaS_Vals')][0].split(':')[1]
        Qs=[float(_) for _ in Qs.replace('[','').replace(']','').split(',')]
        Vals=[float(_) for _ in Vals.replace('[','').replace(']','').split(',')]
        self.alphasQ = interp1d(Qs, Vals,kind='cubic')

  
    def xfxQ(self,iflav,x,Q):
        return self.T[iflav](x,Q)[0,0]

if __name__=='__main__':
  
    pdf=PDFLIB('lhagrid/CJ15nlo_0000.dat','lhagrid/CJ15nlo.info')

    print(pdf.xfxQ(21,0.4,10.0))
    print(pdf.alphasQ(10.0))

