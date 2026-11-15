#!/usr/bin/env bash
# Run the 4-task battery against every fleet model, one engine at a time.
# usage: master.sh <slug> [api_model]   (server must already be up on 8999/8080)
set -u
FE="$(cd "$(dirname "$0")" && pwd)"
SLUG="$1"; APIMODEL="${2:-$1}"; PORT="${3:-8999}"
bash "$FE/run_one.sh" "$SLUG" "$PORT" "$APIMODEL"
python3 "$FE/grade.py" "$SLUG" "$FE/answers/$SLUG"
