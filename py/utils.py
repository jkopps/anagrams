import unittest

def normalize(s):
    return reduce(lambda a, b: a+b, sorted(list(s)), '')

def wordset(a='', b=''):
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a
    z = a.split(',') + b.split(',')
    z.sort()
    return reduce(lambda a, b: '%s,%s' % (a,b), z)

def substrings(s):
    ret = {}
    for i in range(len(s)-1):
        c = s[i]
        if c in ret:
            continue
        ret[c] = s[:i] + s[i+1:]
    return ret

def anacmp(a, b):
    a_ = a.split(' ')
    b_ = b.split(' ')
    if len(a_) != len(b_):
        return cmp(len(a_), len(b_))
    return cmp(min(map(len, b_)), min(map(len, a_)))

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

    def test_wordset(self):
        self.assertEqual('abc,def', wordset('abc', 'def'))
        self.assertEqual('abc,def', wordset('abc,def'))
        self.assertEqual('abc', wordset('abc'))
        self.assertEqual('abc', wordset('', 'abc'))
        self.assertEqual('abc,def,ghi,jkl', wordset('abc,ghi', 'def,jkl'))
        self.assertEqual('abc,def,ghi,jkl', wordset('abc,ghi,jkl', 'def'))
        self.assertEqual('abc,def,ghi,jkl', wordset('ghi', 'abc,def,jkl'))

    def test_anacmp(self):
        x = ['aa bb cc', 'aa bbc c', 'aab bcc', 'aa bbcc']
        expected = ['aab bcc', 'aa bbcc', 'aa bb cc', 'aa bbc c']
        x.sort(cmp=anacmp)
        self.assertEqual(x, expected)

if __name__ == '__main__':
    unittest.main()
