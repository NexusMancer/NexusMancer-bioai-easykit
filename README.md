# NexusMancer-bioai-easykit

**For biologists**: A beginner-friendly toolkit that makes cloning, setting up, and running public BioAI repositories super easy through a **unified workflow**.

If there’s a model or tool you’d like to run but can’t find here, feel free to reach out — I’d be more than happy to help add it.

---

## Progress

| Model / Tool | Status |
| :----------- | :----: |
| **Protein Foundation / Structure Models** | — |
| ESM-2 | ⬜ |
| ESM-3 | ⬜ |
| Protenix | ⬜ |
| OpenFold | ⬜ |
| **RNA / Genomics Foundation Models** | — |
| RNA-FM | ⬜ |
| Evo 2 | ⬜ |
| Nucleotide Transformer | ⬜ |
| DNABERT-2 | ⬜ |
| **Single-Cell Foundation / Representation Models** | — |
| scGPT | ⬜ |
| scFoundation | ⬜ |
| Geneformer | ⬜ |
| scVI | ⬜ |
| **Single-Cell Perturbation Models / Tools** | — |
| scDFM | ✅ |
| ContextMean | ⬜ |
| PerturbMean | ⬜ |
| CPA | ⬜ |
| GEARS | ⬜ |
| state | ⬜ |


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
```

