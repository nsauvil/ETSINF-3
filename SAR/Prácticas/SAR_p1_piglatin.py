#!/usr/bin/env python
#! -*- encoding: utf8 -*-

# 1.- Pig Latin

import sys
import re
import pathlib
""" findall"""


class Translator():

    def __init__(self, punt=None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            punt = ".,;?!"
        self.re = re.compile(r"(\w+)([" + punt + r"]*)")
        

    def translate_word(self, word):
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """

        #sustituir
        vocales = "a,e,i,o,u,y,A,E,I,O,U,Y"
        new_word = word
        punt = ".,;?!"
        i = 0
        aux = ""
        a = 0
        mayus = False
        coma2 = ""
        for i in range(len(word)):
            if i == 0 and word[len(word) - 1] in punt:
                coma2 = word[len(word) - 1]
                new_word = new_word[:len(word) - 1]
                
            if i == 0 and (vocales.find(word[i]) != -1):    #primera letra es vocal
                if word.isupper():                #todas son mayúsculas
                    new_word = new_word + 'YAY' + coma2
                    return new_word
                else :
                    new_word = new_word + 'yay' + coma2    #no todas las letras son mayúsculas
                    return new_word
            
            else:
                if vocales.find(word[i])!= -1:     #si empieza por consonante, busca la primera vocal
                    if word.isupper():
                        new_word = new_word[a:] + aux +  'AY' + coma2
                        if mayus:
                            new_word = new_word.capitalize()
                        return new_word
                    else:
                        new_word = new_word[a:] + aux +  'ay' + coma2  
                        #cuando la encuentra, pone el prefijo al final + ay
                        if mayus:
                            new_word = new_word.capitalize()
                        return new_word
                    
                else:
                    if i == 0 and word[i].isupper() and not word.isupper():
                        aux=aux + word[i].lower()
                        a = a + 1
                        mayus=True
                    else :
                        aux=aux + word[i]
                        a = a + 1
                        aux.replace(' ', '')
        return new_word

    def translate_sentence(self, sentence):
        """
        Recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """

        # sustituir
        new_sentence = sentence
        aux = ""
        res = ""
        new_sentence = sentence.split()
        for palabra in new_sentence:
            aux = self.translate_word(palabra)
            res = res + " " + aux
        new_sentence = res
        return new_sentence

    def translate_file(self, filename):
        """
        Recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: True / False 
        """
        fin = pathlib.Path(filename).suffix
        nuevo = filename[:len(filename) - len(fin)] 
        archivo = open(f'{nuevo}_latin{fin}', 'a+')
        antiguo = open(filename)
        lineas = antiguo.readlines()
        
        for i in range(len(lineas)):
            sol = self.translate_sentence(lineas[i]).strip()
            archivo.write( f'{sol}\n' )
            
        
        return True    
        # rellenar

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f'Syntax: python {sys.argv[0]} [filename]')
        exit()
    t = Translator()
    if len(sys.argv) == 2:
        t.translate_file(sys.argv[1])
    else:
        sentence = input("ENGLISH: ")
        while len(sentence) > 1:
            print("PIG LATIN:", t.translate_sentence(sentence))
            sentence = input("ENGLISH: ")