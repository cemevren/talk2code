# Stage 1: Build the React application
FROM node:latest as build-stage
WORKDIR /client

COPY . /client/
RUN yarn install
RUN yarn run build

# Stage 3: Set up Nginx
FROM nginx:alpine
COPY --from=build-stage /client/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]