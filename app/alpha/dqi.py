import collections
import itertools
import numpy
import pickle

## machine learning
from sklearn import svm, grid_search

## handling natural language
from liwc import liwc
_liwc = liwc.LIWC()

import nltk
import nltk.data

lemma = nltk.stem.wordnet.WordNetLemmatizer()
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def preprocess( text ):

    tokens = nltk.word_tokenize( text )
    tokens = map( lambda x: lemma.lemmatize(x).lower(), tokens )

    ## liwc transformation
    liwcs = map( lambda x: _liwc.search( x.lower() ) , tokens )
    liwcs = list( itertools.chain( *liwcs ) )
    liwcs = collections.Counter( liwcs )

    f = {}

    for term in _liwc.terms():

        f['feature_liwc_' + term ] = 0

    for k,v in liwcs.items():
        f['feature_liwc_' + k ] = float( v ) / len( tokens )

    f['feature_length'] = len( text )
    f['feature_sentences'] = len( tokens )

    ret = []

    for k in sorted( f.keys() ):
        ret.append( f[k] )

    return ret

def learn( data, labels ):

    estimator = svm.SVC()
    grid = [
        {'C': numpy.arange( 0.5 , 10, .5 ), 'gamma': numpy.arange( .0001, .1, .0005) , 'kernel': ['rbf', 'sigmoid'] },
    ]

    model = grid_search.GridSearchCV( estimator , grid )

    data = numpy.array( data )
    labels = numpy.array( labels )

    model.fit( data, labels )

    pickle.dump( model, open('model.svm', 'w') )

    print model.score( data, labels )

def predict( textline ):

    model = pickle.load( open('model.svm') )
    data = numpy.array( preprocess( textline ) )
    return model.predict( [ data ] )


if __name__ == "__main__":

    ## teach with real data

    def _int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False


    import json
    d = json.load( open( '/Users/mnelimar/projects/2015-dqi/lord/data.json' ) )
    d = filter( lambda x: x['text'] != '', d )
    d = filter( lambda x: _int( x['jl'] ), d )

    labels = map( lambda x: int( x['jl'] ), d )
    data = map( lambda x: preprocess( x['text'] ), d )

    print len( data )
    print len( labels )

    print 'Start tuning'

    learn( data, labels )

    print 'Done tuning, model saved'
