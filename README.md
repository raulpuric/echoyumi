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
python manage.py runserver 0.0.0.0:443
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
