FROM python:3.12.3-slim

COPY . /app/picturas/tools/watermark

WORKDIR /app/picturas/tools/watermark

RUN apt update

RUN apt install libmagic1 libmagic-dev -y

RUN pip install -r requirements.txt

ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672

ENV EXCHANGE=TOOLS_EXCHANGE
ENV REQUEST_QUEUE=WATERMARK_QUEUE
ENV WATERMARK_IMAGE_PATH=watermark.png

ENV POOL_SIZE=5

CMD ["python", "watermark_worker.py"]