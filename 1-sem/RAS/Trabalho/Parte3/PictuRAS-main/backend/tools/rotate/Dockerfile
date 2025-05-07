FROM python:3.12.3-slim

COPY . /app/picturas/tools/rotate

WORKDIR /app/picturas/tools/rotate

RUN apt update

RUN apt install ffmpeg libmagic1 libmagic-dev -y

RUN pip install -r requirements.txt

ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672

ENV EXCHANGE=TOOLS_EXCHANGE
ENV REQUEST_QUEUE=ROTATE_QUEUE

ENV POOL_SIZE=5

CMD ["python", "rotate_worker.py"]