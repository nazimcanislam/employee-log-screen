# <img src="log_screen/static/favicon_io/favicon-32x32.png"> Employee Log Screen

User interface using Django to add staff and clients and associate projects.

## Requirements

- Python 3.11
- Django 4.1
- Pyscopg2
- PostgreSql 15

## Running the Server

### Define Database

In order for the Django server to communicate with PostgreSql, it is necessary to write the necessary information against the fields in the `.env` file.

```
DB_NAME=example_db_name
DB_USER=example_user_name
DB_PASSWORD=verysecretpassword
DB_HOST=127.0.0.1
DB_PORT=5432
```

### Create Virtual Environment for Python

Let's create a virtual environment for Django and other necessary libraries...

```bash
python3 -m virtualenv venv
```

Let's run the virtual environment (Windows)

```powershell
.\venv\Scripts\activate.bat
```

Let's run the virtual environment (Unix)

```bash
./venv/bin/activate
```

Let's install the necessary libraries...

```bash
pip install -r requirements.txt
```

### Approve Database Tables

The codes we will write to validate the models of our Django project...

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

### Creating a Super User

We need a superuser to be able to use the app. We can create our superuser with Django's command line.

```bash
python manage.py createsuperuser
```

### Start the Server

The code we will run in the project folder...

```bash
python manage.py runserver
```

Now your project is running at <a href="http://127.0.0.1:8000">127.0.0.1:8000</a>.
