
```bash
conda create -n scgpt python=3.11

conda activate scgpt

pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126

pip install -r requirements.txt

pip install torch_scatter -f https://data.pyg.org/whl/torch-2.6.0+cu126.html

# Upgrade essential build tools
pip install -U pip setuptools wheel packaging ninja cmake

# Install pytorch-fast-transformers
pip install pytorch-fast-transformers \
    --no-build-isolation \
    --index-url https://pypi.org/simple

# Install flash-attn (remember to set TORCH_CUDA_ARCH_LIST according to your GPU)
TORCH_CUDA_ARCH_LIST="9.0" pip install flash-attn==1.0.9 --no-build-isolation
```

### GPU Architecture Settings (`TORCH_CUDA_ARCH_LIST`)

Set the correct value **before** running the flash-attn installation command:

- **A100 / A800** → `8.0`
- **RTX 3090 / A40 / A10** → `8.6`
- **H100 / H800 / H20** → `9.0`
- **RTX 4090** → `8.9`
- **Mixed GPUs (multiple types)** → `8.0 8.6 8.9 9.0`

**Quick examples:**

```bash
# For A100 / A800
TORCH_CUDA_ARCH_LIST="8.0" pip install flash-attn==1.0.9 --no-build-isolation

# For H100 / H20 / H800
TORCH_CUDA_ARCH_LIST="9.0" pip install flash-attn==1.0.9 --no-build-isolation

# For mixed GPU cluster (recommended)
TORCH_CUDA_ARCH_LIST="8.0 8.6 8.9 9.0" pip install flash-attn==1.0.9 --no-build-isolation
