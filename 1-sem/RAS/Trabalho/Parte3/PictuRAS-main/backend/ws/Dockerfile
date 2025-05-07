FROM python:3.12.3-slim

COPY . /var/www/ws

WORKDIR /var/www/ws

RUN pip install -r requirements.txt

CMD ["python", "ws.py"]