FROM python:3.12.3-slim

COPY . /var/www/wsgateway

WORKDIR /var/www/wsgateway

EXPOSE 8764

RUN pip install -r requirements.txt

CMD ["python", "server.py"]