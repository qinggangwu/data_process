import gzip, os, re
from math import log

__version__ = '2.0.0'

class LanguageModel(object):
    def __init__(self, word_file):
        # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
        # with gzip.open(word_file) as f:
        #   words = f.read().decode().split()
        with open(word_file) as f:
            words = f.read().split()
        self._wordcost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
        self._maxword = max(len(x) for x in words)
        self._SPLIT_RE = re.compile("[^a-zA-Z0-9,.?:']+")   # 对拆分点进行设定

    def split(self, s):
        """Uses dynamic programming to infer the location of spaces in a string without spaces."""
        l = [self._split(x) for x in  self._SPLIT_RE.split(s)]
        return [item for sublist in l for item in sublist]

    def _split(self, s):
        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        def best_match(i):
            candidates = enumerate(reversed(cost[max(0, i - self._maxword):i]))
            return min((c + self._wordcost.get(s[i - k - 1:i].lower(), 9e999), k + 1) for k, c in candidates)

        # Build the cost array.
        cost = [0]
        for i in range(1, len(s) + 1):
            c, k = best_match(i)
            cost.append(c)

        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(s)
        while i > 0:
            c, k = best_match(i)
            assert c == cost[i]
            # Apostrophe and digit handling (added by Genesys)
            newToken = True
            if not s[i - k:i] == "'":  # ignore a lone apostrophe
                if len(out) > 0:
                    # re-attach split 's and split digits
                    if out[-1] == "'s" or (s[i - 1].isdigit() and out[-1][0].isdigit()):  # digit followed by digit
                        out[-1] = s[i - k:i] + out[-1]  # combine current token with previous token
                        newToken = False
            # (End of Genesys addition)

            if newToken:
                out.append(s[i - k:i])
            i -= k
        return reversed(out)


def mergeList(s1,s2):
    rezult = []
    for index,ls in enumerate(s2):
        ls.insert(0,s1.pop(0))
        rezult += ls

    if len(s1) != 0:
        rezult.append(s1[0])
        return " ".join(rezult)
    else:
        return " ".join(rezult)

def main(s:str):
    DEFAULT_LANGUAGE_MODEL = LanguageModel('newWord.txt')

    # 寻找子串
    splitList  = re.split("[a-zA-Z':]{2,}",s)
    sList  = re.findall("[a-zA-Z':]{2,}",s)
    sList = [ DEFAULT_LANGUAGE_MODEL.split(sre) for sre in sList ]
    return mergeList(splitList,sList)



if __name__ == "__main__":
    s1 = "ss四、1.It'sred6:00myschoolbag1992isredandyellowzoo."
    # s1 = "ss四、1.6:00"

    print(main(s1))
