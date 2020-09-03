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


## Use ##
The main page is /tag/form/0/ 

Populate the first page with the mandatory information.  
![mandatory_elements](https://github.com/liverms/tag_gac/blob/master/gifs/me.PNG)

A proceed through the next three optional steps.
First general exceptions:
![exceptions](https://github.com/liverms/tag_gac/blob/master/gifs/ge.PNG)

Next are the CFTA exceptions:
![cfta_exceptions](https://github.com/liverms/tag_gac/blob/master/gifs/cfta.PNG)

Next are the limited tendering reasons:
![limited_tendering](https://github.com/liverms/tag_gac/blob/master/gifs/lt.PNG)

The next screen is the final screen showing the results:
![done](https://github.com/liverms/tag_gac/blob/master/gifs/done.PNG)

## Create Fixtures

+ After creating your down data you can create your own fixture:

```
python manage.py dumpdata guide > guide/fixtures/db.json
```
