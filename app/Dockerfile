
FROM nginx:stable-alpine3.24

RUN apk upgrade --no-cache

COPY index.html /usr/share/nginx/html/index.html
COPY nginx-security.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

