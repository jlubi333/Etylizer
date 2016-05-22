import string
import requests
import nltk
from nltk.stem import WordNetLemmatizer

INFINITY = float("+inf")
GERMANIC = "Germanic"
LATIN = "Latin"
ORIGINS = [GERMANIC, LATIN]

nltk.data.path.append("/home/justin/Documents/nltk_data")
WORD_NET = WordNetLemmatizer()

def indexSmallestPositiveInteger(xs):
    minValue = INFINITY
    minIndex = -1
    for i in range(0, len(xs)):
        if xs[i] >= 0 and xs[i] < minValue:
            minValue = xs[i]
            minIndex = i
    return minIndex

def getOnlineEtymologyPage(word):
    return requests.get("http://www.etymonline.com/index.php?term=" + word)

def getEtymology(word):
    possibleRoots = [ word
                    , WORD_NET.lemmatize(word, pos="n")
                    , WORD_NET.lemmatize(word, pos="v")
                    , WORD_NET.lemmatize(word, pos="a")
                    ]

    done = False
    for root in possibleRoots:
        page = getOnlineEtymologyPage(root)
        entry = page.text.lower()

        originOccurrences = []
        for origin in ORIGINS:
            originOccurrences.append(entry.find(origin.lower()))

        firstOccurrenceIndex = indexSmallestPositiveInteger(originOccurrences)
        if (firstOccurrenceIndex != -1):
            return ORIGINS[firstOccurrenceIndex]

    return None

def getWordList(s):
    return "".join(c for c in s if c not in string.punctuation).split(" ")

def main():
    print()
    print("===================================")
    print(" Etylizer - The Etymology Analyzer ")
    print("===================================")
    print()
    while True:
        cmd = input("(w)ord, (f)ile, or (q)uit: ").lower()
        if cmd == "w":
            print()
            word = input("Enter a word: ")
            ety = getEtymology(word)
            if ety is None:
                ety = "Unknown"
            print()
            print("===================================")
            print(" Origin:", ety)
            print("===================================")
            print()
        elif cmd == "f":
            print()
            fileName = input("Enter a file name: ")
            with open(fileName, "r") as f:
                contents = f.read()
                wordList = getWordList(contents)
                length = len(wordList)
                i = 1
                germanic = 0
                latin = 0
                unknown = 0
                print()
                for word in wordList:
                    print("Analyzing word", i, "of", length)
                    ety = getEtymology(word)
                    if ety == GERMANIC:
                        germanic += 1
                    elif ety == LATIN:
                        latin += 1
                    else:
                        unknown += 1
                    i += 1
                print()
                print("===================================")
                print(" Germanic:", germanic, "(" + str(round(100 * germanic / length)) + "%)")
                print(" Latin:", latin, "(" + str(round(100 * latin / length)) + "%)")
                print(" Unknown:", unknown, "(" + str(round(100 * unknown / length)) + "%)")
                print("===================================")
                print()
        elif cmd == "q":
            return

if __name__ == "__main__":
    main()
