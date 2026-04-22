#!/bin/bash
set -e

# =====================================================
# Norman Gene Perturbation Dataset - GEARS Training
# Model name is hardcoded (no command-line model argument required).
# =====================================================

FOLD_ID=${1:-1}

# ============== Configuration ==============
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "${SCRIPT_DIR}/../.." && pwd )"

STATE_BASELINES_DIR="${PROJECT_ROOT}/tools/state-reproduce/baselines"
DATA_TOML_PATH="${PROJECT_ROOT}/configs/zeroshot.toml"
OUTPUT_DIR="${PROJECT_ROOT}/logs/gears_norman/"

echo "✅ Project root detected: $PROJECT_ROOT"

export PROJECT_ROOT

echo "✅ State-reproduce baselines directory: $STATE_BASELINES_DIR"
echo ""

# ============== Install state_sets_reproduce if needed ==============
export PYTHONPATH="$STATE_BASELINES_DIR:${PYTHONPATH}"

if ! python -c "import state_sets_reproduce" 2>/dev/null; then
    echo "🔧 Installing state_sets_reproduce in editable mode..."
    cd "$STATE_BASELINES_DIR"
    pip install -e .
    cd - > /dev/null
    echo "✅ Installation completed successfully"
fi

# ============== Training Settings ==============
mkdir -p "$OUTPUT_DIR"

BATCH_COL="gem_group"
PERT_COL="pert_col"
CELL_TYPE_KEY="cell_type"
CONTROL_PERT="non-targeting"
FOLD_NAME="fold${FOLD_ID}"

echo "═══════════════════════════════════════════════"
echo "  📊 Training GEARS on Norman Gene Perturbation Dataset"
echo "  Fold          : $FOLD_ID"
echo "  Output directory : $OUTPUT_DIR"
echo "═══════════════════════════════════════════════"

cd "$STATE_BASELINES_DIR"

python -m state_sets_reproduce.train \
    data.kwargs.toml_config_path=$DATA_TOML_PATH \
    data.kwargs.embed_key=X_hvg \
    data.kwargs.basal_mapping_strategy=random \
    data.kwargs.output_space=gene \
    data.kwargs.num_workers=24 \
    data.kwargs.batch_col=${BATCH_COL} \
    data.kwargs.pert_col=${PERT_COL} \
    data.kwargs.cell_type_key=${CELL_TYPE_KEY} \
    data.kwargs.control_pert=${CONTROL_PERT} \
    training.max_steps=250000 \
    training.val_freq=5000 \
    training.test_freq=9000 \
    training.batch_size=128 \
    model=gears \
    training=gears \
    output_dir="${OUTPUT_DIR}" \
    name="${FOLD_NAME}"

echo "✅ Training completed for GEARS (fold ${FOLD_ID})"