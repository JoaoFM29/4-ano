FROM python:3.12.3-slim

COPY . /var/www/images_app

WORKDIR /var/www/images_app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]