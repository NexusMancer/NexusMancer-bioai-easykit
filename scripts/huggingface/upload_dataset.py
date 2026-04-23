#!/usr/bin/env python
# -*- coding: utf-8 -*-

from huggingface_hub import HfApi
from pathlib import Path
import os

# ================== CONFIGURATION ==================
if "PROJECT_ROOT" in os.environ:
    PROJECT_ROOT = Path(os.environ["PROJECT_ROOT"])
else:
    PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOCAL_FOLDER = PROJECT_ROOT / "dataset" / "gears_cache"

PATH_IN_REPO = "gears_cache"
REPO_ID = "NexusMancer/NexusMancer-bioai-easykit-gears-cache"
# ==================================================

api = HfApi()

print(f"🚀 Starting upload of folder: {LOCAL_FOLDER}")
print(f"   → Will be saved as {PATH_IN_REPO}/ in the HF dataset")
print("⏳ Scanning files and starting upload... (progress bar will appear soon)")

api.upload_folder(
    folder_path=str(LOCAL_FOLDER),
    path_in_repo=PATH_IN_REPO,
    repo_id=REPO_ID,
    repo_type="dataset",
    commit_message=f"Upload {PATH_IN_REPO} cache"
)

print("✅ Upload completed successfully!")
print(f"🔗 Please refresh your Dataset page:")
print(f"https://huggingface.co/datasets/{REPO_ID}")