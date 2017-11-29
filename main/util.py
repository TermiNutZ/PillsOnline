import unicodedata
import sys
from nltk import SnowballStemmer, defaultdict
import numpy as np
from nltk.corpus import stopwords

tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                    if unicodedata.category(chr(i)).startswith('P'))


def remove_punctuation(text):
    return text.translate(tbl)


stemmer = SnowballStemmer('russian')


class LanguageModel:
    def __init__(self, text):
        self.word_freq = defaultdict(float)
        self.word_freq["####"] = 1.0
        self.word_total = 1.0
        self.words = set()

        for word in text.split():
            stem_word = stemmer.stem(word)
            self.word_freq[stem_word] += 1.0
            self.word_total += 1.0
            self.words.add(stem_word)

    def kl_divergence(self, another_lm, coll_lm):
        """
        measure kl divergence between language models
        :param another_lm: language model to which we want find distance
        :param coll_lm: language model of whole collection
        :return: kl distance
        """
        kl = 0.0
        # smoothing coefficients were taken empirically
        for word in self.words.union(another_lm.words):
            pq = 0.9 * (another_lm.word_freq[word] / another_lm.word_total) + \
                 0.1 * (coll_lm.word_freq[word] / coll_lm.word_total)

            pd = 0.9 * (self.word_freq[word] / self.word_total) + \
                 0.1 * (coll_lm.word_freq[word] / coll_lm.word_total)

            kl += pd * np.log(pd / pq)

        return kl


def query_document_similarity(query, document):
    """
    check if query and document have common words
    """
    stop_words = set(stopwords.words('russian'))
    doc_str = remove_punctuation(document).lower()
    query_str = remove_punctuation(query).lower()
    doc_tokens = set([stemmer.stem(word) for word in doc_str.split()])
    query_tokens = set([stemmer.stem(word) for word in query_str.split()])
    query_tokens = query_tokens.difference(stop_words)

    intersect = doc_tokens.intersection(query_tokens)

    return len(intersect) > 0