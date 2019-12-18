
import argparse
from colorama import Fore, init as colorama_init, Style
import csv
from os import  environ, path
import sys

# Use the database models from Django
environ.setdefault('DJANGO_SETTINGS_MODULE', 'tag_gac.settings')
import django
django.setup()
from guide.models import GoodsCodes, ConstructionCodes, ServicesCodes


def load_goods(csv_file: str):
    with open(csv_file, 'r', encoding='utf8', errors="ignore") as txt_file:
        gc_reader = csv.DictReader(txt_file, dialect='excel')
        total = 0
        duplicates = 0
        prev_key = ""
        for gc in gc_reader:
            current_key = gc['fsc_level_1'] + gc['fsc_level_4']
            if not current_key == prev_key:
                GoodsCodes.objects.update_or_create(fs_code=gc['fsc_level_1'],
                                                    fs_code_desc=gc['fsc_level_4'],
                                                    ccfta=True if gc['CFTA'] == 'YES' else False,
                                                    ccofta=True if gc['CCoFTA'] == 'YES' else False,
                                                    chfta=True if gc['CHFTA'] == 'YES' else False,
                                                    cpafta=True if gc['CPaFTA'] == 'YES' else False,
                                                    cpfta=True if gc['CPFTA'] == 'YES' else False,
                                                    ckfta=True if gc['CKFTA'] == 'YES' else False,
                                                    cufta=True if gc['CUFTA'] == 'YES' else False,
                                                    wto_agp=True if gc['WTO_AGP'] == 'YES' else False,
                                                    ceta=True if gc['CETA'] == 'YES' else False,
                                                    cptpp=True if gc['CPTPP'] == 'YES' else False)
                total += 1
            else:
                duplicates += 1
            prev_key = current_key

        print("{0} loaded, {1} duplicates".format(Fore.CYAN + str(total) + Fore.RESET, Fore.LIGHTYELLOW_EX +
                                                  str(duplicates) + Fore.RESET))


def load_construction(csv_file: str):
    with open(csv_file, 'r', encoding='utf8', errors="ignore") as txt_file:
        cc_reader = csv.DictReader(txt_file, dialect='excel')
        total = 0
        duplicates = 0
        prev_key = ""
        for cc in cc_reader:
            current_key = cc['fsc_level_3'] + cc['fsc_level_4']
            if not current_key == prev_key:
                ConstructionCodes.objects.update_or_create(fs_code=cc['fsc_level_3'],
                                                           fs_code_desc=cc['fsc_level_4'],
                                                           nafta_annex=True if cc['NAFTA'] == 'YES' else False,
                                                           ccfta=True if cc['CCFTA'] == 'YES' else False,
                                                           ccofta=True if cc['CCoFTA'] == 'YES' else False,
                                                           chfta=True if cc['CHFTA'] == 'YES' else False,
                                                           cpafta=True if cc['CPaFTA'] == 'YES' else False,
                                                           cpfta=True if cc['CPFTA'] == 'YES' else False,
                                                           ckfta=True if cc['CKFTA'] == 'YES' else False,
                                                           cufta=True if cc['CUFTA'] == 'YES' else False,
                                                           wto_agp=True if cc['WTO_AGP'] == 'YES' else False,
                                                           ceta=True if cc['CETA'] == 'YES' else False,
                                                           cptpp=True if cc['CPTPP'] == 'YES' else False
                                                           )
                total += 1
            else:
                duplicates += 1
            prev_key = current_key

        print("{0} loaded, {1} duplicates".format(Fore.CYAN + str(total) + Fore.RESET, Fore.LIGHTYELLOW_EX +
                                                          str(duplicates) + Fore.RESET))


def load_services(csv_file: str):
    with open(csv_file, 'r', encoding='utf8', errors="ignore") as txt_file:
        sc_reader = csv.DictReader(txt_file, dialect='excel')
        total = 0
        duplicates = 0
        prev_key = ""
        for sc in sc_reader:
            current_key = sc['ccs_level_1'] + sc['ccs_level_2'] + sc['ccs_level_4']
            if not current_key == prev_key:
                ServicesCodes.objects.update_or_create(
                    nafta_code=sc['ccs_level_1'],
                    ccs_level_2=sc['ccs_level_2'],
                    gsin_class=sc['ccs_level_4'],
                    desc_en="{0} - {1} - {2}".format(sc['ccs_level_1'], sc['ccs_level_2'], sc['ccs_level_4']),
                    nafta_annex=True if sc['NAFTA'] == 'YES' else False,
                    ccfta=True if sc['CCFTA'] == 'YES' else False,
                    ccofta=True if sc['CCoFTA'] == 'YES' else False,
                    chfta=True if sc['CHFTA'] == 'YES' else False,
                    cpafta=True if sc['CPaFTA'] == 'YES' else False,
                    cpfta=True if sc['CPFTA'] == 'YES' else False,
                    ckfta=True if sc['CKFTA'] == 'YES' else False,
                    cufta=True if sc['CUFTA'] == 'YES' else False,
                    wto_agp=True if sc['WTO_AGP'] == 'YES' else False,
                    ceta=True if sc['CETA'] == 'YES' else False,
                    cptpp=True if sc['CPTPP'] == 'YES' else False
                )
                total += 1
            else:
                duplicates += 1
            prev_key = current_key

        print("{0} loaded, {1} duplicates".format(Fore.CYAN + str(total) + Fore.RESET, Fore.LIGHTYELLOW_EX +
                                                          str(duplicates) + Fore.RESET))


colorama_init()
parser = argparse.ArgumentParser(description="Load data for the Trade Agreement Guide from CSV file")
parser.add_argument('--goods-csv', action='store', default='', help='Goods CSV file name', type=str)
parser.add_argument('--construction-csv', action='store', default='', help='Construction Codes CSV file name', type=str)
parser.add_argument('--services-csv', action='store', default='', help='Services codes CSV file name', type=str)

args = parser.parse_args()
if not args.goods_csv == '':
    if path.exists(args.goods_csv):
        load_goods(args.goods_csv)
    else:
        print("Cannot find file {0}{1}{2}".format(Fore.RED + Style.BRIGHT, args.goods_csv, Style.RESET_ALL))

if not args.construction_csv == '':
    if path.exists(args.construction_csv):
        load_construction(args.construction_csv)
    else:
        print("Cannot find file {0}{1}{2}".format(Fore.RED + Style.BRIGHT, args.construction_csv, Style.RESET_ALL))

if not args.services_csv == '':
    if path.exists(args.services_csv):
        load_services(args.services_csv)
    else:
        print("Cannot find file {0}{1}{2}".format(Fore.RED + Style.BRIGHT, args.services_csv, Style.RESET_ALL))