FROM node:14-alpine AS static_builder

RUN apk update && apk upgrade && \
    apk add --no-cache git
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./ /usr/src/app

COPY ./package.json /usr/src/app/
RUN npm install
RUN npm rebuild node-sass

ENV NODE_ENV=production
RUN npm run build

FROM python:3.8.3-alpine
# Uncomment the line above if you want to use a Dockerfile instead of templateId

RUN apk update && apk upgrade && \
    apk add --no-cache \
      make  \
      g++  \
      bash  \
      git  \
      openssh  \
      postgresql-dev \
      jpeg-dev \
      zlib-dev \
      curl

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=static_builder /usr/src/app/dist dist
COPY ./ /usr/src/app

EXPOSE 80

CMD ["runserver.sh"]
