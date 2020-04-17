Trade Agreement Coverage Tool

THe Government of Canada is party to 12 trade agreements with government procurement chapters (eleven international and one domestic).  This permits Canadian suppliers to sell goods, services, or construction services to countries abroad and reciprocal treatment is given for foreign suppliers.  Whenever the Government of Canada considers purchasing a commodity a procurement officer must determine which trade agreements apply.  This tool was built to assist in that determination.  

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
Create username and pasword.
Login to the application at /admin/

Populate the models with your trade agreement data.

## Use ##
The main page is /guide/en/0/ or guide/fr/0/

Populate the first page with the mandatory information.  
A proceed through the next three optional steps.
Upon submitting the final form the user will be presented with guidance on trade agreement applicability.
