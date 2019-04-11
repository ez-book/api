# api

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

## Set up local database

### Install PostgreSQL

First, let's install PostgreSQL:
```
brew install postgresql
```

### Start the service and connect

To start the service, simply run:
```
brew services start postgresql
```

Once, the service is started, you should be able to connect to your local PostgreSQL instance via:
```
psql
```
> For more info troubleshoothing, you can refer to this [gist](https://gist.github.com/ibraheem4/ce5ccd3e4d7a65589ce84f2a3b7c23a3).

### Create dev database, user and tables

For now this process is manual, but to get started simply create a new database and some basic tables

```
CREATE DATABASE ez_book_dev;
```
```
\c ez_book_dev
```
```
CREATE TABLE itenary(id VARCHAR(50) PRIMARY KEY NOT NULL, places VARCHAR(256), url VARCHAR(256));
```

To create a new user:
```
CREATE USER testuser WITH UNENCRYPTED PASSWORD 'password';
```
```
GRANT CONNECT ON DATABASE ez_book_dev TO testuser;
```
```
GRANT USAGE ON SCHEMA public TO testuser;
```
```
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO testuser;
```

> For more CLI commands, you an check this [cheatsheet](https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546)

## Running the app in development

To run the app in development, simply run:
```
flask run
```
> NB: `FLASK_APP` and `FLASK_ENV` are set in `.env`

As we have installed `watchdog`, the server autoreloads on code change!
