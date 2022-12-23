#!/usr/bin/python3


import sys
import math
import numpy as np
from pca import pca
from knn import knn
from gaussian import gaussian

if len(sys.argv)!=7:
  print('Usage: %s <trdata> <trlabels> <tedata> <telabels> <k> <d>' % sys.argv[0]);
  sys.exit(1);

X= np.load(sys.argv[1])['X'];
xl=np.load(sys.argv[2])['xl'];
Y= np.load(sys.argv[3])['Y'];
yl=np.load(sys.argv[4])['yl'];
k=float(sys.argv[5]);
d=int(sys.argv[6]);


print('Dimension\tAlpha\tError');
print('-----------\t-------\t----');

#1. Calcular pca con X
[m,Mvect] = pca(X);
#2.1 proyectar los datos de xtr a ks dimensiones
Xtr_p = (X - m).dot(Mvect[:,1:d]);
#2.2 proyectar los datos de xdr a ks dimensiones
Xdv_p = (Y - m).dot(Mvect[:,1:d]);

error = gaussian(Xtr_p, xl, Xdv_p, yl,k); #error con gauss
#2.4 mostrar resultados:   
error = round(error,2);
print('{}\t\t{}\t{}'.format(d,k, error));


