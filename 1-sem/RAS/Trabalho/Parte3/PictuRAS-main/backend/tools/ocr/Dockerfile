FROM python:3.12.3-slim

COPY . /app/picturas/tools/ocr

WORKDIR /app/picturas/tools/ocr

RUN apt update

RUN apt install tesseract-ocr -y

RUN pip install -r requirements.txt

ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672

ENV EXCHANGE=TOOLS_EXCHANGE
ENV REQUEST_QUEUE=OCR_QUEUE

ENV POOL_SIZE=5

CMD ["python", "ocr_worker.py"]