# ---- Build stage ----
FROM python:3.11-slim AS builder

WORKDIR /build
COPY app/requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libgomp1 && \
    pip install --no-cache-dir --user -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# ---- Runtime stage ----
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r inference && useradd -r -g inference -d /app -s /sbin/nologin inference

WORKDIR /app

# Copy user-installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Application code
COPY app/ ./
COPY model/ ./model/

RUN mkdir -p /app/model

# Permissions
RUN chown -R inference:inference /app
USER inference

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", \
     "--workers", "2", "--log-level", "info"]
