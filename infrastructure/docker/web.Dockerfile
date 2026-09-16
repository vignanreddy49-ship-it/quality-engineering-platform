FROM nginx:1.27-alpine
COPY apps/web-store/index.html /usr/share/nginx/html/index.html
EXPOSE 80
