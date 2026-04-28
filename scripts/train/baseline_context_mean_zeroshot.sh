#!/bin/bash
set -e

echo "=== Starting State model zero-shot training (dynamic paths) ==="

# ==================== Automatically detect project root directory (most robust way) ====================
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "${SCRIPT_DIR}/../.." && pwd )"

echo "📍 Project root detected: ${PROJECT_ROOT}"

# Define paths using relative/dynamic paths
CONDIGS_DIR="${PROJECT_ROOT}/configs"
OUTPUT_DIR="${PROJECT_ROOT}/tools/state"

# Ensure the examples directory exists
mkdir -p "$CONDIGS_DIR"

echo "🚀 Running training with dynamic paths..."

state tx train \
  data.kwargs.toml_config_path="${CONDIGS_DIR}/zeroshot_4baseline.toml" \
  data.kwargs.embed_key=X_hvg \
  data.kwargs.output_space=gene \
  data.kwargs.pert_col=pert_col \
  data.kwargs.control_pert=non-targeting \
  data.kwargs.cell_type_key=cell_type \
  training.max_steps=40000 \
  training.batch_size=8 \
  model=context_mean \
  output_dir="${OUTPUT_DIR}" \
  name="context_mean_zeroshot"

echo "=== Training completed! Output saved to: ${OUTPUT_DIR} ==="