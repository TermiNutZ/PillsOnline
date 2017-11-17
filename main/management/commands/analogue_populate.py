from django.core.management.base import BaseCommand
from main.models import Medication
from collections import defaultdict
import numpy as np
from nltk.stem.snowball import SnowballStemmer
from tqdm import tqdm
import unicodedata
import sys

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
        kl = 0.0
        for word in self.words.union(another_lm.words):
            pq = 0.9 * (another_lm.word_freq[word] / another_lm.word_total) + \
                 0.1 * (coll_lm.word_freq[word] / coll_lm.word_total)

            pd = 0.9 * (self.word_freq[word] / self.word_total) + \
                 0.1 * (coll_lm.word_freq[word] / coll_lm.word_total)

            kl += pd * np.log(pd / pq)

        return kl


class Command(BaseCommand):
    def handle(self, *args, **options):
        medications = Medication.objects.all()
        print("GET ", len(medications), "MEDICATIONS FROM DB")
        lms = []
        collection_str = ""
        print("MAKING LANGUAGE MODELS")
        for medication in tqdm(medications):
            cur_str = remove_punctuation(medication.indication + ' ' + medication.pharm_action).lower()
            lms.append(LanguageModel(cur_str))
            collection_str += cur_str + ' '

        coll_lm = LanguageModel(collection_str)

        print("FINDING AND SAVING ANALOGUES TO DB")
        for med_ind in tqdm(range(len(lms))):
            scores = []
            for i in range(med_ind + 1, len(lms)):
                if lms[med_ind].kl_divergence(lms[i], coll_lm) <= 1.5:
                    scores.append(medications[i])
            medications[med_ind].analogues.add(*scores)
            medications[med_ind].save()
