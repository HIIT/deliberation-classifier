## index for labels

import os
path = os.path.dirname( __file__ ) + '/'

class LIWC:

    meta_classes = [ 1, 2, 3, 30, 32, 40, 50, 60, 70, 80, 90, 120] ## per LIWC 2015

    def __init__( self, clean_meta_class = True ):
        self.__terms = {}

        for line in open( path + 'liwcdic2015_terms.dic'):

            line = line.strip().split('\t')
            if len( line ) > 1:
                if clean_meta_class and int( line[0] ) in LIWC.meta_classes: ## skip meta_classes when ordered so.
                    self.__terms[ line[0] ] = None
                else:
                    self.__terms[ line[0] ] = line[ 1 ].split(' ')[0] ## only the key description

        self.__words = {}
        self.__cutwords = {}

        for line in open( path + 'LIWC2015_English.dic'):

                line = line.strip().split('\t')
                w = line[0].strip()

                if '*' in w:
                    w = w.replace('*', '')
                    self.__cutwords[ w ] = map( lambda x: self.__terms[ x ] , line[ 1: ] )

                else:
                    self.__words[ w ] = map( lambda x: self.__terms[ x ] , line[ 1: ] )

    def terms( self ):
        return filter( lambda x: x != None, self.__terms.values() )

    def search( self, word ):

        ## simple easy words, just run with them
        if word in self.__words:
            return filter( lambda x: x != None, self.__words[ word ] )


        ## search the index based on word length
        for i in range( len(word), 0, -1 ):
            w = word[ : i ]
            if w in self.__cutwords:
                return filter( lambda x: x != None, self.__cutwords[ w ] )

        return []

if __name__ == '__main__':
    a = LIWC()
    print 'zoom', a.search('zoom')

    print ''

    print 'mine', a.search('mine')

    print ''

    print 'ministery', a.search('ministery')
    print 'ministeries', a.search('ministeries')

    print ''

    print 'minesweeper', a.search('minesweeper')
