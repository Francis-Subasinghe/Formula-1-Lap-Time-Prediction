#!/bin/bash
uvicorn api.api:app --host 0.0.0.0 --port 10000
chmod +x start.sh
