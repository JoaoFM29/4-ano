FROM python:3.10.15-slim

# Copy the application files
COPY . /app/picturas/tools/peoplecounter

# Set the working directory
WORKDIR /app/picturas/tools/peoplecounter

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

# Install PyTorch (replace 'cpu' with 'cu118' if you have GPU support with CUDA 11.8)
RUN python -m pip install torch==2.0.0+cu118 torchvision==0.15.0+cu118 torchaudio==2.0.0 --extra-index-url https://download.pytorch.org/whl/cu118

# Install Detectron2 from the GitHub repository
RUN python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

# Install Python dependencies
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

# Set environment variables
ENV RABBITMQ_HOST=rabbitmq
ENV RABBITMQ_PORT=5672
ENV EXCHANGE=TOOLS_EXCHANGE
ENV REQUEST_QUEUE=PEOPLE_COUNTER_QUEUE
ENV RESULTS_QUEUE=RESULTS_QUEUE

ENV POOL_SIZE=1

# Set the command to run the worker
CMD ["python", "pc_worker.py"]