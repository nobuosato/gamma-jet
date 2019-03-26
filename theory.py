#!/usr/bin/env python
import sys,os
import numpy as np
import pandas as pd
import copy

from scipy import interpolate

#--lhapdf
#import lhapdf
#pdf=lhapdf.mkPDF("CJ15nlo", 0)

#--pdflib
from pdflib import PDFLIB
pdf=PDFLIB('lhagrid/CJ15nlo_0000.dat','lhagrid/CJ15nlo.info')


def get_xsec(y3,y4,pT,rS,muR,muF,q=1,g=1):
    xT=2.*pT/rS
    x1=0.5*xT*(np.exp( y3)+np.exp( y4))     
    x2=0.5*xT*(np.exp(-y3)+np.exp(-y4))     
    s=x1*x2*rS**2
    t=-x1*rS*pT*np.exp(-y3)
    u=-x2*rS*pT*np.exp(+y3)

    M2qqb =  8./9.*(t**2+u**2+2*s*(s+t+u))/t/u     
    M2gq  = -1./9.*(s**2+u**2+2*t*(s+t+u))/s/u

    eU=4./9.
    eD=4./9.

    gA=pdf.xfxQ(21,x1,muF)/x1
    gB=pdf.xfxQ(21,x2,muF)/x2

    dA=pdf.xfxQ( 1,x1,muF)/x1
    uA=pdf.xfxQ( 2,x1,muF)/x1
    sA=pdf.xfxQ( 3,x1,muF)/x1
    cA=pdf.xfxQ( 4,x1,muF)/x1
    bA=pdf.xfxQ( 5,x1,muF)/x1

    dbA=pdf.xfxQ(-1,x1,muF)/x1
    ubA=pdf.xfxQ(-2,x1,muF)/x1
    sbA=pdf.xfxQ(-3,x1,muF)/x1
    cbA=pdf.xfxQ(-4,x1,muF)/x1
    bbA=pdf.xfxQ(-5,x1,muF)/x1

    dB=pdf.xfxQ( 1,x2,muF)/x2
    uB=pdf.xfxQ( 2,x2,muF)/x2
    sB=pdf.xfxQ( 3,x2,muF)/x2
    cB=pdf.xfxQ( 4,x2,muF)/x2
    bB=pdf.xfxQ( 5,x2,muF)/x2

    dbB=pdf.xfxQ(-1,x2,muF)/x2
    ubB=pdf.xfxQ(-2,x2,muF)/x2
    sbB=pdf.xfxQ(-3,x2,muF)/x2
    cbB=pdf.xfxQ(-4,x2,muF)/x2
    bbB=pdf.xfxQ(-5,x2,muF)/x2
    
    Lqqb =  eU*(uA*ubB+cA*cbB) + eD*(dA*dbB+sA*sbB+bA*bbB)\
           +eU*(ubA*uB+cbA*cB) + eD*(dbA*dB+sbA*sB+bbA*bB)

    Lgq   = gA*(eU*(uB+cB)+eD*(dB+sB+bB)+eU*(ubB+cbB)+eD*(dbB+sbB+bbB))\
           +gB*(eU*(uA+cA)+eD*(dA+sA+bA)+eU*(ubA+cbA)+eD*(dbA+sbA+bbA))

    alfa=1/137.
    eq2=alfa*4*np.pi
    gs2=pdf.alphasQ(muR)*4*np.pi
  
    xsec=1.0/(16*np.pi*rS**2)/x1/x2  #--overall factor
    xsec*=eq2*gs2                    #--couplings
    xsec*=Lqqb*M2qqb*q + Lgq*M2gq*g  #--parton lum times hard
    return xsec



if __name__=='__main__':

    y3=0
    y4=0
    pT=100.0
    rS=5000.0
    muR=pT
    muF=pT
    print(get_xsec(y3,y4,pT,rS,muR,muF))






