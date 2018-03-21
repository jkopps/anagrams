import re
import os.path

class Wordlist:
    def __init__(self, proper=False):
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
                self.words.add(w)
