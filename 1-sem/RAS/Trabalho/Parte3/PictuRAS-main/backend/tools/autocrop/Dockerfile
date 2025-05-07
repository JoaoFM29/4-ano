FROM python:3.12.3-slim

COPY . /app/picturas/tools/autocrop

WORKDIR /app/picturas/tools/autocrop

RUN apt update

RUN apt install libmagic1 libmagic-dev wget -y

RUN mkdir -p /root/.u2net

RUN wget -O /root/.u2net/u2net.onnx https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx

RUN pip install -r requirements.txt

ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672

ENV EXCHANGE=TOOLS_EXCHANGE
ENV REQUEST_QUEUE=AUTOCROP_QUEUE

ENV POOL_SIZE=1

CMD ["python", "autocrop_worker.py"]