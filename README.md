# This project template was built from the following link which features a django project build walkthrough
# https://www.w3schools.com/django/index.php
# Also referencing the following link
# https://www.youtube.com/watch?v=nGIg40xs9e4&t=103s

# This project was created after making a droplet on DigitalOcean in
# the image of Ubuntu. This project also uses a hosted mysql database on
# DigitalOcean. This project was made on ubuntu by ssh into the ip address
# produced by the DigitalOcean droplet.



# IF PIP IS BEING TRASH DO THIS
(.venv) root@footballcscdroplet:~/footballproj# deactivate
root@footballcscdroplet:~/footballproj# rm -rf .venv
root@footballcscdroplet:~/footballproj# python3 -m venv .venv
root@footballcscdroplet:~/footballproj# source .venv/bin/activate
(.venv) root@footballcscdroplet:~/footballproj# which pip
/root/footballproj/.venv/bin/pip
(.venv) root@footballcscdroplet:~/footballproj# which python
/root/footballproj/.venv/bin/python
(.venv) root@footballcscdroplet:~/footballproj# 

# /////////GITHUB/////////////
git init
git add .
git commit -m "your message"
git branch -M main
git remote add origin git remote add origin https://noelleeon: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@github.com/noelleeon/footballcsc.git
git push -u origin main --force

# Install Djangoi
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install Django

# Create project 
django-admin startproject footballproj
(This makes a sub directory footballproj which will be in the same folder as manage.py)
(This will contain these files:
        __init__.py
        asgi.py
        settings.py
        urls.py
        wsgi.py
)

# Create app
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

# Create template folder in fbapp
    manage.py
    footballproj/
    fbapp/
        templates/
            myfirst.html

# To run the server
-Go to the base folder
python3 manage.py runserver

# Change the settings
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

# Install mysql
-Go to base folder
pip install mysql client

# ///////OPEN AI//////
source: https://platform.openai.com/docs/api-reference/introduction
# To install open ai
pip install openai
source: https://platform.openai.com/docs/quickstart
# Create an api key on open ai and place in .env file
export OPEN_API_KEY="thekey"
source: https://pypi.org/project/python-dotenv/
# Install dotenv to do environment stuff
pip install python-dotenv
# Implement open ai stuff in the views.py file


# ////////LIVE CHAT COMPONENTS////////
source: https://www.geeksforgeeks.org/realtime-chat-app-using-django/
-From 4.0.0 on of channels you need daphne
pip install -U channels
pip install -U daphne
-Add channels and daphne to installed apps in settings.py
-Add this to asgi.py file
import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "footballproj.settings")
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
})

ASGI_APPLICATION = 'footballproj.asgi.application'

-Make sure docker is installed
-start a docker daemon
sudo systemctl start docker
