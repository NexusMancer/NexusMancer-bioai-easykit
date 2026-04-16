
```bash
conda create -n easykit python=3.11

conda activate easykit

pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126

conda install -c conda-forge mamba -y

mamba env update -f environment.yml

pip show torch | grep -E '^Version:'
pip show torchvision | grep -E '^Version:'
pip show torchaudio | grep -E '^Version:'
```


add torch torchvision torchaudio and their version to requirements.txt


```bash
pip install -r requirements.txt
```

