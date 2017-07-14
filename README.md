# Webhook Demo app for UCL API

View the live version here: WIP

## Running locally
- Clone this repository
- Run `yarn` to install JS dependencies
- Run `yarn dev` to build the frontend. Leave it running to watch for changes
- Start a local redis server by running `redis-server`. You must leave this running.
- Run `cp .env.example .env` and fill in the environment variables. (`NGROK_URL` can also be a URL from a similar service like localtunnel)
- Create a new python virtual environment and install python dependencies by running `pip install -r requirements.txt`
- Apply migrations with `python manage.py migrate`
- Run the server with `python manage.py runserver`
