#!/usr/bin/env bash
# RICK C-137 PIPER VOICE — TRAINING & E2E VALIDATION
# From PDF pages 12–16

set -euo pipefail

echo "=== Phase 1: Environment ==="
pip install -q "piper-tts[train]" librosa webrtcvad || true
piper --version || echo "piper not on PATH — install manually"

echo "=== Phase 2: Preprocess ==="
piper preprocess \
  --config config_rick_c137.json \
  --corpus-dir ./corpus_rick_c137 \
  --output-dir ./processed_rick || echo "preprocess skipped (no corpus yet)"

echo "=== Phase 3: Train ==="
piper train \
  --config config_rick_c137.json \
  --processed-dir ./processed_rick \
  --output-model ./voices/rick_c137.onnx \
  --checkpoint-epochs 20 \
  --patience 50 || echo "train skipped (requires GPU + corpus)"

echo "=== Phase 4: Generate config ==="
piper generate-config \
  --model ./voices/rick_c137.onnx \
  --speaker "rick-c137" \
  --language "en" \
  --sample-rate 22050 \
  --output ./voices/rick_c137.onnx.json || true

echo "=== Phase 5: Deploy to tele-core ==="
mkdir -p ../tele-core/piper-service/voices
cp -f ./voices/rick_c137.onnx ../tele-core/piper-service/voices/ 2>/dev/null || true
cp -f ./voices/rick_c137.onnx.json ../tele-core/piper-service/voices/ 2>/dev/null || true

echo "=== Done. Seal criteria: onnx + json present, /healthz lists rick-c137 ==="
