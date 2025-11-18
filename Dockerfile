FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt ./
RUN pip wheel --no-cache-dir -r requirements.txt --wheel-dir wheels

COPY pythonclient/ibapi/ ./ibapi/
COPY pythonclient/setup.py .

RUN pip wheel --no-cache-dir --wheel-dir wheels .

FROM python:3.12-slim AS runner

COPY --from=builder /app/wheels /wheels
COPY bot.py .
COPY .env .env

# Install tzdata properly
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata && \
    rm -rf /var/lib/apt/lists/*

# Fix US/Eastern alias
RUN mkdir -p /usr/share/zoneinfo/US \
    && ln -s /usr/share/zoneinfo/America/New_York /usr/share/zoneinfo/US/Eastern
ENV TZ=America/New_York

RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels