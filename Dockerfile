# Укажите базовый образ с Node.js для сборки
FROM node:20 AS build

# Установите рабочую директорию
WORKDIR /app

# Скопируйте package.json и package-lock.json (если есть)
COPY package*.json ./

# Установите зависимости
RUN npm install

# Скопируйте все остальные файлы
COPY . .

# Соберите приложение
RUN npm run build

# Укажите базовый образ для сервера (Nginx)
FROM nginx:alpine

# Скопируйте сгенерированные файлы в указанную директорию Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Установите конфигурацию Nginx (по желанию — не обязательно)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Показать порт, на котором будет работать контейнер
EXPOSE 80

# Команда для запуска Nginx
CMD ["nginx", "-g", "daemon off;"]
