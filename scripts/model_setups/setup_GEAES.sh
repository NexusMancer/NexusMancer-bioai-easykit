#!/bin/bash
set -e

echo "=== setup_state.sh: Calling Python script under utils/ to generate examples/ .toml ==="

# Automatically detect project root directory (works no matter where you run the script from)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "${SCRIPT_DIR}/../.." && pwd )"

echo "Project root directory automatically detected as: ${PROJECT_ROOT}"

# Use relative paths (recommended, portable across machines)
DATASET_SRC="${PROJECT_ROOT}/dataset/perturbation/norman_preprocessed.h5ad"
EXAMPLES_DIR="${PROJECT_ROOT}/configs"
PY_SCRIPT="${PROJECT_ROOT}/scripts/utils/generate_zeroshot_toml.py"

# 2. Check if dataset exists
if [ ! -f "$DATASET_SRC" ]; then
  echo "❌ Dataset not found: ${DATASET_SRC}"
  echo "   Please confirm that dataset/perturbation/norman_preprocessed.h5ad has been placed in the project root directory"
  exit 1
fi

# 3. Call the Python script
echo "🚀 Calling generate_zeroshot_toml.py to generate configuration file..."
python3 "$PY_SCRIPT" \
  --dataset-path "$DATASET_SRC" \
  --examples-dir "$EXAMPLES_DIR" \
  --dataset-name "example"

echo "=== setup_state.sh execution completed! All .toml files have been automatically generated ==="