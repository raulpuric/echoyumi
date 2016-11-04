# Explainable AI
## Integrating the Yumi robot with Amazon Echo and Alexa

To use this project, clone this repo and run the following:

```bash
sudo pip install -r requirements.txt
sudo apt-get install gnustep-gui-runtime  # For the "say" command on linux
```


Add these to your environment variables (note: this is done in alexa.py):

```bash
ALEXA_APP_IDS=("Your Amazon Alexa App ID",)  # comma separated list of app id's
ALEXA_REQUEST_VERIFICATON=true  # Enables/Disable request verification
```


To run the Django server locally and access the server externally, run the main script from any directory:
```bash
./main
```



The external url will be in the form of https://*.ngrok.io. If you want to have the external url be constant throughout restarts, upgrade to the paid ngrok plan, and replace the last command with:
```bash
./ngrok-linux-64 http -subdomain=inconshreveable 8000
```


Refreshing the homepage will add a log to the database.


To add a different background music song (WAV file only), replace song.wav in the /static and /staticfiles folders.



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
