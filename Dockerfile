# # ---------- Stage 1: build ----------
# FROM python:3.11-slim AS builder

# WORKDIR /app
# COPY requirements.txt .
# RUN apt-get update && apt-get install -y gcc libpq-dev --no-install-recommends && \
#     pip install --no-cache-dir -r requirements.txt && \
#     apt-get purge -y --auto-remove gcc

# # ---------- Stage 2: runtime ----------
# FROM python:3.11-slim

# WORKDIR /app
# COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
# COPY app ./app
# COPY .env .env

# ENV PYTHONUNBUFFERED=1
# EXPOSE 8080

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
    


# ---------- Stage 1: build ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# install build deps for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install into the standard location (/usr/local) so binaries end up in /usr/local/bin
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.11-slim

WORKDIR /app

# copy all installed packages and scripts from builder
COPY --from=builder /usr/local /usr/local

# copy app source
COPY app ./app
COPY .env .env

ENV PYTHONUNBUFFERED=1
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
    