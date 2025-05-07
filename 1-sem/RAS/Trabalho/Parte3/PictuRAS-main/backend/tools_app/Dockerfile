FROM python:3.12.3-slim

COPY . /var/www/tools_app

WORKDIR /var/www/tools_app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]