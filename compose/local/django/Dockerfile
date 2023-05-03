# FROM python:3.11.3-alpine3.17

# ENV PYTHONUNBUFFERED 1

# RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories

# RUN apk update \
# && apk add g++ \
# && apk add libc-dev \
# && apk add --virtual build-deps gcc python3-dev musl-dev postgresql-dev jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev libffi-dev py-cffi gettext postgresql-client \
# && pip install --upgrade pip \
# && pip install --no-cache-dir gunicorn \
# && rm -rf /var/cache/apk/*

# # Requirements are installed here to ensure they will be cached.
# COPY ./requirements.txt ./requirements.txt
# RUN pip install --upgrade pip
# RUN pip install -r ./requirements.txt

# COPY ./compose/production/django/entrypoint /entrypoint
# RUN sed -i 's/\r//' /entrypoint
# RUN chmod +x /entrypoint

# COPY ./compose/local/django/start /start
# RUN sed -i 's/\r//' /start
# RUN chmod +x /start

# COPY ./compose/local/django/celery/worker/start /start-celeryworker
# RUN sed -i 's/\r//' /start-celeryworker
# RUN chmod +x /start-celeryworker

# COPY ./compose/local/django/celery/beat/start /start-celerybeat
# RUN sed -i 's/\r//' /start-celerybeat
# RUN chmod +x /start-celerybeat

# COPY ./compose/local/django/celery/flower/start /start-flower
# RUN sed -i 's/\r//' /start-flower
# RUN chmod +x /start-flower

# WORKDIR /app

# ENTRYPOINT ["/entrypoint"]


FROM python:3.9.16


# Install python module needed for gdal and rasterio
RUN apt-get update; \
    apt-get -y upgrade;


# fancy prompt
RUN echo 'export PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "' >> /root/.bashrc


# copy and install python dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt /tmp/
RUN python -m venv /root/env \
    && . /root/env/bin/activate \
    && pip3 install --upgrade pip \
    && pip3 install -r /tmp/requirements.txt


# # copy aws credentials
# COPY ./.aws /root/.aws


# create directory project
RUN mkdir -p /app
WORKDIR /app


# # copy and assign permissions docker-entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod u+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]