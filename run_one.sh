#!/usr/bin/env bash
# Run the 4-task battery against ONE model already serving on $2, save answers.
# usage: run_one.sh <slug> <port> [api_model_name]
set -u
SLUG="$1"; PORT="$2"; APIMODEL="${3:-$1}"
DIR="$(dirname "$0")/answers/$SLUG"
mkdir -p "$DIR"
for T in A_implement B_fix C_review D_diagnose; do
  if [ -f "$DIR/$T.md" ] && [ -s "$DIR/$T.md" ]; then
    echo "  $T: ja hi és, salto"
    continue
  fi
  python3 "$(dirname "$0")/../llm_dispatch.py" \
    "$(dirname "$0")/prompts/$T.md" "$DIR/$T.md" "$APIMODEL" "$PORT" \
    > "$DIR/$T.timing" 2>&1 || echo "  $T: FAILED"
  cat "$DIR/$T.timing" | sed 's/^/  /'
done
