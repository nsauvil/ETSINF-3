import math
import numpy as np
from scipy import stats
from math import log


def gaussian(Xtr,xltr,Xdv,xldv,alphas):
 
  fil, col = np.shape(Xtr);   #fil (numero de muestras) 
 # edv = np.zeros(len(alphas));
  edv = 0;
  clases = (np.unique(xltr)).astype(int);
  clen = len(clases);
  P_c = np.zeros((clen));  #dimensión  C x 1
 #la media 
  mu = np.zeros((clen,col));  #dimensión C X D
 #matriz covarianzas 
  sigma = np.zeros((clen,col,col));  #dimensión C x D x D
 #suavizado
 # smooth = np.zeros((clen,col));
  smooth = np.zeros((clen,col,col));
#  suma = np.zeros(col); 
     
 
  for c in clases:
      
      elem = np.where(xltr == c)[0] ; #elementos donde la clase es c
      P_c[c] =  np.shape(elem)[0]/fil;
      mu[c] = np.sum(Xtr[elem,:], axis=0)/np.shape(elem)[0];
      suma = np.dot(np.transpose(Xtr[elem,:] - mu[c]),(Xtr[elem,:] - mu[c]));
     # suma = (np.sum(Xtr[elem,:],axis=0) - mu[:,c])*np.transpose(np.sum(Xtr[elem,:], axis=0) - mu[:,c]);
     # sigma[c] = np.sum(suma,axis=0)/np.shape(elem)[0];
      sigma[c] = suma/np.shape(elem)[0];
     

  f,c = np.shape(Xdv);
  maximo =  np.zeros((clen, f));   
  
  for c in clases:
    smooth[c]  = alphas * sigma[c]  + (1-alphas) * np.identity(col);
   
    maximo[c]  = pxc(P_c[c], mu[c], smooth[c] , Xdv);
    
  clases = np.argmax(maximo, axis=0);  #con axis=1 no funciona 
    #Calcular error clasificación
  edv = np.mean(xldv!=clases)*100;
  return edv;

def logdet(X,col):
 # res = 0;
#  i = 0;
 # j = 0;
 # while i < col:
   # res = res + np.log(X[i,j]);
  #  i = i+1;
  #  j = j+1;
  res = 0;
  vals = np.real(np.linalg.eigvals(X));
  for v in vals:
    if v == 0:
      res = sys.float_info.min;
    res += log(v,10);
  

  return res;

def pxc(P_c, mu,sigma, Xdv):
  op1 =0;
  op2 =0;
  op3 =0;
  f,c = np.shape(Xdv);
  res = np.zeros(f);
  col,col2 = np.shape(sigma);
  op1 = -(1/2)*np.linalg.pinv(sigma); #wC 
  op2 = np.linalg.pinv(sigma) @ np.transpose(mu); #wc 
  op3 = np.log(P_c) - (1/2)*logdet(sigma,col) - ((1/2)*mu) @ np.linalg.pinv(sigma) @ np.transpose(mu); #wc0 
  for i in range(f):
    res[i] = Xdv[i] @ op1 @ np.transpose(Xdv[i]);
  res = res + np.dot(Xdv, op2) + op3 ;      
  #  maximo[:,c]  = (Xdv) * op1*Xdv  + np.transpose(op2)*Xdv  + op3;
  return res;

  
