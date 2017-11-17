from django.core.management.base import BaseCommand
from main.models import Medication
from tqdm import tqdm
class DictFromFile:
    def __init__(self, path):
        self.f_in = open(path, "r")
    def getDict(self):
        self.lines = self.f_in.readlines()
        splitted_data = [line.split('\t') for line in self.lines]
        dict = {item[0]:int(item[1]) for item in splitted_data}
        return dict
class Command(BaseCommand):
    help = 'Populates warnings: pregnancy, kidney, liver'
    def handle(self, *args, **options):
        # make a dict with classes
        print("Populates warnings: pregnancy, kidney, liver")
        preg_dict = DictFromFile("static/preg_warnings.txt").getDict()
        kidney_dict = DictFromFile("static/kidney_warnings.txt").getDict()
        liver_dict = DictFromFile("static/liver_warnings.txt").getDict()
        medications = Medication.objects.all()
        for medication in tqdm(medications):
            medication.warn_pregnancy = preg_dict[medication.title[:-1]]
            medication.warn_kidney = kidney_dict[medication.title[:-1]]
            medication.warn_liver = liver_dict[medication.title[:-1]]
            medication.save()