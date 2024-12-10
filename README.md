# Project Name: backend_practice_python
## Project Description

The aim of the project is to create the back-end for a project representing a Pet Rescue,
where Users can register, search for a Pet, and adopt or foster it.


## Technologies Used

- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL


## Project Folder Structure

Source files of the project are saved under the following folder structure:

```bash
.
├── alembic/
│   ├── versions/
│   └── env.py
├── controllers/
├── infra/
│   └── docker-compose.yml
├── models/
├── scripts/
├── services/
├── utils/
├── alembic.ini
├── database.py
├── main.py
└── requirements.txt
```


## Installing the Project

The following commands are used for installing and running the project:
```bash
# start the local database
$: cd ./infra
$: docker compose up -d
✔ Container infra-local_db-1  Started
```

```bash
# create and activate a virtual environment
$: python3 -m venv .venv
$: source .venv/bin/activate
$: python3 -m pip install --upgrade pip

# install dependencies
$: pip3 install -r requirements.txt

# create your .env file
#  DATABASE_HOST=****
#  DATABASE_PORT=****
#  DATABASE_USERNAME=****
#  DATABASE_PASSWORD=****
#  DATABASE_NAME=****

# start the local (development) server
$: fastapi dev main.py
```

Upon successful start of the development server, the following logs will be printed:
```bash
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```


## Functionalities

- AUTH:
    - Register: password hashing
    - Login: Bearer Token
- CRUD:
    - Individual GET by ID
    - Querying:
        - Filtering
        - Search
        - Ordering
        - Pagination
    - Individual UPDATE and DELETE of entities
- Python Migration System


## Migration System

The migration system makes use of Python's Alembic, which uses SQLAlchemy as its underlying engine.

The commands used for creating and then applying (or reverting) a new migration are the following:
```bash
# create a new migration file
$: alembic revision -m "name of migration file"

# apply migration file
$: alembic upgrade head

# revert last migration file
$: alembic downgrade -1
```
