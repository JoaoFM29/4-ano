FROM python:3.12.3-slim

COPY . /var/www/project_app

WORKDIR /var/www/project_app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]