# Stage 1: Base
FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    htop \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# install and add poetry to the path
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false

# Stage 3: Development Build
FROM base AS development
# Install only runtime dependencies and skip installing the app package,
# so that mounted code (if any) takes effect.
RUN poetry install --no-interaction --no-root
COPY . .
EXPOSE 8000
CMD ["uvicorn", "manage:entry_point", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Stage 2: Production Build
FROM base AS production
# Install all dependencies and install the app itself
RUN poetry install --no-interaction --only main
COPY . .
EXPOSE 8000
# TODO: use app factory
CMD ["uvicorn", "manage:entry_point", "--host", "0.0.0.0", "--port", "8000"]


