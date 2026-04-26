# NexusMancer-bioai-easykit

[![Codebase GitHub](https://img.shields.io/badge/Codebase-GitHub-1f1f1f?logo=github&logoColor=white&labelColor=555555&style=flat)](https://github.com/NexusMancer/NexusMancer-bioai-easykit)

**For biologists**: A beginner-friendly toolkit that makes cloning, setting up, and running public BioAI repositories super easy through a **unified workflow**.

If there’s a model or tool you’d like to run but can’t find here, feel free to reach out — I’d be more than happy to help add it.

---

## Progress


| Model / Tool                                       | Status | Repository                                                                                  |
| -------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------- |
| **Protein Foundation / Structure Models**          | —      | —                                                                                           |
| ESM-2                                              | ⬜      | [facebookresearch/esm](https://github.com/facebookresearch/esm)                             |
| ESM-3                                              | ⬜      | [evolutionaryscale/esm](https://github.com/evolutionaryscale/esm)                           |
| Protenix                                           | ⬜      | [bytedance/Protenix](https://github.com/bytedance/Protenix)                                 |
| OpenFold                                           | ⬜      | [aqlaboratory/openfold](https://github.com/aqlaboratory/openfold)                           |
| **RNA / Genomics Foundation Models**               | —      | —                                                                                           |
| RNA-FM                                             | ⬜      | [ml4bio/RNA-FM](https://github.com/ml4bio/RNA-FM)                                           |
| Evo 2                                              | ⬜      | [ArcInstitute/evo2](https://github.com/ArcInstitute/evo2)                                   |
| Nucleotide Transformer                             | ⬜      | [instadeepai/nucleotide-transformer](https://github.com/instadeepai/nucleotide-transformer) |
| DNABERT-2                                          | ⬜      | [MAGICS-LAB/DNABERT_2](https://github.com/MAGICS-LAB/DNABERT_2)                             |
| **Single-Cell Foundation / Representation Models** | —      | —                                                                                           |
| scFoundation                                       | ⬜      | [biomap-research/scFoundation](https://github.com/biomap-research/scFoundation)             |
| Geneformer                                         | ⬜      | [jkobject/geneformer](https://github.com/jkobject/geneformer)                               |
| scGPT                                              | ✅      | [ArcInstitute/state](https://github.com/ArcInstitute/state-reproduce)                       |
| scVI                                               | ✅      | [ArcInstitute/state](https://github.com/ArcInstitute/state-reproduce)                       |
| **Single-Cell Perturbation Models / Tools**        | —      | —                                                                                           |
| ContextMean                                        | ✅      | [ArcInstitute/state](https://github.com/ArcInstitute/state-reproduce)                       |
| PerturbMean                                        | ✅      | [ArcInstitute/state](https://github.com/ArcInstitute/state-reproduce)                       |
| lrlm                                               | ✅      | [ArcInstitute/state](https://github.com/ArcInstitute/state-reproduce)                       |
| CPA                                                | ✅      | [ArcInstitute/state](https://github.com/ArcInstitute/state-reproduce)                       |
| GEARS                                              | ✅      | [ArcInstitute/state](https://github.com/ArcInstitute/state-reproduce)                       |
| state                                              | ✅      | [ArcInstitute/state](https://github.com/ArcInstitute/state)                                 |
| scDFM                                              | ✅      | [AI4Science-WestlakeU/scDFM](https://github.com/AI4Science-WestlakeU/scDFM)                 |


---

For other CUDA versions, CPU-only, or newer/older PyTorch releases, visit:  

- [PyTorch Previous Versions](https://pytorch.org/get-started/previous-versions/)

---

## Quick Start (3–5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/NexusMancer/NexusMancer-bioai-easykit.git
cd NexusMancer-bioai-easykit

# 2. Make the setup script executable (important!)
chmod +x model_setup.sh

# 3. Create the unified conda environment

conda create -n easykit python=3.11

conda activate easykit

pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126 

conda install -c conda-forge mamba -y

mamba env update -f environment.yml

pip show torch | grep -E '^Version:'
pip show torchvision | grep -E '^Version:'
pip show torchaudio | grep -E '^Version:'

change/add torch torchvision torchaudio and their version to requirements.txt

pip install -r requirements.txt


# 5. Run the setup script (this automatically clones all tools + applies bug fixes)
./model_setup.sh

---


```

## GEARS Cache (Hugging Face Dataset)

GEARS requires a large pre-processed cache folder: `dataset/gears_cache/go_essential_all/`.  
We have uploaded it to **Hugging Face Datasets** for fast one-click download.

**Dataset URL**:  
🔗 [https://huggingface.co/datasets/NexusMancer/NexusMancer-bioai-easykit-gears-cache](https://huggingface.co/datasets/NexusMancer/NexusMancer-bioai-easykit-gears-cache)

### 📥 How to Use (Recommended)

Two ready-to-use scripts are provided in `scripts/huggingface/`:

#### 1. Download the cache (most common for users)

```bash
# Go to project root
cd NexusMancer-bioai-easykit

# One-click download (uses China mirror + resume support)
python3 scripts/huggingface/download_dataset.py
```

#### 2. Upload the cache (for maintainers only)

```bash
python3 scripts/huggingface/upload_dataset.py
```

After downloading, the folder structure will be:

```
NexusMancer-bioai-easykit/
└── dataset/
    └── gears_cache/
        └── go_essential_all/
            ├── go_essential_all.csv
            ├── ...
```

GEARS will automatically detect and use this path.

---

