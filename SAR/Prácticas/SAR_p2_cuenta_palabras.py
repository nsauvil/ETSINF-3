#! -*- encoding: utf8 -*-



########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################

import argparse
import re
import sys
import pathlib
import operator
from collections import defaultdict


def sort_dic_by_values(d, asc=True):
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))

class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')

    def write_stats(self, filename, stats, use_stopwords, full):
        """
        Este método escribe en fichero las estadísticas de un texto
            
        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas

        :return: None
        """
        
        with open(filename, 'w') as fh:
            ## completar
            
                
            fh.write('Lines: ' + str(stats['nlines']) + '\n')
            fh.write('Number words (including stopwords): ' + str(stats['nwords']) + '\n')
            if use_stopwords:
                fh.write('Number words (without stopwords): ' + str(stats['vocab']) + '\n')
            fh.write('Vocabulary size: ' + str(stats['vocabs']) + '\n')
            fh.write('Number of symbols: ' + str(stats['nsymbols']) + '\n')
            fh.write('Number of different symbols: ' + str(stats['nsymbolsd']) + '\n')
            fh.write('Words (alphabetical order): ' + '\n')
            dicw = sorted(stats['word'].items(), key=operator.itemgetter(0), reverse=False)
            i = 0
            for a in dicw:
                fh.write("\t" + str(a[0]) + ": " + str(a[1]) + '\n')
                i = i + 1
                if not full and i >= 20:
                    break
            fh.write('Words (by frequency): ' + '\n')
          #  dicw = sorted(stats['word'].items(), key=operator.itemgetter(1), reverse=True) 
            dicw = sorted(stats['word'].items(), key=lambda a:(-a[1],a[0])) 
            i = 0
            for a in dicw:
                fh.write("\t" + str(a[0]) + ": " + str(a[1]) + '\n')
                i = i + 1
                if not full and i >= 20:
                    break
            fh.write('Symbols (alphabetical order): ' + '\n')
            dics = sorted(stats['symbol'].items(), key=operator.itemgetter(0), reverse=False)
            i = 0
            for a in dics:
                fh.write("\t" + str(a[0]) + ": " + str(a[1]) + '\n')
                i = i + 1
                if not full and i >= 20:
                    break
            fh.write('Symbols (by frequency): ' + '\n')
            dics = sorted(stats['symbol'].items(), key=lambda a:(-a[1],a[0]))
            i = 0
            for a in dics:
                fh.write("\t" + str(a[0]) + ": " + str(a[1]) + '\n')
                i = i + 1
                if not full and i >= 20:
                    break
            
            if stats['bi']:
                fh.write('Word pairs (alphabetical order): ' + '\n')
                dicw = sorted(stats['biword'].items(), key=operator.itemgetter(0), reverse=False)
                i = 0
                for a in dicw:
                    fh.write("\t" + str(a[0]) + ": " + str(a[1]) + '\n')
                    i = i + 1
                    if not full and i >= 20:
                        break
                fh.write('Word pairs (by frequency): ' + '\n')
                dicw = sorted(stats['biword'].items(), key=lambda a:(-a[1],a[0])) 
                i = 0
                for a in dicw:
                   fh.write("\t" + str(a[0]) + ": " + str(a[1]) + '\n')
                   i = i + 1
                   if not full and i >= 20:
                       break
                fh.write('Symbol pairs (alphabetical order): ' + '\n')
                dics = sorted(stats['bisymbol'].items(), key=operator.itemgetter(0), reverse=False)
                i = 0
                for a in dics:
                    fh.write("\t" + str(a[0][0]) + str(a[0][1]) + ": " + str(a[1]) + '\n')
                    i = i + 1
                    if not full and i >= 20:
                        break
                fh.write('Symbol pairs (by frequency): ' + '\n')
                dics = sorted(stats['bisymbol'].items(), key=lambda a:(-a[1],a[0]))
                i = 0
                for a in dics:
                    fh.write("\t" + str(a[0][0]) + str(a[0][1]) + ": " + str(a[1]) + '\n')
                    i = i + 1
                    if not full and i >= 20:
                        break


            pass


    def file_stats(self, filename, lower, stopwordsfile, bigrams, full):
        """
        Este método calcula las estadísticas de un fichero de texto

        :param 
            filename: el nombre del fichero.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?

        :return: None
        """

        stopwords = [] if stopwordsfile is None else open(stopwordsfile).read().split()

        # variables for results

        sts = {
                'nwords': 0,
                'vocab': 0,
                'vocabs' : 0,
                'nsymbols' : 0,
                'nsymbolsd' : 0,
                'nlines': 0,
                'word': {},
                'symbol': {},
                'bi' : False
                }
        stsw = {}
        stss = {}

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}
            sts['bi'] = True
        biw = {} 
        bis = {} 
        
        lastword = "$"
        pd = []
        sd = []  
        
        archivo = open(filename, 'r', encoding='utf8')

        for linea in archivo:
            if lower:
                linea = linea.lower() 
           # linea = ''.join(filter(str.isalnum, linea)) #quita los no alfanuméricos 
            linea = self.clean_re.sub(' ', linea)
            lastword = "$"

            for pal in linea.split():
                if stopwords != [] and stopwords.count(pal) != 0:  #comprobar que no es stopword 
                    sts['vocabs'] -= 1

                if pal not in pd:
                    sts['vocabs'] += 1  #contar palabras distintas
                    
                stsw[pal] = stsw.get(pal,0) + 1   #añadir palabra al dic. Si ya está, aumenta su contador 
                pd.append(pal)
                sts['nwords'] += 1
                sts['vocab'] += 1  #contar palabras sin stopwords 
                 

                if bigrams: 
                    biw[lastword + " " + pal] = biw.get(lastword + " " + pal,0) + 1 
                    lastword = pal
                    #contar bigramas
                for letra in pal:
                    if letra not in sd:
                        sts['nsymbolsd'] += 1  #contar palabras distintas
                    stss[letra] = stss.get(letra,0) + 1
                    sd.append(letra)
                    #contar letras 
                    sts['nsymbols'] += 1
                if bigrams:
                    for i in range(len(pal) - 1):
                        w1, w2 = pal[i : i + 2]
                        bis[(w1,w2)] = bis.get((w1,w2), 0) + 1
                    #obtener pares de símbolos

            if lastword != "$":
                biw[lastword + " $"] = biw.get(lastword + " $", 0) + 1
                #contar bigramas
            sts['nlines'] += 1

        sts['word'] = stsw
        sts['symbol'] = stss 
        sts['biword']  = biw  
        sts['bisymbol']  = bis     

       
        # completar
        exten = pathlib.Path(filename).suffix
        nuevonom = filename[:len(filename) - len(exten)] + "_" 
        stop = False
        if stopwordsfile:
            stop = True
#        recorrer = [lower, stop, bigrams, full] 
        count = 0
#        rec = 1
#       for i in range(len(recorrer)):
#            if recorrer[i]:
        if lower:
            nuevonom = nuevonom + 'l'
            count = count + 1
        if stop:
            nuevonom = nuevonom + 's'
            count = count + 1
#            rec = rec + 1
        if bigrams:
            nuevonom = nuevonom + 'b'
            count = count + 1
        if full:
            nuevonom = nuevonom + 'f'
            count = count + 1
#                rec = rec + 1
        if count > 0:
            nuevonom = nuevonom + '_stats' + exten
        else: 
            nuevonom = nuevonom + 'stats' + exten
        
        new_filename =  open(nuevonom, "w", encoding="utf8")# cambiar
        self.write_stats(nuevonom, sts, stopwordsfile is not None, full)


    def compute_files(self, filenames, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """
 
        for filename in filenames:
            self.file_stats(filename, **args)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower',
                        action='store_true', default=False, 
                        help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                        help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram',
                        action='store_true', default=False, 
                        help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full',
                        action='store_true', default=False, 
                        help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file,
                     lower=args.lower,
                     stopwordsfile=args.stopwords,
                     bigrams=args.bigram,
                     full=args.full)


