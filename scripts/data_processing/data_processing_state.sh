#!/bin/bash
# =============================================================================
# data_processing_state.sh
# Automated Norman data preprocessing pipeline (relative paths, portable)
# =============================================================================

set -e  # Exit immediately if any command fails

# ==================== 1. Automatically detect project paths ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DATASET_DIR="${PROJECT_ROOT}/dataset/perturbation"

# ==================== 2. Define input/output paths ====================
# Corrected vocab file path
INPUT_ADATA="${DATASET_DIR}/norman_2019_adata.h5ad"
VOCAB_FILE="${PROJECT_ROOT}/tools/scDFM/src/tokenizer/norman_5000_highly_vocab.json"
INTERMEDIATE_H5AD="${DATASET_DIR}/norman.h5ad"
PREPROCESSED_H5AD="${DATASET_DIR}/norman_preprocessed_4baseline.h5ad"

# ==================== 3. Run the preprocessing pipeline ====================
echo "🚀 Starting Norman data preprocessing pipeline..."
echo "Project root          : ${PROJECT_ROOT}"
echo "Dataset directory     : ${DATASET_DIR}"
echo "Vocab file            : ${VOCAB_FILE}"

# Step 1: Run norman_preprocessing_pipeline.py
echo "📌 Step 1: Running norman_preprocessing_pipeline.py ..."
python "${PROJECT_ROOT}/data_processing/norman_preprocessing_pipeline.py" \
    --input "${INPUT_ADATA}" \
    --vocab "${VOCAB_FILE}" \
    --output "${INTERMEDIATE_H5AD}"

echo "✅ Step 1 completed! Intermediate file created: ${INTERMEDIATE_H5AD}"

# Step 2: Run state tx preprocess_train
echo "📌 Step 2: Running state tx preprocess_train ..."
state tx preprocess_train \
    --adata "${INTERMEDIATE_H5AD}" \
    --output "${PREPROCESSED_H5AD}" \
    --num_hvgs 2000

echo "✅ Step 2 completed! Final preprocessed file created: ${PREPROCESSED_H5AD}"
echo "🎉 All processing finished successfully!"