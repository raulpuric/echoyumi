# Explainable AI
## Integrating the Yumi robot with Amazon Echo and Alexa

To use this project, clone this repo and run the following:

```bash
sudo pip install requests
sudo pip install Django==1.10.1
sudo pip install django-alexa
```


Add these to your environment variables:

```bash
ALEXA_APP_IDS = ("Your Amazon Alexa App ID",)  # comma separated list of app id's
ALEXA_REQUEST_VERIFICATON = True  # Enables/Disable request verification
```


To run the Django server:

```bash
python manage.py runserver 0.0.0.0:443
```


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
