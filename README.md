Trade Agreement Guide - Guide des accords commerciaux

This web application helps identify which trade agreements apply when 
procuring goods.

## Setup ##

+ Setting up the database

  Follow the standard process for create models in Django 
```bash
python .\manage.py makemigrations
python .\manage.py showmigrations
python .\manage.py sqlmigrate guide 0001_initial
python .\manage.py migrate
```

+ Create an Admin User

```bash
python manage.py createsuperuser
```

### Load Data ###

From the project root directory, and after activating the virtual environment, run the
load data script
```bash
python .\load-data-from-csv.py --goods-csv .\data\ogd_goods.csv --construction-csv .\data\construction.csv --services-csv .\data\ogd_services.csv  --exceptions-csv .\data\exceptions.csv --threshold-csv .\data\thresholds.csv
```

