## A Django Rest Framewokr project template for a RESTful Application using Docker

Este es un proyecto de plantilla de Django Rest Framework que utiliza Docker para manejar el entorno de desarrollo y **producción**. Además, también se incluye una configuración para Dockerizar la base de datos.

## Requisitos previos

Antes de comenzar a utilizar este proyecto, asegúrese de tener instalado lo siguiente en su sistema:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Tree folder structure of project
```
    ├── README.md (this file)
    ├── .env
    │   └── .django (django enviroment settings)
    │   └── .postgres (postgres enviroment settings)
    ├── compose (general dockerfile description, aimed at development)
    │   └── local
    │       └── celery (celery script and settings)
    │       └── Dockerfile (dockerfile for Django)
    │       └── start (script for initialize Django)
    │   └── Production
    │     
    ├── core (config, files and settings of project Django)
    │   └── __init__.py
    │   └── settings (settings of project Django)
    |       └── base.py
    |       └── local.py
    |       └── production.py
    │   └── urls.py
    │   └── wsgi.py
    ├── manage.py (script for manage Django)
    ├── requirements.txt (requirements for Django)
    ├── docker-compose-dev.yml (docker-compose file for development)
    ├── docker-compose-prod.yml (docker-compose file for production)

```

## Configuración del proyecto

1. Configurar las variales de entorno del proyecto. Para ello, se debe modificar las variables que se encuentran en los siguientes archivos:
```
    ├── .env
    │   └── .django (django enviroment settings)
    │   └── .postgres (postgres enviroment settings)
```

2. Construye e inicia los contenedores de Docker:
    La imagen de django aplica automáticamente las migraciones de Django y crea un super usuariro con las credenciales que se encuentran en el archivo .env/.django

```
    docker-compose -f docker-compose-dev.yml build
    docker-compose -f docker-compose-dev.yml up -d
```

## Uso del proyecto

Después de configurar el proyecto, puede acceder a la aplicación web en su navegador en la dirección `http://localhost:8001`.

Para acceder a la línea de comandos de Django dentro del contenedor de Docker, ejecute el siguiente comando:

Para ver el nombre del contenedor del proyecto de Django:
```
docker ps
```

Con el nombre del proyecto de Django, ejecutar el siguiente comando:

```
docker-compose -f docker-compose-dev.yml exec -it django_container_name python manage.py shell
```

Para **detener** los contenedores de Docker, ejecute el siguiente comando:

```
docker-compose -f docker-compose-dev.yml build down
```


## Contribución

Si desea contribuir a este proyecto, ¡estamos abiertos a sugerencias! Simplemente haga un fork del repositorio y envíe una pull request con sus cambios.