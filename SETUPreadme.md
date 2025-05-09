 ###### *https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-22-04*
 This project template was built from the following link which features a django project build walkthrough
 ###### *https://www.w3schools.com/django/index.php*
 Also referencing the following link
 ###### *https://www.youtube.com/watch?v=nGIg40xs9e4&t=103s*

 


# COMPONENTS OUTSIDE OF THIS APPLICATION BUILD  
I made a droplet on digital ocean (including a mysql cluster), configured SSL purchased from godaddy as well as a domain to point towards IP.    

I generated a private key configured here:  
> /etc/nginx/sites-enabled/footballproj.conf file  


# FOOTBALL DATA STUFF  
###### *source: https://pypi.org/project/nfl-data-py/#description*  
`pip install nfl_data_py`  

results in:  
> Installing collected packages: pytz, appdirs, six, numpy, fsspec, cramjam, python-dateutil, pandas, fastparquet, nfl_data_py
Successfully installed appdirs-1.4.4 cramjam-2.9.0 fastparquet-2024.11.0 fsspec-2024.10.0 nfl_data_py-0.3.3 numpy-1.26.4 pandas-1.5.3 python-dateutil-2.9.0.post0 pytz-2024.2 six-1.17.0  

###### *source: https://rapidapi.com/tank01/api/tank01-nfl-live-in-game-real-time-statistics-nfl*  
This is for the live play by play data  

I did gzip in nginx and am also using celery because some of the payload is very large  
`pip install celery`  

# Create django project
Install Django  
`python3 -m venv .venv`  
`. .venv/bin/activate`  
`python3 -m pip install Django`  


### Create project  
`django-admin startproject footballproj`  

This makes a sub directory footballproj which will be in the same folder as manage.py  
The footballproj directory will contain these files:  
> __init__.py  
> asgi.py
> settings.py  
> urls.py  
> wsgi.py  


### Create app
`py manage.py startapp fbapp`  

This makes a sub directory fbapp which will be in the same folder as manager.py, and will contain these files:  
> migrations/  
  > __init__.py  
> __init__.py  
> admin.py  
> apps.py  
> models.py  
> tests.py  
> views.py   

views.py is where all of the http requests and responses go
urls.py is where you declare the url patterns/paths

### Create template folder in fbapp
    manage.py
    footballproj/
    fbapp/
        templates/
            myfirst.html

# To run the server:  
Go to the base directory of your project  
`python3 manage.py runserver`  

Change the settings  
Go to:  
> /footballproj/settings.py

Write the name of the application in here:  

        INSTALLED_APPS = [  
            'django.contrib.admin',  
            'django.contrib.auth',  
            'django.contrib.contenttypes',  
            'django.contrib.sessions',  
            'django.contrib.messages',  
            'django.contrib.staticfiles',  
            'fbapp'  
        ] 

Run the migrate command  
`python3 manage.py migrate`   
Run the server and the html should render

# GUNICORN
###### *source: https://www.youtube.com/watch?v=Td3lirXIeRI&t=2206s*  
Inside of file .venv/bin/gunicorn_start:  

        #!/bin/bash -x
        
        export NAME='footballproj'  
        export DJANGODIR=/home/footballproj  
        export SOCKFILE=/home/footballproj/run/gunicorn.sock  
        export USER=  
        export GROUP=  
        export NUM_WORKERS=5  
        export DJANGO_SETTINGS_MODULE=footballproj.settingsprod  
        export DJANGO_WSGI_MODULE=footballproj.wsgi    
        export TIMEOUT=120    

        cd $DJANGODIR  
        source .venv/bin/activate  
        export PYTHONPATH=$DJANGODIR:$PYTHONPATH  
                
        RUNDIR=$(dirname $SOCKFILE)  
        test -d $RUNDIR || mkdir -p $RUNDIR  

        exec .venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \  
                --name $NAME \  
                --workers $NUM_WORKERS \  
                --timeout $TIMEOUT \  
                --user=$USER --group=$GROUP \  
                --bind=unix:$SOCKFILE \  
                --log-level=debug \  
                --log-file=-  

To run the file:  
`.venv/bin/gunicorn_start`  

Inside of file /etc/supervisor/conf.d/footballproj.conf:  

        [program:footballproj]  
        command = /home/footballproj/.venv/bin/gunicorn_start  
        user =   
        stderr_logfile = /home/footballproj/logs/supervisor.log  
        stdout_logfile = /home/footballproj/logs/supervisor.log  
        redirect_stderr = true  
        environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8  

