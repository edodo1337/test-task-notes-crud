FROM python:3.10-alpine as builder

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add gcc git libtool automake build-base
RUN apk add gettext
RUN pip3 install Cython
RUN pip3 install -U setuptools pip
RUN pip3 install poetry


COPY poetry.lock pyproject.toml /code/
COPY ./backend /code

WORKDIR /code
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

FROM builder AS base
COPY --from=builder /code /code

WORKDIR /code
