import pprint

class DocGroups(object):
    def __init__(self):
        self.group = dict()
        self.group_scores = dict()
        self.recurse_stop = False

    def add_doc(self, group, doc, score):
        if self.group.has_key(group):
            #add to other docs
            if not self.recurse_stop:
                for d in self.group[group]:
                    if d == group:
                        continue
                    self.recurse_stop = True
                    self.add_doc(d, doc, 0)
                    self.recurse_stop = False
        else:
            self.group[group] = set()
            self.group_scores[group] = set()
        if group != doc:  # no interest in recording a match with itself
            self.group[group].add(doc)
            self.group_scores[group].add((doc, score))

    def show(self):
        pprint.pprint(self.group)

    def compare(self, dg, detailed = False):
        dglc = len(dg.group)
        dgl = len(self.group)

        # report on group length
        if dgl == dglc:
            print 'same group count %d' % dgl
        else:
            print '%d versus % d groups' % (dgl, dglc)

        # check how many groups are different
        for k, v in self.group:
            if dg.group.has_key(k):
                v2 = dg.group[k]
                differences = list(set(v2) - set(v))
                pprint.pprint(differences)
            else:
                print 'group %s not found in dest' % k

def get_test_doc_groups():
    dg = DocGroups()
    dg.add_doc('0_YHOO.txt','0_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','10_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','11_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','12_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','14_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','15_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','17_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','18_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','1_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','21_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','22_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','23_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','2_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','3_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','4_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','7_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','8_YHOO.txt',1)
    dg.add_doc('0_YHOO.txt','9_YHOO.txt',1)
    dg.add_doc('5_YHOO.txt','5_YHOO.txt',1)
    dg.add_doc('6_YHOO.txt','6_YHOO.txt',1)
    dg.add_doc('13_YHOO.txt','13_YHOO.txt',1)
    dg.add_doc('16_YHOO.txt','16_YHOO.txt',1)
    dg.add_doc('19_YHOO.txt','19_YHOO.txt',1)
    dg.add_doc('19_YHOO.txt','20_YHOO.txt',1)
    dg.add_doc('0_AAPL.txt','0_AAPL.txt',1)
    dg.add_doc('0_AAPL.txt','1_AAPL.txt',1)
    dg.add_doc('0_AAPL.txt','24_YHOO.txt',1)
    dg.add_doc('2_AAPL.txt','2_AAPL.txt',1)
    dg.add_doc('4_AAPL.txt','4_AAPL.txt',1)
    dg.add_doc('5_AAPL.txt','5_AAPL.txt',1)
    dg.add_doc('6_AAPL.txt','6_AAPL.txt',1)
    dg.add_doc('6_AAPL.txt','7_MSFT.txt',1)
    dg.add_doc('3_MSFT.txt','3_MSFT.txt',1)
    dg.add_doc('8_MSFT.txt','8_MSFT.txt',1)

    return dg