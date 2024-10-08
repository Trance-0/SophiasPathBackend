# pull official base image
FROM python:3.9.18-bullseye as builder

# configurations
ENV HOME=/home
ENV APP_HOME=/home/spbackend
ENV PRODUCTION_MEDIA_ROOT=/home/mediafiles
ENV PRODUCTION_STATIC_ROOT=/home/staticfiles
RUN mkdir ${APP_HOME}

# install dependencies
WORKDIR $HOME 
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

# copy files
WORKDIR ${APP_HOME}
COPY . . 
# remove existing env file
RUN rm ${APP_HOME}/.env
# copy production env file to app dir and root dir
COPY ./.env.prod ${APP_HOME}/.env
COPY ./.env.prod /.env

# add entrypoint to root
ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh 

# create the appropriate directories for static and media file (nginx)
# nginx only process medias and should not be exposed.
RUN mkdir $HOME/staticfiles
RUN mkdir $HOME/mediafiles

# copy developing file to target location (collect static passively)
RUN python ${APP_HOME}/manage.py collectstatic --noinput
COPY ./productionfiles ${PRODUCTION_STATIC_ROOT}
COPY ./media ${PRODUCTION_MEDIA_ROOT}

# change file permission
RUN chmod -R a+x ${PRODUCTION_STATIC_ROOT}
RUN chmod -R a+x ${PRODUCTION_MEDIA_ROOT}
# the safer version as below
# RUN chown -R www-data:www-data ${HOME}/staticfiles
# RUN chown -R www-data:www-data ${HOME}/mediafiles

# netcat for database server testing
RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]