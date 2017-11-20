from django.core.management.base import BaseCommand
from main.models import Medication
from tqdm import tqdm

from main.util import remove_punctuation, LanguageModel


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
