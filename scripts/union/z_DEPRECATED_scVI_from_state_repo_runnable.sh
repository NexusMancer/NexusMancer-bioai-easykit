#!/bin/bash
# =============================================================================
# scVI Model One-Stop Full Pipeline (Setup -> Preprocess -> Train)
#
# Purpose: Sequentially execute the following three core scripts to achieve
#          one-click workflow from environment setup -> data preprocessing
#          -> zero-shot training.
# Location: scripts/union/run_scVI_full_pipeline.sh
#
# NOTE: This version uses DYNAMIC PROJECT_ROOT detection
#       (no more hard-coded path)
# =============================================================================

set -e  # Exit immediately if any command fails

# ====================== Dynamic Project Root Detection ======================
# Automatically detect PROJECT_ROOT based on the script's own location
# (Script path: ${PROJECT_ROOT}/scripts/union/run_scVI_full_pipeline.sh)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# ====================== Configuration ======================
LOG_FILE="${PROJECT_ROOT}/logs/scVI_full_pipeline_$(date +%Y%m%d_%H%M%S).log"

# Paths to the three core scripts (now using dynamic PROJECT_ROOT)
SCRIPT_SETUP="${PROJECT_ROOT}/scripts/model_setups/setup_scVI.sh"
SCRIPT_PREPROCESS="${PROJECT_ROOT}/scripts/data_processing/data_processing_state.sh"
SCRIPT_TRAIN="${PROJECT_ROOT}/scripts/train/train_scVI_zeroshot.sh"

# ====================== Helper Functions ======================
log() {
    echo -e "\033[1;36m[$(date '+%Y-%m-%d %H:%M:%S')] $1\033[0m" | tee -a "$LOG_FILE"
}

check_script() {
    if [ ! -f "$1" ]; then
        log "❌ Error: Script not found -> $1"
        exit 1
    fi
    if [ ! -x "$1" ]; then
        log "⚠️  Granting execute permission -> $1"
        chmod +x "$1"
    fi
}

# ====================== Main Pipeline ======================
echo "=================================================================="
log "🚀 Starting scVI Model One-Stop Full Pipeline"
log "📍 Detected Project Root: $PROJECT_ROOT"
log "📝 Log File: $LOG_FILE"
echo "=================================================================="

# Record start time for total duration calculation
start_time=$(date +%s)

# 1. Check all required scripts
log "🔍 Step 0/4: Checking script files..."
check_script "$SCRIPT_SETUP"
check_script "$SCRIPT_PREPROCESS"
check_script "$SCRIPT_TRAIN"
log "✅ All scripts verified"

# 2. Run Setup
log "🔧 Step 1/4: Running Environment Setup -> setup_state.sh"
time bash "$SCRIPT_SETUP"
log "✅ Setup completed"

# 3. Run Data Preprocessing
log "📊 Step 2/4: Running Data Preprocessing -> data_processing_state.sh"
time bash "$SCRIPT_PREPROCESS"
log "✅ Data preprocessing completed"

# 4. Run Zero-Shot Training
log "🔥 Step 3/4: Running Zero-Shot Training -> train_scVI_zeroshot.sh"
time bash "$SCRIPT_TRAIN"
log "✅ Training completed!"

# ====================== Final Summary ======================
echo "=================================================================="
log "🎉 Full Pipeline executed successfully! scVI Model workflow completed."
echo "=================================================================="

# Calculate and display total runtime
end_time=$(date +%s)
duration=$((end_time - start_time))
log "⏱️  Total pipeline duration: $(date -d@${duration} -u +%H:%M:%S)"

echo "💡 Next steps:"
echo "   View training log : cat $LOG_FILE"
echo "   Check model output: ls ${PROJECT_ROOT}/output/scVI_tx/"
echo "   Rerun pipeline    : ./run_scVI_full_pipeline.sh"

exit 0