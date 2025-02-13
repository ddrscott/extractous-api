FROM ubuntu:24.04 AS builder

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    pkg-config \
    zlib1g-dev \
    && curl https://sh.rustup.rs -sSf | sh -s -- -y \
    && curl -LsSf https://astral.sh/uv/install.sh | sh -s

RUN bash -c 'source "$HOME/.cargo/env" \
    && source "$HOME/.local/bin/env" \
    && uv python install 3.12 \
    && uv venv --python 3.12 \
    && uv pip install extractous '

RUN find ./root/.cache/uv -name *.so -path *bindings/extractous*  ! -path *release* -print -exec cp {} /.venv/lib/python3.12/site-packages/extractous/ \;

FROM python:3.12-slim

RUN pip install uv \
    && uv venv

COPY --from=builder /.venv/lib/python3.12/site-packages/extractous /.venv/lib/python3.12/site-packages/extractous

WORKDIR /app

COPY requirements.txt .

RUN uv pip install -r requirements.txt

COPY . .

CMD ["./start.sh"]
