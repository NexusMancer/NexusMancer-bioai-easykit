#!/bin/bash
# =============================================================================
# State EasyKit Environment Setup (One-Click)
#
# Purpose: Create and fully set up the 'state_easykit' conda environment
#          with PyTorch + all project dependencies.
#          Uses ONLY relative paths and auto-detected project root.
# Location: scripts/env_setups/state.sh
# =============================================================================

set -e  # Exit immediately if any command fails

# ====================== Auto-detect Project Root ======================
# Get absolute path of this script, then go up 2 levels to project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=================================================================="
echo "🚀 Starting State EasyKit Environment Setup"
echo "📍 Auto-detected Project Root : $PROJECT_ROOT"
echo "=================================================================="

# ====================== 1. Create conda environment ======================
ENV_NAME="state_easykit"

echo "🔧 Step 1: Creating/Checking conda environment '$ENV_NAME'..."
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "✅ Environment '$ENV_NAME' already exists, skipping creation."
else
    conda create -n "$ENV_NAME" python=3.11 -y
    echo "✅ Environment '$ENV_NAME' created successfully."
fi

# ====================== 2. Activate conda environment ======================
echo "🔌 Step 2: Activating conda environment '$ENV_NAME'..."
# Make conda activate work inside non-interactive script
eval "$(conda shell.bash hook)"
conda activate "$ENV_NAME"

# Verify activation
if [[ "$CONDA_DEFAULT_ENV" != "$ENV_NAME" ]]; then
    echo "❌ Failed to activate environment '$ENV_NAME'"
    exit 1
fi
echo "✅ Activated '$ENV_NAME' (Python $(python --version))"

# ====================== 3. Install PyTorch with CUDA 12.6 ======================
echo "🔥 Step 3: Installing PyTorch 2.6.0 + CUDA 12.6..."
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
    --index-url https://download.pytorch.org/whl/cu126

echo "✅ PyTorch installation completed"

# ====================== 4. Install project requirements ======================
echo "📦 Step 4: Installing requirements from requirements.txt..."
pip install -r "${PROJECT_ROOT}/requirements.txt"

echo "✅ requirements.txt installed"

echo "📦 Step 5: Installing torch_scatter..."
pip install torch_scatter -f https://data.pyg.org/whl/torch-2.6.0+cu126.html
echo "✅ torch_scatter installed"

# ====================== 5. Install State package in editable mode ======================
echo "🛠️  Step 5: Installing state package in editable mode..."
cd "${PROJECT_ROOT}/tools/state"
pip install -e . --no-deps --no-build-isolation

echo "✅ state package installed (editable mode)"

# ====================== Final Summary ======================
echo "=================================================================="
echo "🎉 Environment setup completed successfully!"
echo "📍 Environment name : state_easykit"
echo "📍 Project root     : $PROJECT_ROOT"
echo "🔥 To activate manually in the future:"
echo "   conda activate state_easykit"
echo "=================================================================="

exit 0