To run this conf:  
`supervisorctl reread`  
`supervisorctl update`  
`supervisorctl status`  

Should print out something like this:  
> footballproj                     RUNNING   pid 35275, uptime 0:00:18  

# NGINX STUFF  
Go to sites-available and add file:  
`cd /etc/nginx/sites-available`  
`vim footballproj.conf`  

In footballproj.conf:  

        upstream footballproj_app_server {
                server unix:/home/footballproj/run/gunicorn.sock fail_timeout=0;  
        }  
        
        server {
                listen 80;  
                server_name blitz3d.net www.blitz3d.net;  
                access_log /home/footballproj/logs/access.log;  
                error_log /home/footballproj/logs/error.log;  
                return 301 https://$host$request_uri;  
        }

        server {
                listen 443 ssl;  
                server_name blitz3d.net www.blitz3d.net;  
                ssl_certificate /etc/ssl/certs/ ;  
                ssl_certificate_key /etc/ssl/private/ ;

                location /static/ {  
                        alias /home/footballproj/static/;  
                }

                location /media/ {  
                        alias /home/footballproj/media/;  
                }  
                location / {  
                        add_header 'Access-Control-Allow-Origin' 'http://www.blitz3d.net' always;  
                        add_header 'Access-Control-Allow-Credentials' 'true' always;  
                        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;  
                        add_header 'Access-Control-Allow-Headers' 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With' always;  

                        # if preflight request, we will cache it  
                        if ($request_method = 'OPTIONS') {  
                                add_header 'Access-Control-Max-Age' 1728000;  
                                add_header 'Content-Type' 'text/plain charset=UTF-8';  
                                add_header 'Content-Length' 0;  
                                return 204;  
                        }  

                        proxy_pass http://unix:/home/footballproj/run/gunicorn.sock;  
                        proxy_set_header X-Forwarded-Proto $scheme;  
                        proxy_set_header Host $host;  
                        proxy_set_header X-Real-IP $remote_addr;  
                }  
        }  


Go to sites-enabled:  
`cd /etc/nginx/sites-enabled`  
Make symbolic link:  
`ln -s ../sites-available/footballproj.conf .`  
Check that nginx will compile with no errors:  
`nginx -t`  
In /etc/nginx/nginx.conf I followed this demo. Some of the football apis have a massive payload, this is supposed to help with that latency.
###### *source: https://www.digitalocean.com/community/tutorials/how-to-improve-website-performance-using-gzip-and-nginx-on-ubuntu-20-04#step-4-verifying-the-new-configuration*  
###### *source: https://stackoverflow.com/questions/29823422/compressing-the-response-payload-in-django-rest**

While still in sites-enabled directory start nginx:  
`sudo systemctl start nginx`  



# Install dependancies
Install mysql:  
`pip install mysqlclient`  
Install bootstrap (it is easier to do links in html with this):  
###### *source: https://www.w3schools.com/django/django_add_bootstrap5.php*  
`pip install django-bootstrap-v5`  

# OPEN AI
###### *source: https://platform.openai.com/docs/api-reference/introduction*
To install open ai:  
`pip install openai`

###### *source: https://platform.openai.com/docs/quickstart*  
Create an api key on open ai and place in .env file  
> export OPEN_API_KEY=""  
###### *source: https://pypi.org/project/python-dotenv/*
Install dotenv to do environment stuff:  
`pip install python-dotenv`  

Implement open ai stuff in the views.py file


# TANK API
###### *source: https://rapidapi.com/tank01/api/tank01-nfl-live-in-game-real-time-statistics-nfl*

# IF PIP IS BEING TRASH DO THIS  
`(.venv) root@footballcscdroplet:~/footballproj# deactivate`  
`root@footballcscdroplet:~/footballproj# rm -rf .venv`  
`root@footballcscdroplet:~/footballproj# python3 -m venv .venv`  
`root@footballcscdroplet:~/footballproj# source .venv/bin/activate`  
`(.venv) root@footballcscdroplet:~/footballproj# which pip`  
results in:  
> /root/footballproj/.venv/bin/pip  

`(.venv) root@footballcscdroplet:~/footballproj# which python`  
results in:  
> /root/footballproj/.venv/bin/python  

# Extra stuff for future chat services:
###### *https://www.photondesigner.com/articles/instant-messenger?ref=rdjango-instant-messenger*  
###### *https://www.digitalocean.com/community/questions/enable-remote-redis-connection*  
###### *https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-22-04*  
###### *https://simpy.readthedocs.io/en/latest/simpy_intro/installation.html*  

