FROM openfaas/classic-watchdog:0.18.1 as watchdog
FROM python:3

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog


ENV PATH=$PATH:/home/app/.local/bin:/home/app/python/bin/
ENV PYTHONPATH=$PYTHONPATH:/home/app/python

RUN mkdir -p /home/app

RUN \
        apt-get update && apt-get install -y \
        autoconf \
        build-essential \
        libtool \
        bc \
        automake \
        git

RUN \
        apt-get install -y \
        wget

WORKDIR /home/app
RUN \
        git clone https://github.com/kaustubhrajput46/darknet.git

WORKDIR /home/app/darknet
RUN \
        wget https://github.com/kaustubhrajput46/datasets/raw/main/jpgs.zip && \
        unzip jpgs.zip -d data

COPY exec.py .
RUN chmod 777 exec.py
# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
ENV fprocess="python3 exec.py"

# Set to true to see request in function logs
ENV write_debug="true"

EXPOSE 8080
CMD ["fwatchdog"]