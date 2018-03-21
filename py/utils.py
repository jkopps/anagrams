import unittest

def normalize(s):
    return reduce(lambda a, b: a+b, sorted(list(s)), '')

def substrings(s):
    ret = {}
    for i in range(len(s)-1):
        c = s[i]
        if c in ret:
            continue
        ret[c] = s[:i] + s[i+1:]
    return ret

class TestUtilities(unittest.TestCase):
    def test_normalize_empth(self):
        x = ''
        y = ''
        self.assertEqual(y, normalize(x))
        
    def test_normalize_charSingle(self):
        x = 'a'
        y = 'a'
        self.assertEqual(y, normalize(x))

    def test_normalize_charRepeated(self):
        x = 'bb'
        y = 'bb'
        self.assertEqual(y, normalize(x))

    def test_normalize_wordUniqueChars(self):
        x = 'cat'
        y = 'act'
        self.assertEqual(y, normalize(x))

    def test_normalize_wordWithRepeats(self):
        x = 'aardvark'
        y = 'aaadkrrv'
        self.assertEqual(y, normalize(x))
        
    def test_substrings_wordWithRepeats(self):
        sup = 'aabbcc'
        expected = {'a' : 'abbcc', 'b' : 'aabcc', 'c' : 'aabbc'}
        actual = substrings(sup)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
