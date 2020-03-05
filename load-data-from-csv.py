
import argparse
from colorama import Fore, init as colorama_init, Style
import csv
from os import  environ, path
import sys

# Use the database models from Django
environ.setdefault('DJANGO_SETTINGS_MODULE', 'tag_gac.settings')
import django
django.setup()
from guide.models import GoodsCode, ConstructionCode, ServicesCode, TAException, ValueThreshold, LimitedTendering


def load_goods(csv_file: str):
    with open(csv_file, 'r', encoding='utf8', errors="ignore") as txt_file:
        gc_reader = csv.DictReader(txt_file, dialect='excel')
        total = 0
        duplicates = 0
        prev_key = ""
        for gc in gc_reader:
            current_key = gc['fsc_level_1'] + gc['fsc_level_4']
            if not current_key == prev_key:
                GoodsCode.objects.update_or_create(fs_code=gc['fsc_level_1'],
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

        print("Goods Codes: {0} loaded, {1} duplicates".format(Fore.CYAN + str(total) + Fore.RESET, Fore.LIGHTYELLOW_EX +
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
                ConstructionCode.objects.update_or_create(fs_code=cc['fsc_level_3'],
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

        print("Construction Codes: {0} loaded, {1} duplicates".format(Fore.CYAN + str(total) + Fore.RESET, Fore.LIGHTYELLOW_EX +
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
                # YES means the good is exempt under the trade agreement
                ServicesCode.objects.update_or_create(
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

        print("Services Codes: {0} loaded, {1} duplicates".format(Fore.CYAN + str(total) + Fore.RESET, Fore.LIGHTYELLOW_EX +
                                                          str(duplicates) + Fore.RESET))


def load_exceptions(csv_file: str):
    with open(csv_file, 'r', encoding='utf8', errors="ignore") as txt_file:
        ex_reader = csv.DictReader(txt_file, dialect='excel')
        total = 0
        for ex in ex_reader:
            TAException.objects.update_or_create(
                desc_en=ex['Exceptions'],
                desc_fr=ex['Exceptions'],
                nafta_annex=True if ex['NAFTA'] == 'Exempt' else False,
                ccfta=True if ex['CCFTA'] == 'Exempt' else False,
                ccofta=True if ex['CCoFTA'] == 'Exempt' else False,
                chfta=True if ex['CHFTA'] == 'Exempt' else False,
                cpafta=True if ex['CPaFTA'] == 'Exempt' else False,
                cpfta=True if ex['CPFTA'] == 'Exempt' else False,
                ckfta=True if ex['CKFTA'] == 'Exempt' else False,
                cufta=True if ex['CUFTA'] == 'Exempt' else False,
                wto_agp=True if ex['WTO_AGP'] == 'Exempt' else False,
                ceta=True if ex['CETA'] == 'Exempt' else False,
                cptpp=True if ex['CPTPP'] == 'Exempt' else False
            )
            total += 1

        print("Exceptions: {0} loaded".format(Fore.CYAN + str(total) + Fore.RESET))


def load_dollar_thresholds(csv_file: str):
    with open(csv_file, 'r', encoding='utf8', errors="ignore") as txt_file:
        value_reader = csv.DictReader(txt_file, dialect='excel')
        total = 0
        for vt in value_reader:
            ValueThreshold.objects.update_or_create(
                desc_en=vt['Type'],
                desc_fr=vt['Type'],
                nafta=vt['NAFTA'],
                ccfta=vt['CCFTA'],
                ccofta=vt['CCoFTA'],
                chfta=vt['CHFTA'],
                cpafta=vt['CPaFTA'],
                cpfta=vt['CPFTA'],
                ckfta=vt['CKFTA'],
                cufta=vt['CUFTA'],
                wto_agp=vt['WTO_AGP'],
                ceta=vt['CETA'],
                cptpp=vt['CPTPP'],
            )
            total += 1

        print("Thresholds: {0} loaded".format(Fore.CYAN + str(total) + Fore.RESET))


def load_limited_tendering(csv_file: str):
    with open (csv_file, 'r', encoding='utf8', errors="ignore") as txt_file:
        ltr_reader = csv.DictReader(txt_file, dialect='excel')
        total = 0
        ta_urls_en = {}
        for ltr in ltr_reader:
            if ltr['Data Field'] == 'URL':
                ta_urls_en['CFTA Article 513'] = ltr['CFTA Article 513']
                ta_urls_en['NAFTA Article 1016'] = ltr['NAFTA Article 1016']
                ta_urls_en['Chile (CCFTA) Article Kbis-09'] = ltr['Chile (CCFTA) Article Kbis-09']
                ta_urls_en['Colombia (CCoFTA) Article 1409'] = ltr['Colombia (CCoFTA) Article 1409']
                ta_urls_en['Honduras (CHFTA) Article 17.11'] = ltr['Honduras (CHFTA) Article 17.11']
                ta_urls_en['Panama (CPaFTA) Article 16.10'] = ltr['Panama (CPaFTA) Article 16.10']
                ta_urls_en['Korea (CKFTA) Article 14.3 (WTO) '] = ltr['Korea (CKFTA) Article 14.3 (WTO) ']
                ta_urls_en['Peru (CPFTA) Article 1409'] = ltr['Peru (CPFTA) Article 1409']
                ta_urls_en['WTO-AGP Article XV'] = ltr['WTO-AGP Article XV']
                ta_urls_en['CETA 19.12'] = ltr['CETA 19.12']
                ta_urls_en['CPTPP  Article 15.10 (2)'] = ltr['CPTPP  Article 15.10 (2)']
            else:
                LimitedTendering.objects.update_or_create(
                    title_en=ltr['Data Field'],
                    title_fr=ltr['Data Field'],
                    nafta=ltr['NAFTA Article 1016'],
                    ccfta=ltr['Chile (CCFTA) Article Kbis-09'],
                    ccofta=ltr['Colombia (CCoFTA) Article 1409'],
                    chfta=ltr['Honduras (CHFTA) Article 17.11'],
                    cpafta=ltr['Panama (CPaFTA) Article 16.10'],
                    cpfta='',
                    ckfta='',
                    cufta='',
                    wto_agp=ltr['WTO-AGP Article XV'],
                    ceta=ltr['CETA 19.12'],
                    cptpp=ltr['CPTPP  Article 15.10 (2)'],
                    cfta=ltr['CFTA Article 513']
                )
                total += 1

        print("Limited Tendering Reasons: {0} loaded".format(Fore.CYAN + str(total) + Fore.RESET))

colorama_init()
parser = argparse.ArgumentParser(description="Load data for the Trade Agreement Guide from CSV file")
parser.add_argument('--goods-csv', action='store', default='', help='Goods CSV file name', type=str)
parser.add_argument('--construction-csv', action='store', default='', help='Construction Codes CSV file name', type=str)
parser.add_argument('--services-csv', action='store', default='', help='Services codes CSV file name', type=str)
parser.add_argument('--exceptions-csv', action='store', default='', help='Exception Reasons CSV file name', type=str)
parser.add_argument('--threshold-csv', action='store', default='', help='Value Thresholds CSV file name', type=str)
parser.add_argument('--tendering-csv', action='store', default='', help='Limited Tendering Reasons CSV file name', type=str)

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

if not args.exceptions_csv == '':
    if path.exists(args.exceptions_csv):
        load_exceptions(args.exceptions_csv)
    else:
        print("Cannot find file {0}{1}{2}".format(Fore.RED + Style.BRIGHT, args.exceptions_csv, Style.RESET_ALL))

if not args.threshold_csv == '':
    if path.exists(args.threshold_csv):
        load_dollar_thresholds(args.threshold_csv)
    else:
        print("Cannot find file {0}{1}{2}".format(Fore.RED + Style.BRIGHT, args.threshold_csv, Style.RESET_ALL))

if not args.tendering_csv == '':
    if path.exists(args.tendering_csv):
        load_limited_tendering(args.tendering_csv)
    else:
        print("Cannot find file {0}{1}{2}".format(Fore.RED + Style.BRIGHT, args.tendering_csv, Style.RESET_ALL))