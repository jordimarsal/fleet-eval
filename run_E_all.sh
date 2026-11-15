#!/usr/bin/env bash
FE=/tmp/opencode/fleet-eval
declare -A M=(
  [qwen36]="qwen36-35b-distill-mxfp4_moe.gguf"
  [minicpm]="MiniCPM-V-4_7-35B-A3B-Q4_K_M.gguf"
  [gemma4]="gemma-4-26B-A4B-it-UD-Q5_K_XL.gguf"
  [SC117]="Qwen3.6-35B-A3B-uncensored-heretic-Native-MTP-Preserved-APEX-I-Compact.gguf"
  [Huihui]="Huihui-Qwen3.8-27B-abliterated-UD-Q3_K_XL.gguf"
  [qwen4b]="Qwen3-4B-Instruct-2507-Q4_K_M.gguf"
)
for s in qwen36 minicpm gemma4 SC117 Huihui qwen4b; do
  echo "##### $s"
  bash "$FE/run_E.sh" "$s" "$HOME/ia/llama/models/${M[$s]}" 8999 "$s"
done
echo "##### Strata"
bash "$FE/run_E.sh" Strata "-" 8080 qwen3.8-flash-next-iq3_xxs
echo "##### fi"
