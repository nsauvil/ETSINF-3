#!/usr/bin/python3


import sys
import math
import numpy as np
from pca import pca
from knn import knn
from multinomial import multinomial

if len(sys.argv)!=6:
  print('Usage: %s <trdata> <trlabels> <tedata> <telabels> <k>' % sys.argv[0]);
  sys.exit(1);

X= np.load(sys.argv[1])['X'];
xl=np.load(sys.argv[2])['xl'];
Y= np.load(sys.argv[3])['Y'];
yl=np.load(sys.argv[4])['yl'];
k=float(sys.argv[5]);


print('Epsilon\tEdv');
print('-------\t----');


error = multinomial(X, xl, Y, yl,k); #error con multinomial 
#mostrar resultados:   
error = round(error,2);
print('{}\t{}'.format(k, error));


