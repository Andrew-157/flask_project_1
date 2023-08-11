Flask Project 'Asklee'

### Usage

`Asklee` allows users to ask any question they want and let other users help them find the answer. Users can provide details and tags for their questions. Both questions and answers can be voted as useful or not useful. Also users can search for questions through tags or just entering some text in search bar.

### Technologies

* `Flask`
* `MySQL`
* `Bootstrap5`

### Project Structure

`Asklee` uses `Flask`'s 'blueprints' and 'application factory'. For running migrations and writing queries were used `Flask-Migrate` and `Flask-SQLAlchemy`, respectively. For managing authentication `Flask-Login` was used. `CSRF`-protection was enabled with `Flask-WTF`.

`Asklee` has two blueprints:
* main
* auth

`main` blueprint manages creating of questions and answers, as well as voting for them. Authenticated user that created question or answer can update it and delete it. There are also two pages for each authenticated user: personal(see only by user) and public(seen by any user). All users(non-authenticated too) can read questions, answers and search for them.

`auth` blueprint manages registration, login and logout. Also this app manages operation of changing
users' info(username and email).

### Installation

To work with this project you need Python3.9+ installed on your machine

If you do not have Python installed, visit official documentation and install it: https://www.python.org/downloads/

Clone repository, using command:
```
    git clone https://github.com/Andrew-157/flask_project_1
```
and go into directory 'flask_project_1'.

**Everything shown below assumes you are working from directory 'dj_project_3'**

Requirements:
```
    Flask==2.3.2
    Flask-SQLAlchemy==3.0.5
    python-dotenv==1.0.0
    Flask-Migrate==4.0.4
    Flask-Login==0.6.2
    mysqlclient==2.2.0
    Flask-WTF==1.1.1
    pytest==7.4.0
    autopep8==2.0.2
```

If you are using pipenv,run in the command line from directory where Pipfile is located:
```
    pipenv install
```

To activate environment using pipenv, run in the command line in the same directory:
```
    pipenv shell
```

You can also use file `requirements.txt` with pip.
Inside your activated virtual environment, run:
```
    pip install -r requirements.txt
```
For `Windows`
```
    pip3 install -r requirements.txt
```
For `Unix`-based systems

### Run project

**The following steps show how to run project locally(i.e., with development configuration will be used)**

Generate secret key, using the following code:
```python
    import secrets

    secret_key = secrets.token_hex(32)

    print(secret_key)
```

In root directory of the project create file .env(**do not forget to add it to .gitignore, if it is not there**) and add the following line:
```
    SECRET_KEY=<secret_key_you_generated>
```

Then you need to create MySQL database(using MySQL Workbench or any other tool), using SQL statement:
```SQL
    CREATE DATABASE <your_database_name>;
```

Next, go to .env and using credentials of your database, add the following lines:
```
    DB_NAME=<your_database_name>
    DB_USER=<your_database_user>
    DB_PASSWORD=<your_database_password>
    DB_PORT=<your_database_port>
    DB_HOST=<your_database_host>
```

After that, in command line run:
```
    python manage.py migrate
    python manage.py runserver
```

Go to your browser at the address: 'http://127.0.0.1:5000/', you should be able to see `Asklee`'s index page.

### Testing

`Asklee` uses `Python`'s module `pytest` for running tests. All test modules as well as 'conftest.py' are
in directory 'tests'. In 'conftest.py' you can find some `fixtures` used by tests.

To run all tests, in command line run:
```
    pytest
```

To run particular module, run:
```
    pytest tests/test_auth.py
```

To run particular test in a module, run:
```
    pytest tests/test_auth.py::test_register 
``` 