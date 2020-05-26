Trade Agreement Coverage Tool

THe Government of Canada is party to 12 trade agreements with government procurement chapters (eleven international and one domestic).  This permits Canadian suppliers to sell goods, services, or construction services to countries abroad and reciprocal treatment is given for foreign suppliers.  Whenever the Government of Canada considers purchasing a commodity a procurement officer must determine which trade agreements apply.  This tool was built to assist in that determination.  

Create a virtual environment
```
python3 -m venv /path/to/new/virtual/environment
```
Install requirements:
```
pip install -r requirements.txt
```
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

python manage.py dumpdata > guide/fixtures/data.json --indent 4
Create username and pasword.
Login to the application at /admin/

Populate the models with your trade agreement data.  There are 8 models.  
First enter the commodity types (Goods, Services, Construction).  Then enter the commodity codes for those commodity types.  
Enter the entities, these are the departments and agencies of the Government of Canada.

Then the limited tendering reasons, trade agreement exceptions, and Canada Free Trade Agreement exceptions.


## Use ##
The main page is /guide/en/0/ or guide/fr/0/

Populate the first page with the mandatory information.  
![mandatory_elements](https://github.com/liverms/tag_gac/blob/master/me.PNG)

A proceed through the next three optional steps.
First general exceptions:
![exceptions](https://github.com/liverms/tag_gac/blob/master/ex.PNG)

Next are the limited tendering reasons:
![limited_tendering](https://github.com/liverms/tag_gac/blob/master/lt.PNG)

Next are the CFTA exceptions:
![cfta_exceptions](https://github.com/liverms/tag_gac/blob/master/ce.PNG)

The next screen is the final screen showing the results:
![done](https://github.com/liverms/tag_gac/blob/master/done.PNG)

