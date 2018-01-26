'''
make_ngrams.py

Generate n-grams for a given directory of extracted narratives and
save to a whitespace delimited csv file.
Punctuation and stop words are not removed to make the sample more generic,
numbers are turned into `<NUM>` tokens, `(Laughter)` and `(Applause)`
annotations are preserved.

tokenizing pattern:
    r'\(laughter\)|\(applause\)|\d*[,.]\d+|\w+|[^\w\s]'

requirements: ntlk
'''
import os
import sys
import re
from collections import Counter

from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer


def main():
    # edit to change the output.
    foldername = "cleaned_ted_data"
    ngrams_to_csv(foldername, n=1, outfile="ted_ngrams/unigram.csv")
    ngrams_to_csv(foldername, n=2, outfile="ted_ngrams/bigram.csv")
    ngrams_to_csv(foldername, n=3, outfile="ted_ngrams/trigram.csv")


def generate_ngrams(directory, n=3, sample=50000):
    '''loop through a given directory generate and
    return a `collections.Counter` of ngrams'''
    counts = Counter()
    for root, dirs, files in os.walk(directory):
        for name in files:
            if not name.endswith(".md") or name == "README.md":
                continue
            filename = os.path.join(root, name)
            try:
                with open(filename, "r") as f:
                    text = f.read()
            except IOError:
                print("could not open file: %s" % filename)
            # proccess data into ngrams.
            # `transcript_tokenizer` & `isnum` defined later.
            tokens = transcript_tokenizer.tokenize(text.lower())
            tokens = ("<NUM>" if isnum.match(t) else t for t in tokens)
            counts.update(ngrams(tokens, n))
    return counts.most_common(sample)

def ngrams_to_csv(directory, n=3, sample=50000, outfile="ngram.csv"):
    "write ngram Counter to ' ' delimeted csv file with no header"
    counts = generate_ngrams(directory, n, sample)
    with open(outfile, "w") as out:
        for keys, c in counts:
            out.write("{} {}\n".format(concat(keys), c))
    print("n={}. From '{}/' created file '{}' with {} unique entries".format(
            n, directory, outfile, len(counts)))

concat = " ".join

transcript_tokenizer = RegexpTokenizer(r"\(laughter\)|\(applause\)|\d*[,.]\d+|\w+|[^\w\s]")

isnum = re.compile("^[\d.]*\d+$|\d+,\d+")


if __name__ == "__main__":
    main()
