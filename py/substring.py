import string
import sys
import unittest

from wordlist import Wordlist
from utils import *

class Congruence:
    def __init__(self, remainder=None, words=None):
        ### each "remainder" substring maps to a set of word tuples
        self.data = {}
        if remainder == None and words != None:
            raise ValueError('Must specify remainder with words')
        if remainder != None:
            self.data[remainder] = set()
        if words != None:
            self.data[remainder].add(tuple(sorted(words)))

    def __contains__(self, k):
        return k in self.data

    def __getitem__(self, k):
        return self.data[k]

    def iteritems(self):
        return self.data.iteritems()
            
    def merge(self, remainder, w1, w2):
        """Merge two sub-congruences into this one
        """
        errmsg = 'parameters w1 and w2 must be sets of tuples of strings'
        if type(w1) != set or type(w2) != set:
            raise ValueError(errmsg)
        if type(remainder) != str:
            raise ValueError('remainder parameter must be str')
                   
        k = normalize(remainder)
        if k not in self.data:
            self.data[k] = set()
        if w1 == set():
            for t in w2:
                self.data[k].add(t)
            return
        if w2 == set():
            for t in w1:
                self.data[k].add(t)
            return
        for t1 in w1:
            # assert type(t1) == tuple, ValueError(errmsg)
            for t2 in w2:
                # assert type(t2) == tuple, ValueError(errmsg)
                v = tuple(sorted(t1 + t2))
                self.data[k].add(v)

class TestCongruence(unittest.TestCase):
    def test_merge(self):
        x1 = Congruence('x1', ('a', 'b'))
        x2 = Congruence('x2', ('d', 'c'))
        x3 = Congruence('x3', ('f', 'e'))
        x4 = Congruence('x4', ('g', 'h'))
        ##
        y = Congruence()
        y.merge('y1', x1.data['x1'], x2.data['x2'])
        y.merge('y2', x3.data['x3'], x4.data['x4'])
        #
        self.assertTrue('1y' in y.data)
        self.assertTrue('2y' in y.data)
        self.assertEqual(len(y.data), 2)
        self.assertTrue(('a','b','c','d') in y.data['1y'])
        self.assertTrue(('e','f','g','h') in y.data['2y'])
        ##
        z = Congruence()
        z.merge('z', y.data['1y'], y.data['2y'])
        #
        self.assertTrue('z' in z.data)
        self.assertEqual(len(z.data), 1)
        self.assertTrue(('a','b','c','d','e','f','g','h') in z.data['z'])

    def test_merge_halfEmpty(self):
        z = Congruence()
        w1 = set()
        w1.add(('abc', 'def'))
        w1.add(('ghi', 'jkl'))
        w2 = set()
        z.merge('k', w1, w2)
        self.assertTrue('k' in z.data)
        self.assertTrue(('abc', 'def') in z.data['k'])

class AnagramTree:
    def __init__(self, wordlist=None):
        if wordlist == None:
            wordlist = Wordlist()
        self.wordlist = wordlist
        # nodes is a mapping of (normalized) strings to anagram congruences
        self.nodes = {}
        # make base entry of single characters
        for c in string.letters[0:26]:
            self.nodes[c] = Congruence(c, None)

    def add(self, s):
        if s == '' or type(s) != str:
            raise ValueError('Input must be a nontrivial string')        
        if s in self.nodes:
            return

        s = normalize(s)
        ret = Congruence()
        if s in self.wordlist:
            ret.merge('', self.wordlist[s], set())

        for c, s1 in substrings(s).iteritems():
            # s = c + s1
            x = self.get(s1)
            for r1, w1 in x.iteritems():
                #    s1  = r1 + w1[i]
                # => s   = (c + r1) + w1[i]
                #
                # degenerate case: w1 = '', meaning c+r1 = s
                if len(w1) == 0:
                    continue
                s2 = normalize(c + r1)
                if s2 in self.wordlist:
                    # Eureka! No remainder
                    ret.merge('', self.wordlist[s2], w1)
                else:
                    y = self.get(c + r1)
                    for r2, w2 in y:
                        #    c + rem = r2 + w2
                        # => c + rem + w1 = r2 + w1 + w2
                        # => c + subs = r2 + w1 + w2
                        # => s = r2 + w1 + w2
                        ret.merge(r2, w1, w2)
        self.nodes[s] = ret
        
    def get(self, s):
        sys.stderr.write('get called on "%s"\n' % s)
        s = normalize(s)
        self.add(s)
        return self.nodes[s]

class TestAnagramTree(unittest.TestCase):
    def test_add_wordOrdered(self):
        tree = AnagramTree()
        tree.add('be')
        z = tree.get('be')
        self.assertTrue('' in z)
        self.assertTrue('be' in z[''])

    def test_add_wordUnordered(self):
        tree = AnagramTree()
        tree.add('bed')
        z = tree.get('bed')
        self.assertTrue('' in z)
        self.assertTrue('bed' in z[''])

    def test_add_words(self):
        tree = AnagramTree()
        z = tree.get('fatcat')
        self.assertTrue('' in z)
        self.assertTrue(('cat', 'fat') in z[''])

# Algorithm
# for each substring:
#    words, partial = findAnagrams(substring)
#    w2, p2 = findAnagrams(partial + missingletter)
#    return (words + w2, p2)
#    return (words, partial + missingletter)

if __name__ == '__main__':
    unittest.main()
