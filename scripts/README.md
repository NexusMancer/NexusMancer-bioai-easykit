# Scripts

This directory contains all automation scripts for setting up environments, preprocessing data, and training models in the **NexusMancer-bioai-easykit** project.

We use the **State model** as the main example. The folder is designed to be easily extended to other models (e.g., scGPT, Geneformer) in the future.

---

## 🚀 Quick Start (Recommended - One-Click Pipeline)

The simplest and fastest way to run the entire State model workflow:

```bash
# 1. Go to environment setup folder
cd scripts/env_setups

# 2. Setup conda environment (only needed once)
chmod +x state.sh
./state.sh

# 3. Run the full one-stop pipeline
cd ../union
chmod +x run_state_full_pipeline.sh
./run_state_full_pipeline.sh
```

This single command will:
- Create and configure the `state_easykit` conda environment
- Preprocess the data
- Launch zero-shot training

---

## 📋 Manual Step-by-Step Workflow (State Model)

If you need to customize data, modify parameters, or run steps individually, follow this exact order:

### 1. Environment Setup (only run once)
```bash
cd scripts/env_setups
chmod +x state.sh
./state.sh
```

### 2. Data Processing (prepare your `.h5ad` file)
```bash
cd scripts/data_processing
chmod +x data_processing_state.sh
./data_processing_state.sh
```

### 3. Training (zero-shot training)
```bash
cd scripts/train
chmod +x train_state_zeroshot.sh
./train_state_zeroshot.sh
```

**Pro tip**: You can also run everything at once using the union script (recommended).

---

## 📁 Folder Structure

```bash
scripts/
├── env_setups/          # Environment creation scripts
│   └── state.sh
├── model_setups/        # Model-specific initialization
│   └── setup_state.sh
├── data_processing/     # Data preprocessing for each model
│   └── data_processing_state.sh
├── train/               # Training scripts
│   └── train_state_zeroshot.sh
├── union/               # One-stop full pipelines
│   └── run_state_full_pipeline.sh
├── utils/               # Helper utilities
│   └── generate_zeroshot_toml.py
└── README.md
```

---

## 🔍 Detailed Script Descriptions (State Model)

| Script | Location | Purpose |
|--------|----------|---------|
| `state.sh` | `env_setups/` | Creates `state_easykit` conda env + installs PyTorch + project dependencies |
| `setup_state.sh` | `model_setups/` | Model-specific setup (usually called automatically) |
| `data_processing_state.sh` | `data_processing/` | Preprocesses raw data into the required `.h5ad` format for State |
| `train_state_zeroshot.sh` | `train/` | Launches zero-shot training with all necessary parameters |
| `run_state_full_pipeline.sh` | `union/` | **Recommended**: Runs all three steps automatically with logging |

---

## 💡 Tips & Best Practices

- All scripts use **relative paths** and automatically detect the project root.
- Logs are saved in the `logs/` folder (auto-created).
- Training outputs are saved under `output/state_tx/`.
- You can safely re-run the full pipeline anytime.
- If you modify data, only re-run `data_processing_state.sh` and `train_state_zeroshot.sh`.
- wandb logs are automatically ignored by `.gitignore`.

---

## 🚧 Adding New Models

The folder structure is designed to be model-agnostic.  
To add a new model (e.g., `scgpt`):
1. Create corresponding scripts following the same naming pattern (`xxx_scgpt.sh`)
2. Add a new pipeline in `union/`

---

**Questions or issues?**  
Check the header comments inside each `.sh` file or open an issue in the repository.

Happy training! 🔥
