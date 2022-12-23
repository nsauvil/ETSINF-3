#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys
import pathlib



########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################



def sort_index(d):
    for k in d:
       # l = sorted(((y, x) for x, y in d[k][1] ), reverse=True)
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]')  #para dividir en frases 
        self.r2 = re.compile('\W+')    #para eliminar símbolos no alfanuméricos 


    def index_sentence(self, sentence, tri):
        #############
        # COMPLETAR #
        #############
        dic = self.index['bi']
       # for i in range(len(sentence)):
           # sentence[i] = sentence[i].lower()
        sentence = sentence.lower()
        frase = sentence.split()    
            
        act=''#frase(i) 
        
        count = 0 #contador de la tupla 
       # print(frase, 'frase')

        for i in range(0, len(frase)-1):
            act = frase[i]
            if act in dic:   #la palabra ya está en el dic 
                count = dic[act][0] + 1 #contador del act, guardarlo para añadirlo tras recorrer los consecuentes
                sig = dic[act][1] #lista con las palabras que van después de act
                for el in sig:   
                    añadir = True
                    if frase[i+1] == el[1]: #si una de las tuplas es el consecuente, aumentar contador
                        nuevocont = el[0] + 1
                        j = sig.index(el) #posición en la que se encuentra el
                       #insertar el consecuente modificado 
                        sig = sig[:j] + [(nuevocont, el[1])] + sig[j+1:]  
                        añadir = False
                        break
                if añadir: #si el act i+1 no está tras act, añadirlo 
                    sig = sig + [(1, frase[i+1])] 
               #juntar todo en el dic
                dic[act] = (count, sig)  
            else:
                dic[act] = (1, [(1,frase[i+1])])  #si es comienzo de frase, añadirlo al dic y poner la palabra siguiente
        if tri:
            for i in range(0, len(frase) - 2):
                tupla = (frase[i], frase[i+1])
                self.index['tri'][tupla] = self.index['tri'].get(tupla, {})
                self.index['tri'][tupla][frase[i+2]] = self.index['tri'][tupla].get(frase[i+2], 0) + 1


      #  print (dic)
        self.index['bi'] = dic


    def compute_index(self, filename, tri):
        self.index = {'name': filename, "bi": {}}
        if tri:
            self.index["tri"] = {}
        #raw_sentence = ""
        
        # COMPLETAR #
        
        
        archivo = open(filename, 'r', encoding='utf8')
        texto = archivo.read()
        texto = texto.replace('\n\n', '.') #dividir las frases, cambiando los 2 saltos de línea por '.'
        texto = texto.replace(';', '.')
        texto = texto.replace('\n', '')
        texto = texto.replace('?', '.')
        texto = texto.replace('!', '.')
        texto = texto.replace(',', '')
        texto = texto.split('.')
        
        for linea in texto:
           # frase = ''.join(ch for ch in linea if ch.isalnum()) #quitar símbolos no alfanuméricos 
           # frase = frase.lower()
            if linea == '': continue #si la frase es nula, el bucle para a la siguiente 
            linea = self.r1.sub('', linea)

            frase = '$ ' + linea + ' $' #para saber cuándo acaba y empieza la frase
            self.index_sentence(frase, tri)
           # print(dic, 'diccionario')
        


        
        
       # sort_index(self.index)['bi']
        if tri:
            sort_index(self.index['tri'])
        
        

    def load_index(self, filename):
        with open(filename, "rb") as fh:
            self.index = pickle.load(fh)


    def save_index(self, filename):
        with open(filename, "wb") as fh:
            pickle.dump(self.index, fh)


    def save_info(self, filename):
        with open(filename, "w") as fh:
            print("#" * 20, file=fh)
            print("#" + "INFO".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            print("filename: '%s'\n" % self.index['name'], file=fh)
            print("#" * 20, file=fh)
            print("#" + "BIGRAMS".center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for word in sorted(self.index['bi'].keys()):
                wl = self.index['bi'][word]
                print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)
            if 'tri' in self.index:
                print(file=fh)
                print("#" * 20, file=fh)
                print("#" + "TRIGRAMS".center(18) + "#", file=fh)
                print("#" * 20, file=fh)
                for word in sorted(self.index['tri'].keys()):
                    wl = self.index['tri'][word]
                    print("%s\t=>\t%d\t=>\t%s" % (word, wl[0], ' '.join(["%s:%s" % (x[1], x[0]) for x in wl[1]])), file=fh)


    def generate_sentences(self, n=10):
        #############
        # COMPLETAR #
        #############
        if not 'tri' in self.index:
            frases = ''
            for a in range(n):
                count = 0
                dic = self.index['bi']
                pal = '$'  #comienzo de frase; pal es la palabra actual
                sig = ''  #palabra siguiente. Cuando sea $, la frase termina
                while sig != '$' and count < 25:
                    lista = dic[pal][1] #lista con los sucesores de pal
                    frecuencias = []
                    for l in lista: #poner la palabra repetida tantas veces como su frecuencia de aparición 
                        insertar = [l[1]] * l[0]
                        frecuencias += insertar     
                       #l0 es el número de apariciones en el texto
                      #l1 es la palabra 
                    r =  random.randint(0,len(frecuencias)-1) #elige al azar una palabra, teniendo en cuenta la frecuencia de aparición
                    sig = frecuencias[r] 
                    if sig != '$':  #para que $ no se inserte al final de frase 
                        frases = frases +  ' ' + str(sig)
                        count=count + 1  #palabras de la frase
                    pal = sig 
                
                frases = frases + '\n'
            print(frases)
        else:
            frases = ''
            for a in range(n):
                count = 0
                dic = self.index['tri']
                pal = '$'  #comienzo de frase; pal es la palabra actual
                pal2 = ''
                sig = ''  #palabra siguiente. Cuando sea $, la frase termina
                while sig != '$' and count < 25:
                    lista = dic[(pal, pal2)][1] #lista con los sucesores de pal
                    frecuencias = []
                    for l in lista: #poner la palabra repetida tantas veces como su frecuencia de aparición 
                        insertar = [l[1]] * l[0]
                        frecuencias += insertar     
                       #l0 es el número de apariciones en el texto
                      #l1 es la palabra 
                    r =  random.randint(0,len(frecuencias)-1) #elige al azar una palabra, teniendo en cuenta la frecuencia de aparición
                    sig = frecuencias[r] 
                    if sig != '$':  #para que $ no se inserte al final de frase 
                        frases = frases +  ' ' + str(sig)
                        count=count + 1  #palabras de la frase
                    pal = sig 
                
                frases = frases + '\n'
            print(frases)


        


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")


  