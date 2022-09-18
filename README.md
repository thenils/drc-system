DRC system User auth

TO RUN THIS PROJECT:
In Linux:
    setup mysql configuration to run django project!
    https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04

after creating user and seting it up in locally add the credential to the django app.

in `setting.py`


    `'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drc',
        'USER': 'root',
        'PASSWORD': '?',
        'HOST': 'localhost',
        'PORT': 3306
    }`

change the db and pass and the host of database.

now create virtual environment for the project.
`virtualenv env` and activate env 


`pip install -r requirements.txt` use to install dependencies 

In this project i have used minimum libraries..

after installation of requirements just run 

`python manage.py runserver` in environment activated terminal

server will be running on the default port 8000 and the url: http://localhost:8000