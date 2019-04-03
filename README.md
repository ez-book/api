# api

## Prerequisites

For this app to run, you will need to have `python3` and `psql`.

If not already installed (Python 3 should come out of the box in the latest MacOS), you can fetch them via `brew`:
```
brew install python3
brew install postgresql
```

## Installation

### Create an environment

Create a new environment with `venv`:
```
python3 -m venv venv
```

Activate the environment with:
```
. venv/bin/activate
```

### Install dependencies

Install the dependencies with `pip`:
```
pip install -r requirements.txt
```

### Copy .env.sample to .env

To set up the environment variables, copy `.env.sample` to `.env` (git-ignored):
```
cp .env.sample .env
```

## Running the app in development

To run the app in development, simply run:
```
flask run
```
> NB: `FLASK_APP` and `FLASK_ENV` are set in `.env`

As we have installed `watchdog`, the server autoreloads on code change!
