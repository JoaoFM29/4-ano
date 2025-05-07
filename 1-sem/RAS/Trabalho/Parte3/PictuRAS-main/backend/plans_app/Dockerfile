FROM python:3.12.3-slim

COPY . /var/www/plans_app

WORKDIR /var/www/plans_app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]