
```bash
conda create -n state_easykit python=3.11

conda activate state_easykit

pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126

pip install -r requirements.txt

cd state

pip install -e . --no-deps --no-build-isolation

pip install torch_scatter -f https://data.pyg.org/whl/torch-2.6.0+cu126.html
```

