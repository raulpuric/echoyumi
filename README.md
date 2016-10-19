# Explainable AI
## Integrating the Yumi robot with Amazon Echo and Alexa

To use this project, clone this repo and run the following:

```bash
sudo pip install requests
sudo pip install Django==1.10.1
sudo pip install django-alexa
```


Add these to your environment variables (note: this is done in alexa.py):

```bash
ALEXA_APP_IDS=("Your Amazon Alexa App ID",)  # comma separated list of app id's
ALEXA_REQUEST_VERIFICATON=true  # Enables/Disable request verification
```


To run the Django server:

```bash
python manage.py runserver
```


After running that locally, you can access the server externally by running (in 2 different terminals):
```bash
python manage.py runserver
./ngrok-linux-64 http 8000
```

The external url will be in the form of https://*.ngrok.io. If you want to have the external url be constant throughout restarts, upgrade to the paid ngrok plan, and replace the last command with:
```bash
./ngrok-linux-64 http -subdomain=inconshreveable 8000
```


Our server is hosted on heroku:
```
https://explainable-ai.herokuapp.com
```

Refreshing the homepage will add a log to the database.


To add a different background music mp3 song, run the following:
```
brew install ffmpeg
lame -b 32 --resample 24 -m m your_song.mp3 song.mp3
```
Open up the file in a text editor, like Sublime, and delete all the bytes before the first "0xff 0xf3" bytes.
Then put song.mp3 into the /static and /staticfiles folder.



## Helpful Links
Alexa
* https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/overviews/understanding-custom-skills
* https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-web-service
* https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/deploying-a-sample-skill-as-a-web-service
* https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-interface-reference
* https://github.com/amzn/alexa-skills-kit-js
* https://github.com/matt-kruse/alexa-app
* https://github.com/matt-kruse/alexa-app-server

Server
* https://github.com/rocktavious/django-alexa
* https://pypi.python.org/pypi/django-alexa/0.0.3

## Reminders

* Change SECRET_KEY in settings.py if using this in a production application.
* Put all static files in the 'static' directory. Heroku will compile these static files and other Django static files into the 'staticfiles' directory, which will be overwritten everytime we push!





ALEXA_APP_ID_='amzn1.ask.skill.7a5f78a8-7bad-4540-a6b3-425f1f206da6'
ALEXA_APP_ID_YUMI='amzn1.ask.skill.7a5f78a8-7bad-4540-a6b3-425f1f206da6'
ALEXA_APP_IDS='amzn1.ask.skill.7a5f78a8-7bad-4540-a6b3-425f1f206da6'
ALEXA_REQUEST_VERIFICATON=True
DJANGO_SETTINGS_MODULE='echoyumi.settings'
