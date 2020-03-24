import argparse
import csv
from os import  environ, path
from django.db.models.fields import *
import getattr
import csv

# Use the database models from Django
environ.setdefault('DJANGO_SETTINGS_MODULE', 'tag_gac.settings')
import django
django.setup()


def sort_bools(line, key, value):
    if line[key] == 'YES':
        value=True
    elif line[key] == 'NO':
        value=False
    else:
        value=line[key]
    return line


fields_list = [field.name for field in model._meta.get_fields()]

with open(csv_file, 'r', encoding='utf-8', errors='ignore') as txt_file:
    lines = csv.DictReader(txt_file, dialect='excel')
    headers = next(txt_file)

    if not headers == fields_list:
        print('Model fields and csv fields not the same')
    else:
        model_dict = {}
        for field in fields_list:
            model_dict[field] = getattr(model, field)
        total = 0
        duplicates = 0
        prev_key = ''
        for line in lines:
            current_key = ''
            charfield = [field.name for field in model._meta.get_fields().__class__ is CharField]
            for field in charfield:
                current_key = current_key + line[field]
            if not current_key == prev_key:
                for key, value in model_dict.items:
                    model.objects.update_or_create(
                        sort_bools(line=line, key=key, value=value)
                    )
                total += 1
            else:
                duplicates += 1
            prev_key = current_key


