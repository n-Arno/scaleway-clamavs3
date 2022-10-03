FROM clamav/clamav:latest

COPY init /init
COPY serve.py /serve.py

RUN apk add --no-cache python3 py3-pip && \
    pip install boto3 pyclamd bottle paste && \
    mkdir -p /scandir && \
    chmod +x /init && \
    freshclam

EXPOSE 8080
