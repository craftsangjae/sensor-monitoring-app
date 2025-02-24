# Stage 1: Build dependencies
FROM python:3.12-slim as builder

WORKDIR /app/

# Install poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --without dev

# Stage 2: Final image
FROM python:3.12-slim as runtime

WORKDIR /app/

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY src/ src/
COPY webapp/ webapp/

EXPOSE 80

ENTRYPOINT ["uvicorn", "webapp.app:create_app"]
CMD ["--host", "0.0.0.0", "--port", "80", "--no-access-log", "--factory"]