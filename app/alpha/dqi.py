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

    for k,v in liwcs.items():
        f['feature_liwc_' + k ] = float( v ) / len( tokens )

    f['feature_length'] = len( text )
    f['feature_sentences'] = len( tokens )

    ret = []

    for k in sorted( f.keys() ):
        ret.append( f[k] )

    return ret

def learn( data ):

    estimator = svm.SVC()
    grid = [
        {'C': range( 0.5 , 10, .5 ) + range(10,50, 1), 'gamma': range( .0001, .1 .0005) , 'kernel': ['rbf', 'sigmoid'] },
    ]

    model = grid_search.GridSearchCV( estimator , grid )

    model.fit( data, labels )
    print model.score()

    pickle.dump( model, open('model.svm', 'w') )

def predict( textline ):

    model = pickle.load( open('model.svm') )
    return model.predict( preprocess( textline ) )


if __name__ == "__main__":
    learn()
