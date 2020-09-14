# Trade Agreement Determination Tool

The Government of Canada is party to 12 trade agreements with government procurement chapters (eleven international and one domestic).  This permits Canadian suppliers to sell goods, services, or construction services to countries abroad and reciprocal treatment is given for foreign suppliers.  Whenever the Government of Canada considers purchasing a commodity a procurement officer must determine which trade agreements apply.  This tool was built to assist in that determination.  

## Setup ##
Create a virtual environment
```
python3 -m venv /path/to/new/virtual/environment
```
Install requirements:
```
pip install -r requirements.txt
```

+ Setting up the database

  Follow the standard process for create models in Django 

```
python manage.py makemigrations
python manage.py showmigrations
python manage.py sqlmigrate guide 0001_initial
python manage.py migrate
```

+ This repo includes dummy data to test

```
python manage.py loaddata guide/fixtures/db.json
```

+ Create an Admin User

```
python manage.py createsuperuser
```

++ Create username and pasword.
++ Login to the application at /admin/

+ Populate Models
++ There are instructions on the admin page to help you load models.


## Demo ##
The main page is /tag/form/0/ 

Populate the first page with the mandatory information.  

![The first page contains from mandatory information about the procurement](gifs/me.gif)


![The next step is to select any general exceptions, if any, which apply](gifs/ge.gif)


![The next step is to select any CFTA-specific exceptions, if any, which apply](gifs/cfta.gif)

![The next step is the limited tendering reasons, select any which apply](gifs/lt.gif)

![The last screen shows the final results indicating which trade agreements may apply](gifs/done.gif)

## Create Fixtures

+ After creating your down data you can create your own fixture:

```
python manage.py dumpdata guide > guide/fixtures/db.json
```
