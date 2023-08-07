# Django Rest Framework Backend template Project  using Docker

This is a Django Rest Framework template project that uses Docker to manage the development and **production** environment. Additionally, it includes configuration for Dockerizing the database.

## Prerequisites

Before starting to use this project, make sure you have the following installed on your system:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Project Folder Structure


```
├── README.md (this file)
├── .env
│   └── .django (django environment settings)
│   └── .postgres (postgres environment settings)
├── compose (general dockerfile description, aimed at development)
│   └── local
│       └── celery (celery script and settings)
│       └── Dockerfile (dockerfile for Django)
│       └── start (script for initializing Django)
│   └── Production
│     
├── core (config, files, and settings of the Django project)
│   └── __init__.py
│   └── settings (settings of the Django project)
|       └── base.py
|       └── local.py
|       └── production.py
│   └── urls.py
│   └── wsgi.py
├── manage.py (script for managing Django)
├── requirements.txt (requirements for Django)
├── docker-compose-dev.yml (docker-compose file for development)
├── docker-compose-prod.yml (docker-compose file for production)

```

## Project Configuration

1. Configure the environment variables of the project. To do this, modify the variables found in the following files:

```
    ├── .env
    │   └── .django (django enviroment settings)
    │   └── .postgres (postgres enviroment settings)
```

2. Build and start the Docker containers:

   The Django image automatically applies Django migrations and creates a superuser with the credentials that are specified in the .env/.django file.


```
    docker-compose -f docker-compose-dev.yml build
    docker-compose -f docker-compose-dev.yml up -d
```

## Usage
After configuring the project, you can access the web application in your browser at http://localhost:8001`.

To access the Django command line inside the Docker container, execute the following command:

To view the name of the Django project container:
```
docker ps
```

With the name of the Django project, run the following command:

```
docker-compose -f docker-compose-dev.yml exec -it django_container_name python manage.py shell
```

To **stop** the Docker containers, execute the following command:

```
docker-compose -f docker-compose-dev.yml build down
```


## Contribution
If you want to contribute to this project, we are open to suggestions! Simply fork the repository and send a pull request with your changes.