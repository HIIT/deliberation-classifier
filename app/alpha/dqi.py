import collections
import itertools
import numpy
import pickle

## machine learning
from sklearn import svm, grid_search, cross_validation

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

    model = grid_search.GridSearchCV( estimator , grid, cv = 10, verbose = 5 )

    data = numpy.array( data )
    labels = numpy.array( labels )

    ## separate train and test
    data_train, data_test, labels_train, labels_test = cross_validation.train_test_split( data, labels, test_size = .2 )

    model.fit( data, labels )

    pickle.dump( model, open('model.svm', 'w') )

    print "Test result"
    print model.score( data_train, labels_train )
    print ""
    print "Test result"
    print model.score( data_test, labels_test )

def predict( textline ):

    model = pickle.load( open('alpha/model.svm') )
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

    labels = map( lambda x: int( x['jl'] ) >= 2, d )
    data = map( lambda x: preprocess( x['text'] ), d )

    print "Data size", len( data )

    print 'Start tuning'

    learn( data, labels )

    print 'Done tuning, model saved'
