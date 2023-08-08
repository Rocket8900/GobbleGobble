"Heaps final submission"

Gobble Gobble food app. 
Deployed and accessible here: https://gobblegobble-33452308dd78.herokuapp.com/

Using aws rds for hosting of postgreSQL db, aws s3 buckets for handling of static files and heroku for hosting of the django and backend. 

Gobble Gobble is a food app that is meant to simplify the process of finding somewhere fun to eat. It does this in two different ways 

Community search:
This is a pre filled out database which allows you to search through the different food places set by the gobble gobble team. It includes a map with reference and a description along with categories. 

My list: 
Create an account first through the usage of django authentication and sendgrid for email verification. After creating an account, you are then able to input your own places which only you will be able to view. Furthermore, you are able to add in any places in the community search into your own private list with just a simple click of a button. 


In order to run this code: 
1) Creatè a virtual environment

2) Install all the required libraries through pip install -r requirements.txt

3) Install QGIS to process spatial data: https://www.qgis.org/en/site/forusers/download.html

4) run the django file using python manage.py runserver (wont be able to run without getting in the necessary secret codes)
