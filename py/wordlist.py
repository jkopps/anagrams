import re
import os.path
import unittest

from utils import *

class Wordlist:
    def __init__(self, proper=False, minLength=1):
        self.proper = proper
        self.linect = 0
        self.words = set()
        
        if proper:
            word_re = re.compile("([A-Za-z']+)")
        else:
            word_re = re.compile("([a-z']+)")
        fname = os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                'import',
                'en_US.dic'
                )
        try:
            fh = open(fname, 'r')
        except IOError as err:
            sys.stderr.write('Could not locate dictionary file en_US.dic\n')
            raise err
        for line in fh:
            self.linect += 1
            m = word_re.match(line)
            if m:
                w = m.groups()[0].lower()
                if len(w) < minLength:
                    continue
                self.words.add(w)

        self.lookup = {}
        for w in self.words:
            k = normalize(w)
            if k not in self.lookup:
                self.lookup[k] = set()
            self.lookup[k].add(w)

    def __contains__(self, k):
        return k in self.lookup
    
    def __getitem__(self, k):
        return self.lookup[k]

class TestWordlist(unittest.TestCase):
    def test_get(self):
        x = Wordlist()
        y = x['acr']
        self.assertEqual(2, len(y))
        self.assertTrue('arc' in y)
        self.assertTrue('car' in y)

    def test_in(self):
        x = Wordlist()
        self.assertTrue(('acr') in x)
        self.assertFalse(('arc') in x)

if __name__ == '__main__':
    unittest.main()
