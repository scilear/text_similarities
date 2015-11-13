import timeit
import os


##TODO I need to do it differently at the moment if I have A,B,C, it will be stored 3 times!
## this does not handle the fact that an item to could be similar to several distinct groups


"""
    This is a structure to hold similarities of documents
    each documents is mapped through a dictionnay to a set of index
    linking to different groups as it may be similar to distinct groups

    Then we hold a list of groups of documents
    whose index is referred to by the previous dictionnary/set

    so groups are only held in memory once
    but the system will not yet look for group duplicates or group overlap
    ie group could be ABCD and a second group could be either ABCD and ABCDE

    we do not store group that contains themselves
"""
class DocSimilarities(object):
    def __init__(self):
        # stores list of items that have a relationship
        self.relationship_lists = list()
        # will store for each item with relationships the index of the list in relationship_lists
        self.items = dict()

    def add_group(self, item_list):
        for item in item_list:
            self.__add_similar_items(item, item_list)

    def __add_similar_items(self, item, item_list):
        #check if any item already exists and points
        if self.items.has_key(item):
            # add
            idx = self.items[item]
            rl = self.relationship_lists[idx]
            rl += item_list
            sl = set(rl)
            self.relationship_lists[idx] = list(sl)
        else:
            # making sure it is the right format
            il = list(item_list)
            self.relationship_lists.append(il)
            idx = len(self.relationship_lists) - 1
            self.items[item] = idx

    def get_similar_items(self, item):
        if self.items.has_key(item):
            idx = self.items[item]
            return self.relationship_lists[idx]
        return None

    def __str__(self):
        string = ''
        for a in self.relationship_lists:
            string += str(a)
            string += '\n'
        return string


def run_tests():
    import pickle

    # list of items
    ds = None
    start_time = timeit.default_timer()
    if os.path.exists(r'ds.p'):
        ds = pickle.load(open(r'ds.p', 'rb'))
    else:
        ds = DocSimilarities()
        max_gen = 10000000
        il = range(0, max_gen)
        for i in il:
            sim_list = list(range(max(i-50,0), min(i+49,max_gen), 1))
            # me_list = list([i])
            # sim_list = me_list + list(nprnd.randint(max_gen, size=100))
            if (i % 5000 == 0):
                print i
            ds.add_similar_items(sim_list)
        pickle.dump(ds, open( "ds.p", "wb"))
    elapsed = timeit.default_timer() - start_time
    print 'elapsed %d' % elapsed

    #print ds
    start_time = timeit.default_timer()
    for i in il:
        #print '=' * 80
        v = ds.get_similar_items(i)
    elapsed = timeit.default_timer() - start_time
    print 'elapsed %d' % elapsed
    print 'avg elapsed %f' % (1.0 * elapsed / max_gen)

if __name__ == "__main__":
    run_tests()
