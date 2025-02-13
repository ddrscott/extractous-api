#!/bin/bash -ev

PORT=${PORT:-8080}

exec uv run uvicorn app:app --host 0.0.0.0 --port ${PORT}
