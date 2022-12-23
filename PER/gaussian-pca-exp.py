#!/usr/bin/python3

import sys
import math
import numpy as np
from pca import pca
from gaussian import gaussian

if len(sys.argv)!=7:
  print('Usage: %s <trdata> <trlabels> <ks> <ds> <%%trper> <%%dvper>' % sys.argv[0]);
  sys.exit(1);

X= np.load(sys.argv[1])['X'];
xl=np.load(sys.argv[2])['xl'];
ks=np.fromstring(sys.argv[3],dtype=float,sep=' ');
ds=np.fromstring(sys.argv[4],dtype=int,sep=' ');
trper=int(sys.argv[5]);
dvper=int(sys.argv[6]);

N=X.shape[0];
np.random.seed(23); perm=np.random.permutation(N);
X=X[perm]; xl=xl[perm];

# Selecting a subset for train and dev sets
Ntr=round(trper/100*N);
Xtr=X[:Ntr]; xltr=xl[:Ntr];
Ndv=round(dvper/100*N);
Xdv=X[N-Ndv:]; xldv=xl[N-Ndv:];

#1. Calcular pca con xtr
[m,Mvect] = pca(Xtr);

print('Dimension\tAlpha\tError');
print('-----------\t-------\t----');

for d in ds:
  for k in ks:
    #2.1 proyectar los datos de xtr a ks dimensiones
    Xtr_p = (Xtr - m).dot(Mvect[:,1:d]);
    #2.2 proyectar los datos de xdr a ks dimensiones
    Xdv_p = (Xdv - m).dot(Mvect[:,1:d]);
    #2.3 medir error con la funcion gauss
    error = gaussian(Xtr_p, xltr, Xdv_p, xldv,k); #error con gaussian
    error = round(error,2);
    print('{}\t\t{}\t{}'.format(d,k, error));
  



 


