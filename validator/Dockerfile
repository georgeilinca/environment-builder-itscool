# FROM python:3.12-slim

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --no-cache-dir -r requirements.txt

# COPY validator.py .
# COPY tehnologii-suportate.yml .

# ENTRYPOINT ["python", "validator.py"]

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY validator.py .
COPY server.py .
COPY tehnologii-suportate.yml .

RUN mkdir -p /config /output

EXPOSE 80

ENTRYPOINT ["python", "server.py"]