FROM python:3.11.3-alpine3.17

ENV PYTHONUNBUFFERED 1

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories

RUN apk update \
&& apk add g++ \
&& apk add libc-dev \
&& apk add --virtual build-deps gcc python3-dev musl-dev postgresql-dev jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev libffi-dev py-cffi gettext postgresql-client \
&& pip install --upgrade pip \
&& pip install --no-cache-dir gunicorn \
&& rm -rf /var/cache/apk/*

# # Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements/base.txt

# we will install separately the requirements to avoid
# having to install all the packages from scratch in case of having a new library
RUN pip install --no-cache-dir -r /requirements/local.txt

# "RUN sed -i 's/\r//' /entrypoint", utiliza el comando "sed"
#  para eliminar los caracteres de retorno de carro (representados por "\r") del archivo
#  "/entrypoint". Esto se hace porque los archivos pueden tener diferentes formatos de final
#  de línea según el sistema operativo, y es posible que el archivo "entrypoint" tenga estos
#  caracteres que pueden causar problemas en la ejecución del script.
COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

WORKDIR /app

ENTRYPOINT ["/entrypoint"]