#!/usr/bin/env bash
set -euo pipefail

TRAIN_CSV="results/split/train.csv"
TEST_CSV="results/split/test.csv"
MODEL_DIR="results/model"
PRED_DIR="results/predictions"

mkdir -p "${MODEL_DIR}" "${PRED_DIR}"

# 训练
chemprop train \
  --data-path "${TRAIN_CSV}" "${TEST_CSV}" \
  --split-sizes 0.8 0.0 0.0 \
  --task-type classification \
  --smiles-columns smiles \
  --target-columns label \
  --output-dir "${MODEL_DIR}" \
  --metric roc \
  --epochs 30 \
  --pytorch-seed 42

# 预测
# 通常选 best checkpoint
BEST_MODEL=$(find "${MODEL_DIR}" -name "*.ckpt" | head -n 1)

chemprop predict \
  --test-path "${TEST_CSV}" \
  --model-path "${BEST_MODEL}" \
  --smiles-columns smiles \
  --preds-path "${PRED_DIR}/test_predictions.csv"

echo "Prediction file saved to ${PRED_DIR}/test_predictions.csv"
