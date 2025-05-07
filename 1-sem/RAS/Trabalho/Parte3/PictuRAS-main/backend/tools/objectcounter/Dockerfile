FROM python:3.10.15-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    make \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/picturas/tools/objectcounter

WORKDIR /app/picturas/tools/objectcounter

# Install PyTorch (replace 'cpu' with 'cu118' if you have GPU support with CUDA 11.8)
RUN python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install Detectron2 from the GitHub repository
RUN python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Install other Python dependencies
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672

ENV EXCHANGE=TOOLS_EXCHANGE
ENV REQUEST_QUEUE=OBJECT_COUNTER_QUEUE

ENV POOL_SIZE=1

CMD ["python", "oc_worker.py"]