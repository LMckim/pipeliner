# Pipeliner
A very simple asynchronous application to show some operations like pulling from an API and string in formats such as Excel (`.xlsx`) and storing within a database

## Install
Simply run `pipenv install` (if `pipenv` is not install do so via 'pip install pipenv' in your global environment)

## Running
### Environment
Store these variables within a `.env` file in the root directory of the project
```bash
PG_HOST=<host>
PG_USER=<username>
PG_PASS=<password>
PG_DBNAME=<dbname>
PG_PORT=5432

TWELVEDATA_KEY=<key>
SYMBOLS=<comma-seperated-symbols>
```
Run either `pipenv run main.py` or `python main.py` if you're within the venv. The application
will pull the symbol data and write it to an Excel file and then attempt to connect to the specified database, if it cannot it will throw an Exception.


