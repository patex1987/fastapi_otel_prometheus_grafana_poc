# syntax=docker/dockerfile:1.9

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
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

########################################################################

# Stage 3: Development Build
FROM base AS development
# Install only runtime dependencies and skip installing the app package,
# so that mounted code (if any) takes effect.
RUN poetry install --no-interaction --no-root
COPY . .
EXPOSE 8000

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app
CMD ["uvicorn", "manage:entry_point", "--host", "0.0.0.0", "--port", "8000", "--reload"]

########################################################################

# Stage 2: Production Build
FROM base AS production_builder

# Install all dependencies and install the app itself
# TODO: add package caching and volume binding
RUN poetry install --no-interaction --only main --no-root

# build the wheel for the service and install with pip into the venv - TODO: use uv for this in the future, as this is a hack
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
RUN poetry build -f wheel
RUN pip install --no-deps dist/*.whl


#######################################################################
# Stage 4: Production
# TODO: use a smaller image and install only python into it
# TODO: don't run the app as root
FROM python:3.12-slim AS production

# copy the python env from the builder into the container
COPY --from=production_builder /app/.venv /app/.venv
COPY --from=production_builder /app/manage.py /app/manage.py
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

EXPOSE 8000
# TODO: use app factory
CMD ["uvicorn", "manage:entry_point", "--host", "0.0.0.0", "--port", "8000"]
