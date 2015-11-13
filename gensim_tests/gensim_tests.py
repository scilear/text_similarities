"""
http://radimrehurek.com/gensim/simserver.html
"""
import os

from logbook import info, warn, error, FileHandler, StderrHandler
from os import listdir
from os.path import isfile, join
import pandas as pd


# project imports
from doc_group import DocGroups, get_test_doc_groups

#required to show gensim messages
import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# utility functions for text massaging
from gensim.parsing.preprocessing import STOPWORDS

from gensim import utils

def simple_preprocess(text):
    # there we probably need NER and ngram recognisiton
    return utils.simple_preprocess(text)

def tokenize(text):
    return [token for token in simple_preprocess(text) if token not in STOPWORDS]

from simserver import SessionServer
class gensim_news(object):
    def __init__(self):
        self.server = SessionServer(r'c:\temp\data_server')
        print self.server

    def initialise(self, docs):
        corpus4server = self.create_server_corpus(docs)
        self.server.train(corpus4server, method='lsi')

    def create_server_corpus(self, docs):
        return [{'id': '%s' % id, 'tokens': simple_preprocess(text)} for id, text in docs.iteritems()]

    def gensim_similarities(self, docs_dict, new=False):
        text4server = self.create_server_corpus(docs_dict)
        sims = self.server.find_similar(text4server[0], min_score=0.90)
        self.server.index(text4server)
        return sims

def main():
    #read corpus files
    texts = dict()
    files = [f for f in listdir('./data/corpus') if isfile(join('./data/corpus', f))]
    for f in files:
        file_name = './data/corpus/%s' % f
        with open(file_name, 'r') as fi:
            text = fi.read()
            texts[f] = text

    print '##################### corpus files loaded in memory #####################'

    # create index and object for similarity computation
    ncat = gensim_news()
    ncat.initialise(texts)

    print '##################### server trained #####################'

    # # testing on training corpus
    # original_texts = texts
    # columns = ['ref'] + texts.keys()
    # df = pd.DataFrame(columns=columns)
    # df['ref'] = texts.keys()
    # if not os.path.exists('sim_results.csv'):
    #     counter = 0
    #     for k, v in original_texts.iteritems():
    #         data = [k]
    #         data = [k]
    #         doc_dict = dict()
    #         doc_dict[k] = v
    #         try:
    #             sims = ncat.gensim_similarities(doc_dict)
    #             #print(sims)
    #             for t in sims:
    #                 df.loc[counter][t[0]] = t[1] #= np.concatenate((np.asarray([k]), sims), axis=0)
    #         except Exception, e:
    #             print e
    #         counter += 1
    #         print counter
    #     print df
    #     df.to_csv('sim_results.csv')



    # testing on new docs
    texts = dict()
    files = [f for f in listdir('./data/tests') if isfile(join('./data/tests', f))]

    print '##################### test files loaded in memory #####################'

    # TODO need to index all docs and them do a similarity pass so that we do not discover similarities incrementally
    # but we get all of them and that shoudl help us build cluster

    dg = DocGroups()
    for f in files:
        file_name = './data/tests/%s' % f
        print '#############' + file_name
        with open(file_name, 'r') as fi:
            text = fi.read()
            texts[f] = text
            doc_dict = dict()
            doc_dict[f] = text
            sims = ncat.gensim_similarities(doc_dict, True)
            for i in sims:
                doc = i[0]
                sim = i[1]
                if doc in files:
                    dg.add_doc(f, doc, sim)

    dg.show()
    print '##################### similarities computed #####################'

    dg.compare(get_test_doc_groups())
    print '##################### comparison finished #####################'

if __name__ == "__main__":
    main()

