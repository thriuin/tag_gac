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

From the project root directory, and after activating the virtual environment, load the data from fixtures
```
python .\manage.py loaddata guide/fixtures/data.json

To create fixture file:
python .\manage.py dumpdata --output guide/fixtures/data.json
```

