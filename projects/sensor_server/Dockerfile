FROM python:3.12-slim

WORKDIR /app/

RUN pip install poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --without dev

COPY src/ src/
COPY webapp/ webapp/

EXPOSE 80

ENTRYPOINT ["poetry", "run", "uvicorn", "webapp.app:create_app"]
CMD ["--host", "0.0.0.0", "--port", "80", "--no-access-log", "--factory"]