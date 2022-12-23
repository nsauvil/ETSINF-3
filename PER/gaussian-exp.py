#!/usr/bin/python3

import sys
import math
import numpy as np
from gaussian import gaussian

if len(sys.argv)!=6:
  print('Usage: %s <trdata> <trlabels> <ks> <%%trper> <%%dvper>' % sys.argv[0]);
  sys.exit(1);

X= np.load(sys.argv[1])['X'];
xl=np.load(sys.argv[2])['xl'];
ks=np.fromstring(sys.argv[3],dtype=float,sep=' ');
trper=int(sys.argv[4]);
dvper=int(sys.argv[5]);

N=X.shape[0];
np.random.seed(23); perm=np.random.permutation(N);
X=X[perm]; xl=xl[perm];

# Selecting a subset for train and dev sets
Ntr=round(trper/100*N);
Xtr=X[:Ntr]; xltr=xl[:Ntr];
Ndv=round(dvper/100*N);
Xdv=X[N-Ndv:]; xldv=xl[N-Ndv:];


print('Alpha\tError');
print('-------\t----');
for k in ks:
  error = gaussian(Xtr, xltr, Xdv, xldv,k); #error con gaussian
  error = round(error,2);
  print('{}\t{}'.format(k, error));

 


