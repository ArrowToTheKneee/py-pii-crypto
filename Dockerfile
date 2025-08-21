from python:3.11-slim as builder

WORKDIR /app

# Install build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*


# Upgrade pip + build backend
RUN pip install --upgrade pip setuptools wheel build

# Copy metadata only (for layer caching)
COPY pyproject.toml readMe.md /app/

# Copy source code
COPY src /app/src

# Install project (will read dependencies from pyproject.toml)
RUN pip install .

# Stage 2: Runtime stage

FROM python:3.11-slim

WORKDIR /app

# Copy installed packages and CLI entrypoint
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Final entrypoint
ENTRYPOINT ["pii-crypto"]

