FROM python:3.9-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install required tools
RUN apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    curl \
    # Install poetry
    && curl -sSL 'https://install.python-poetry.org' | python - \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*
RUN pip install poetry

# Copy the pyproject.toml and lock file
COPY pyproject.toml poetry.lock poetry.toml ./
# Avoid creating a virtual environment
RUN poetry config virtualenvs.create false
# Install only the PROD dependencies
RUN poetry install --only main --no-root --no-interaction

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
# Start the uvicorn server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
