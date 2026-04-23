#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Download script for GEARS go_essential_all cache from Hugging Face.
"""

import os
from huggingface_hub import snapshot_download

# ================== CONFIGURATION ==================
# Use Chinese mirror for faster download (recommended in China)
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

REPO_ID = "NexusMancer/NexusMancer-bioai-easykit-gears-cache"
LOCAL_DIR = "dataset/gears_cache"          # will create this folder automatically
# ==================================================

print("🚀 Starting download from Hugging Face...")
print(f"   Repository : {REPO_ID}")
print(f"   Target path: {LOCAL_DIR}")
print("   Using mirror: https://hf-mirror.com (China fast mirror)")

snapshot_download(
    repo_id=REPO_ID,
    repo_type="dataset",
    local_dir=LOCAL_DIR,
    allow_patterns="gears_cache/**",       # only download the gears_cache folder
    resume_download=True,                  # support resume if interrupted
)

print("✅ Download completed successfully!")
print(f"📁 Cache has been saved to: {LOCAL_DIR}/")
print("   You can now use it in your GEARS project.")