
```bash
conda create -n gears python=3.11

conda activate gears

pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126

pip install -r requirements.txt

pip install torch_scatter -f https://data.pyg.org/whl/torch-2.6.0+cu126.html

pip install torchmetrics
pip install torch_geometric
pip install dcor
```

