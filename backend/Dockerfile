FROM python:3.12-slim-bookworm AS builder

RUN pip install -U pip setuptools wheel
RUN pip install pdm

COPY pyproject.toml pdm.lock README.md /pkgs/

WORKDIR /pkgs

RUN mkdir __pypackages__ && pdm install --prod --frozen-lockfile --no-editable

FROM python:3.12-slim-bookworm

ENV PYTHONPATH=/pkgs
COPY --from=builder /pkgs/__pypackages__/3.12/lib /pkgs
COPY --from=builder /pkgs/__pypackages__/3.12/bin/* /bin/

COPY . /app

WORKDIR /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



