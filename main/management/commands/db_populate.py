from django.core.management.base import BaseCommand
from main.models import Medication
import os
class Command(BaseCommand):
    help = 'Populates medication'
    def handle(self, *args, **options):
        for root, dirs, files in os.walk('static/desc'):
            for file in files:
                if(file[-3:]=="txt"):
                    print(file)
                    with open(root+os.sep+file) as f:
                        data = f.readlines()
                        title = data[0]
                        splitted_h_d = "\n".join(data[1:]).split('!#!')
                        transl_dict = {'Показания': 'indication', 'Дозировка': 'dosage', 'Противопоказания': 'contra',
                                       'Побочные действия': 'side_effect', 'Фармакологическое действие': 'pharm_action',
                                       'Особые указания': 'spec_instruct', 'Беременность и лактация': 'pregnancy',
                                       'Лекарственное взаимодействие': 'med_interact', 'Фармакокинетика': 'pharm_kinetic',
                                       'Применение в детском возрасте': 'child_policy',
                                       'Клинико-фармакологическая группа': 'clinic_pharm_group',
                                       'Форма выпуска, состав и упаковка': 'form_composition',
                                       'Условия отпуска из аптек': 'distr_policy',
                                       'Условия и сроки хранения': 'expiration_date', 'Передозировка': 'overdosage',
                                       'При нарушениях функции почек': 'kidney', 'При нарушениях функции печени': 'liver',
                                       'Применение в пожилом возрасте': 'old_policy'}
                        paste_dict = {}
                        for h_d in splitted_h_d:
                            if h_d != '':
                                h_d = h_d.split('#!#\n\n')
                                paste_dict[transl_dict[h_d[0]]] = h_d[1]
                            for key, item in transl_dict.items():
                                if item not in paste_dict:
                                    paste_dict[item] = ''
                        img_path=''
                        for img_root,_,img_files in os.walk('static/img'):
                            for img in img_files:
                                if img[:-4] == file[:-4]:
                                    img_path = img_root + os.sep + img
                        cur_med = Medication(title=title,
                                             indication=paste_dict['indication'],
                                             dosage=paste_dict['dosage'],
                                             contra=paste_dict['contra'],
                                             side_effect=paste_dict['side_effect'],
                                             pharm_action=paste_dict['pharm_action'],
                                             spec_instruct=paste_dict['spec_instruct'],
                                             pregnancy=paste_dict['pregnancy'],
                                             med_interact=paste_dict['med_interact'],
                                             pharm_kinetic=paste_dict['pharm_kinetic'],
                                             child_policy=paste_dict['child_policy'],
                                             clinic_pharm_group=paste_dict['clinic_pharm_group'],
                                             form_composition=paste_dict['form_composition'],
                                             distr_policy=paste_dict['distr_policy'],
                                             expiration_date=paste_dict['expiration_date'],
                                             overdosage=paste_dict['overdosage'],
                                             kidney=paste_dict['kidney'],
                                             liver=paste_dict['liver'],
                                             old_policy=paste_dict['old_policy'],
                                             img_path=img_path
                                             )
                        cur_med.save()

        print("DB populated successfuly!")