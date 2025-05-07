FROM python:3.12.3-slim

COPY . /var/www/users_app

WORKDIR /var/www/users_app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]