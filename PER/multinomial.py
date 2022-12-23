import math
import numpy as np
from scipy import stats
from math import log


# Computes the multinomial error rate
# of the test set Xdv with respect to training set Xtr
# Xtr  is a n x d training data matrix 
# xltr is a n x 1 training label vector 
# Xdv is a m x d test data matrix
# xldv is a m x 1 test label vector 
# epsilons is the epsilons vector (para realizar suavizado)
def multinomial(Xtr,xltr,Xdv,xldv,epsilons):

  fil, col = np.shape(Xtr);
  
  edv = 0;
  
  clases = (np.unique(xltr)).astype(int);
  clen = len(clases);
  P_c = np.zeros((clen));  #dimensión  C x 1
  
  Pc = np.zeros((clen,col));  #dimensión C x D 
 #suavizado
 #smooth = np.zeros((clen,col));
  smooth = [];
 
  for c in clases:
      elem = np.where(xltr == c); #elementos donde la clase es c
      P_c[c] =  len(elem)/len(xltr);  #P_c = Nc/N
      Pc[c] = np.sum(Xtr[elem], axis=0)/np.sum(Xtr[elem]);
    #suma_c  = np.sum(Xtr[elem,:], axis=1);  #sumar la fila
    #suma_c = np.sum(suma_c, axis=0);
    #suma_c2 = np.sum(suma_c, axis=0);  #suma de los valores de todas las dimensiones de los objetos tipo c
    #suma_c2 = np.sum(Xtr[elem,:], axis=1);
       
  #SUAVIZAR CON LAPLACE
  
  smooth = (Pc + epsilons) / (1 + epsilons*col); #Pc + epsilon / (1+epsilon*Dimension) 
  #Clasificar el conjunto Xdv
   
  maximo = Xdv@np.transpose(np.log(smooth)) + np.log(P_c);
  clases = np.argmax(maximo, axis=1);
  #Calcular error clasificación
  edv = np.mean(xldv!=clases)*100;
  
      

  return edv;
