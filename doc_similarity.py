import profile
import timeit


class DocSimilarities(object):
    def __init__(self):
        # stores list of items that have a relationship
        self.relationship_lists = list()
        # will store for each item with relationships the index of the list in relationship_lists
        self.items = dict()

    def add_similar_items(self, item_list):
        for item in item_list:
            self.__add_similar_items(item, item_list)

    def __add_similar_items(self, item, item_list):
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
    import random as rnd


    # list of items
    ds = DocSimilarities()
    max_gen = 5000
    start_time = timeit.default_timer()
    il = range(0, max_gen)
    for i in il:
        sim_list = list()
        for j in il:
            if i == j or rnd.randint(0,10) >= 9:
                sim_list.append(j)
        ds.add_similar_items(sim_list)
    elapsed = timeit.default_timer() - start_time
    print 'elapsed %d' % elapsed

    #print ds
    start_time = timeit.default_timer()
    for i in il:
        #print '=' * 80
        v = ds.get_similar_items(i)
        #print '%d - %s' % (i, )
    elapsed = timeit.default_timer() - start_time
    print 'elapsed %d' % elapsed
    print 'avg elapsed %d' % 1.0 * elapsed / max_gen

if __name__ == "__main__":
    run_tests()
