
FROM python:3.7-alpine
LABEL org.opencontainers.image.authors="Brian Love"

# Tell Python to run in unbuffered mode; recommended when in Docker
# Don't buffer outputs - just print them directly; avoids some complications
ENV PYTHONUNBUFFERED 1

# Install our dependencies
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# Copy the contents of the app into the image
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -D means running applications only - no need for home directory
# If you don't run this, it defaults to root
RUN adduser -D user
USER user
