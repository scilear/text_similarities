"""
    work in progress, ignore
    TODO reimplement server functionnalities
"""

import os
import pprint
import pandas as pd
from multiprocessing import Process
from logbook import info, warn, error, FileHandler, StderrHandler
import sys
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from gensim import similarities, corpora, models
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# utility functions for text massaging
from gensim.parsing.preprocessing import STOPWORDS

def simple_preprocess(text):
    # there we probably need NER and ngram recognisiton
    return text.lower().split()


def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]


# import ner


texts = dict()
if not os.path.exists('sim_results.csv'):
    files = [f for f in listdir('./data/corpus') if isfile(join('./data/corpus', f))]
    for f in files:
        file_name = './data/corpus/%s' % f
        with open(file_name, 'r') as fi:
            text = fi.read()
            texts[f] = text

original_texts = texts

print 'files loaded in memory'

class CorpusIter(object):
    def __iter__(self):
        for line in open('data.mm'):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())


from simserver import SessionServer


class gensim_news(object):
    def __init__(self):
        self.index = None
        self.dictionnary = None
        self.corpus = None
        self.lsi = None
        self.dictionary = corpora.Dictionary.load('data.dict')
        self.corpus = corpora.MmCorpus('data.mm')
        if os.path.exists('data.lsi'):
            self.lsi = models.LsiModel.load('data.lsi')
        else:
            self.lsi = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=400)
            self.lsi.save('data.lsi')
        print 'lsi data loaded'
        if os.path.exists('index.index'):
            self.index = similarities.Similarity.load('index.index')
            print 'index loaded in memory'


    def initialise(self):
        if not os.path.exists('index.index'):
            self.index = similarities.Similarity('index.index',self.lsi[self.corpus],400)
            self.index.save('index.index')
            print 'index loaded in memory'

    # def gensim_similarities(self, t1):
    #     sim = 0
    #     vec1_bow = self.dictionary.doc2bow(simple_preprocess(t1))
    #     vec_lsi = self.lsi[vec1_bow]
    #     sims = self.index[vec_lsi]
    #     return sims
    #
    def gensim_similarities(self, t1, new=False):
        sim = 0
        vec1_bow_old = self.dictionary.doc2bow(simple_preprocess(t1))
        vec1_bow = self.dictionary.doc2bow(tokenize(t1))
        vec_lsi = self.lsi[vec1_bow]
        sims = self.index[vec_lsi]
        if new:
            try:
                corpus = [vec1_bow]
                corpora.MmCorpus.serialize('data_tmp.mm', corpus)
                corpus_obj = corpora.MmCorpus('data_tmp.mm')
                self.index.add_documents(corpus_obj)
            except:
                pass

            try:
                corpus = vec1_bow
                corpora.MmCorpus.serialize('data_tmp.mm', corpus)
                corpus_obj = corpora.MmCorpus('data_tmp.mm')
                self.index.add_documents(corpus_obj)
            except:
                pass

            return sims



columns = ['ref'] + texts.keys()
df = pd.DataFrame(columns=columns)
df['ref'] = texts.keys()
#print df


dictionary = None
if os.path.exists('data.dict'):
    dictionary = corpora.Dictionary.load('data.dict')
else:
    ##create dictionnary
    for k, v in texts.items():
        texts[k] = tokenize(v)
    # not doing anything with frequency count yet!
    dictionary = corpora.Dictionary(texts.values())
    dictionary.save('data.dict')
print 'dictionnary loaded in memory'

##create corpus
corpus = None
if os.path.exists('data.mm'):
    corpus = corpora.MmCorpus('data.mm')
else:
    # now we need to convert doc in the dictionnary vector representation
    corpus = [dictionary.doc2bow(text) for text in texts.values()]
    corpora.MmCorpus.serialize('data.mm', corpus)
print 'corpus loaded in memory'

# create index and object for similarity computation
ncat = gensim_news()
ncat.initialise()

# testing on training corpus
if not os.path.exists('sim_results.csv'):
    counter = 0
    for k, v in original_texts.iteritems():
        data = [k]
        data = [k]
        sims = ncat.gensim_similarities(v)
        #print(sims)
        df.loc[counter] = np.concatenate((np.asarray([k]), sims), axis=0)
        counter += 1
        print counter
    print df
    df.to_csv('sim_results.csv')

# testing on new docs
#loading new doc from
texts = dict()
files = [f for f in listdir('./data') if isfile(join('./data', f))]
from_size = 0
for f in files:
    file_name = './data/%s' % f
    with open(file_name, 'r') as fi:
        text = fi.read()
        texts[f] = text
        sims = ncat.gensim_similarities(text, True)
        if from_size == 0:
            from_size = len(sims)-1
        print sims[from_size:]



