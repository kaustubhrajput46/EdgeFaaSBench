FROM ghcr.io/openfaas/classic-watchdog:0.1.4 as watchdog
FROM nvcr.io/nvidia/l4t-base:r32.4.4

RUN apt-get update && apt-get install -y --no-install-recommends make g++
RUN apt-get install --no-install-recommends --no-install-suggests -y ca-certificates

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

RUN \
        apt-get update && apt-get install -y \
        autoconf \
        build-essential \
        libtool \
        bc \
        automake \
        git \
        zip

RUN mkdir -p /home/app
WORKDIR /home/app

RUN \
        git clone https://github.com/kaustubhrajput46/yolo-custom.git

WORKDIR /home/app/yolo-custom
RUN \
        wget https://github.com/kaustubhrajput46/datasets/raw/main/jpgs.zip && \
        unzip jpgs.zip -d data

COPY exec.py .
RUN chmod 777 exec.py

# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
ENV fprocess="python3 exec.py"

# Set to true to see request in function logs
ENV write_debug="false"

EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
