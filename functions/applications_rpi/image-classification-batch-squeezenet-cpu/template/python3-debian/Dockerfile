FROM openfaas/classic-watchdog:0.18.18 as watchdog
FROM python:3.7

# Allows you to add additional packages via build-arg
ARG ADDITIONAL_PACKAGE

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog
RUN apt-get update \
    && apt-get install -y ca-certificates ${ADDITIONAL_PACKAGE} \
    && rm -rf /var/lib/apt/lists/

# Add non root user
RUN groupadd app && useradd -r -g app app

WORKDIR /home/app/

COPY index.py           .
COPY requirements.txt   .
COPY imagenet_classes.txt .

RUN chown -R app /home/app && \
    mkdir -p /home/app/python && chown -R app /home/app

USER root
RUN apt-get update && apt-get upgrade -y && apt-get install -y build-essential \
    python3-future \
    python3-numpy \
    python3-wheel \
    python3-setuptools \
    python3-requests \
    python3-pillow \ 
    python3-yaml \ 
    python3-six \  
    wget \ 
    curl

RUN wget https://mathinf.eu/pytorch/arm64/torch-1.6.0a0+b31f58d-cp37-cp37m-linux_aarch64.whl
RUN wget https://mathinf.eu/pytorch/arm64/torchvision-0.7.0a0+78ed10c-cp37-cp37m-linux_aarch64.whl

RUN pip install torch*.whl torchvision*.whl

RUN \
    wget https://github.com/kaustubhrajput46/datasets/raw/main/jpgs2.zip && \
    unzip jpgs2.zip -d data

USER app
ENV PATH=$PATH:/home/app/.local/bin:/home/app/python/bin/
ENV PYTHONPATH=$PYTHONPATH:/home/app/python

RUN pip install -r requirements.txt --target=/home/app/python

RUN mkdir -p function
RUN touch ./function/__init__.py

WORKDIR /home/app/function/
COPY function/requirements.txt	.

RUN pip install -r requirements.txt --target=/home/app/python

WORKDIR /home/app/

USER root

COPY function           function

# Allow any user-id for OpenShift users.
RUN chown -R app:app ./ && \
    chmod -R 777 /home/app/python

USER app

ENV fprocess="python3 index.py"
EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]