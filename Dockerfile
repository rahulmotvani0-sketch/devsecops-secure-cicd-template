# Stage 1: Build & Dependency Wheel Compilation
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build tools in build stage only
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Hardened Runtime Container
FROM python:3.12-slim AS runner

WORKDIR /app

# Create dedicated non-root user and group with fixed UID/GID
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin -M -d /app appuser

# Copy installed wheels from builder to non-root home
COPY --from=builder /root/.local /home/appuser/.local
COPY sample-service/src/ ./src/

# Set ownership and permissions
RUN chown -R appuser:appgroup /app /home/appuser

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Switch to non-root execution context (CIS Docker Benchmark 4.1)
USER appuser:appgroup

EXPOSE 8080

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
