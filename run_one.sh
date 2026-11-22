#!/usr/bin/env bash
# Run the 4-task battery against ONE model already serving on $2, save answers.
# usage: run_one.sh <slug> <port> [api_model_name]
set -u
FE="$(cd "$(dirname "$0")" && pwd)"
SLUG="$1"; PORT="$2"; APIMODEL="${3:-$1}"
# Dispatch driver: la còpia VERSIONADA del repo mana; fallback a les rutes
# històriques fora de repo (el fitxer es va perdre una vegada, 2026-11-22).
DISPATCH="$FE/llm_dispatch.py"
[ -f "$DISPATCH" ] || DISPATCH="$(dirname "$0")/../llm_dispatch.py"
DIR="$(dirname "$0")/answers/$SLUG"
mkdir -p "$DIR"
for T in A_implement B_fix C_review D_diagnose; do
  if [ -f "$DIR/$T.md" ] && [ -s "$DIR/$T.md" ]; then
    echo "  $T: ja hi és, salto"
    continue
  fi
  python3 "$DISPATCH" \
    "$(dirname "$0")/prompts/$T.md" "$DIR/$T.md" "$APIMODEL" "$PORT" \
    > "$DIR/$T.timing" 2>&1 || echo "  $T: FAILED"
  cat "$DIR/$T.timing" | sed 's/^/  /'
done
