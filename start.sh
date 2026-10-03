#!/bin/bash
uv run uvicorn services.auth.main:app --port 8001 --reload &
uv run uvicorn services.transport.main:app --port 8002 &
uv run uvicorn services.utility.main:app --port 8003 &
uv run uvicorn services.environment.main:app --port 8004 &
uv run uvicorn services.billing.main:app --port 8005 &
uv run uvicorn services.notification.main:app --port 8006 &
wait
