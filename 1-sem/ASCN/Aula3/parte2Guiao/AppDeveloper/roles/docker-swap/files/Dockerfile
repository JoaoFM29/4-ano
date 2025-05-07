FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    curl \
    zip \
    unzip \
    nodejs \
    npm \
    yarn \
    default-mysql-client \
    && add-apt-repository ppa:ondrej/php \
    && apt-get update && apt-get install -y \
    php7.4 php7.4-fpm php7.4-zip php7.4-mbstring php7.4-tokenizer \
    php7.4-mysql php7.4-gd php7.4-xml php7.4-bcmath php7.4-intl \
    php7.4-curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

WORKDIR /app

RUN git clone https://github.com/Hackathonners/swap.git .

# Copia os arquivos da diretoria atual para /app
COPY . .

RUN composer update
RUN composer install

RUN npm install

# Copia o arquivo .env.example para .env
RUN cp .env.example .env

RUN php artisan key:generate

# Executa o script que altera o .env
COPY script.sh /usr/local/bin/script.sh

RUN chmod +x /usr/local/bin/script.sh

EXPOSE 8000

CMD ["/usr/local/bin/script.sh"]
