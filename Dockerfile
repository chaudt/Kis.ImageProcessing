FROM continuumio/miniconda3
WORKDIR /app

#COPY ./cameras/camera_config.py ./cameras/
COPY enviroment.yml .
RUN conda env create -f enviroment.yml
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

SHELL ["conda", "run", "-n", "removebg_env", "/bin/bash", "-c"]

COPY main_v2.py .
COPY latest.pth .
ENV DATA_DIR=/data
RUN mkdir -p "$DATA_DIR"
ENTRYPOINT  ["conda", "run", "--no-capture-output", "-n", "removebg_env", "python", "main_v2.py"] 

# để build 1 image: docker build -t <python-imagename> .
# để chạy image: docker run <python-imagename>