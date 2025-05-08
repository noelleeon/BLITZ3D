# This project was created after making a droplet on DigitalOcean in
# the image of Ubuntu. This project also uses a hosted mysql database on
# DigitalOcean. 

### IF PIP IS BEING TRASH DO THIS
(.venv) root@footballcscdroplet:~/footballproj# deactivate
root@footballcscdroplet:~/footballproj# rm -rf .venv
root@footballcscdroplet:~/footballproj# python3 -m venv .venv
root@footballcscdroplet:~/footballproj# source .venv/bin/activate
(.venv) root@footballcscdroplet:~/footballproj# which pip
/root/footballproj/.venv/bin/pip
(.venv) root@footballcscdroplet:~/footballproj# which python
/root/footballproj/.venv/bin/python
(.venv) root@footballcscdroplet:~/footballproj# 

### Install Django
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install Django

### Create project 
django-admin startproject footballproj
(This makes a sub directory footballproj which will be in the same folder as manage.py)
(This will contain these files:
        __init__.py
        asgi.py
        settings.py
        urls.py
        wsgi.py
)

### Create app
py manage.py startapp fbapp
(this makes a sub directory fbapp which will be in the same folder as manager.py)
(This will contain these files:
        migrations/
            __init__.py
        __init__.py
        admin.py
        apps.py
        models.py
        tests.py
        views.py
)
-views.py is where all of the http requests and responses go 
-urls.py is where you declare the url patterns/paths

### Create template folder in fbapp
    manage.py
    footballproj/
    fbapp/
        templates/
            myfirst.html

### To run the server
-Go to the base folder
python3 manage.py runserver

### Change the settings
-Go to: /footballproj/settings.py
-Write the name of the application in here
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fbapp'
]
-Run the migrate command
python3 manage.py migrate
-Run the server and the html should render

### Install mysql
-Go to base folder
pip install mysql client

### ///////OPEN AI//////
source: https://platform.openai.com/docs/api-reference/introduction
### To install open ai
pip install openai
source: https://platform.openai.com/docs/quickstart
### Create an api key on open ai and place in .env file
export OPEN_API_KEY="thekey"
source: https://pypi.org/project/python-dotenv/
### Install dotenv to do environment stuff
pip install python-dotenv
### Implement open ai stuff in the views.py file
