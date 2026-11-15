#!/usr/bin/env bash
# Task E only, for every model: one engine at a time.
# usage: run_E.sh <slug> <gguf-filename> [port] [api_model]
set -u
FE="$(cd "$(dirname "$0")" && pwd)"
SLUG="$1"; GGUF="$2"; PORT="${3:-8999}"; API="${4:-$1}"
PAT='[l]lama-''server'

pkill -f "$PAT" 2>/dev/null; sleep 5
[ "$PORT" = "8080" ] && { pkill -f '[s]erve/server\.py' 2>/dev/null; sleep 8; }

if [ "$PORT" = "8080" ]; then
  cd ~/ia/llama/Strata
  setsid nohup ./run-iq3_xxs.sh < /dev/null > "$FE/logs/$SLUG.strata.out" 2>&1 &
else
  cd ~/ia/llama
  python3 -c "
import sys; sys.path.insert(0,'.')
from ggufbench import server
open('/tmp/opencode/_e_srv.sh','w').write(' '.join(server.build_args('$GGUF','fixed',$PORT)))
"
  setsid nohup bash /tmp/opencode/_e_srv.sh > "$FE/logs/$SLUG.server.log" 2>&1 &
fi

for i in $(seq 1 60); do
  sleep 5
  curl -s --max-time 3 "http://127.0.0.1:$PORT/health" 2>/dev/null | grep -q '"status"' && { echo "  $SLUG healthy ($((i*5))s)"; break; }
done
curl -s --max-time 3 "http://127.0.0.1:$PORT/health" | grep -q '"status"' || { echo "  $SLUG NEVER HEALTHY"; exit 1; }

mkdir -p "$FE/answers/$SLUG"
if [ -s "$FE/answers/$SLUG/E_largefile.md" ]; then
  echo "  $SLUG: E ja hi és"
else
  python3 /tmp/opencode/llm_dispatch.py "$FE/prompts/E_largefile.md" \
    "$FE/answers/$SLUG/E_largefile.md" "$API" "$PORT" 2>&1 | sed 's/^/  /'
fi
python3 "$FE/grade_E.py" "$SLUG" "$FE/answers/$SLUG"
