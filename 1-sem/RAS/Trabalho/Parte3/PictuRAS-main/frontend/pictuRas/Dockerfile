FROM node:23-alpine3.20 AS build


WORKDIR /app

COPY package*.json ./

COPY .env.example .env

RUN npm install

COPY . ./

RUN npm run build

FROM nginx:stable-alpine AS production

COPY --from=build /app/nginx /etc/nginx/conf.d

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 90

CMD ["nginx", "-g", "daemon off;"]
