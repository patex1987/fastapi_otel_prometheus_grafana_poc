# Use the official Python 3.12 slim base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including htop and curl (required for Poetry installation)
RUN apt-get update && apt-get install -y \
    htop \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only the dependency files to leverage Docker caching
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main \
    && poetry run opentelemetry-bootstrap -a install

# Copy the rest of the application code
COPY . .
WORKDIR /app/fastapiService

# Expose the FastAPI application port
EXPOSE 8000

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
#CMD ["tail", "-f", "/dev/null"]
