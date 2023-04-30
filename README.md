<h1 style="text-align: center; display: flex; flex-direction: column; align-items: center; row-gap: 16px;">
    <img src="app/log_screen/static/favicon_io/android-chrome-512x512.png" width="128">
    <span>Employee Log Screen</span>
</h1>

[![Python - 3.11](https://img.shields.io/badge/Python-3.11-2ea44f)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/nazimcanislam/employee-log-screen/blob/main/LICENSE)

User interface using Django to add staff and clients and associate projects.

## Requirements

- Python 3.11
- Django 4.1
- Pyscopg2
- PostgreSql 15
- Docker

## Running the Server

### Define Database

In order for the Django server to communicate with PostgreSql, it is necessary to write the necessary information against the fields in the `app/.env` file. If the file doesn't exist, create it.

```
DB_NAME=example_db_name
DB_USER=example_user_name
DB_PASSWORD=verysecretpassword
DB_HOST=127.0.0.1
DB_PORT=5432
```

### Creating & Running Docker Images

We can create images for development and production.

#### For Development

This command crates and runs development images with `docker-compose.dev.yml` files data.

```bash
docker-compose -f docker-compose.dev.yml up
```

#### For Production

When your `app/.env` file is ready, then run this command for creating and running image. Thanks to `-d` flag, we can run the application in background.

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Now your project is running at <a href="http://127.0.0.1:8000">127.0.0.1:8000</a>.

<h3>Creating a Super User</h3>

After stopping the application, we reach inside the container and tell Django to create a superuser.

```bash
docker-compose -f docker-compose.prod.yml run web python manage.py createsuperuser
````

- `-f` stands for file and specifies which `docker-compose` to use. Use `docker-compose.dev.yml` for development and of couse `docker-compose.prod.yml` for production.
- `web` is the Docker container name for Django application.
- After entering this command, you need to create a super user with username and password.

Now you can start docker image again!
