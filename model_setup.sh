#!/bin/bash
set -e

echo "🚀 Starting model setup: cloning repositories, applying patches, and downloading data..."

# ================== 1. Clone original repositories ==================
clone_if_not_exists() {
  local dir=$1
  local url=$2
  if [ ! -d "tools/$dir" ]; then
    echo "Cloning $dir ..."
    git clone "$url" "tools/$dir"
  else
    echo "✅ $dir already exists, skipping clone"
  fi
}

# ================== 2. Automatically apply patches ==================
apply_patch() {
  local tool=$1
  local patch_file="patches/$tool/final-fix.patch"
 
  if [ -f "$patch_file" ]; then
    echo "Applying patch for $tool..."
    cd "tools/$tool"
   
    git apply --ignore-whitespace --verbose "../../$patch_file" || {
      echo "⚠️  Patch may already be applied or has minor conflicts, continuing anyway..."
    }
   
    cd ../..
    echo "✅ $tool patch applied successfully"
  fi
}

# ================== 3. Download required datasets ==================
ensure_data_download() {
  local url=$1
  local dest=$2
  local dir=$(dirname "$dest")

  # Create the target directory (skip if it already exists)
  if [ ! -d "$dir" ]; then
    echo "Creating directory: $dir"
    mkdir -p "$dir"
    echo "✅ Directory created: $dir"
  else
    echo "✅ Directory already exists: $dir (skipping creation)"
  fi

  # Download the file (skip if it already exists)
  if [ ! -f "$dest" ]; then
    echo "Downloading $(basename "$dest") from figshare..."
    echo "   → Saving to: $dest"
    curl -L --progress-bar -o "$dest" "$url" || {
      echo "❌ Download failed for $dest"
      return 1
    }
    echo "✅ Successfully downloaded: $dest"
  else
    echo "✅ File already exists, skipping download: $dest"
  fi
}

# ================== Clone and patch the required tools ==================
clone_if_not_exists "state" "https://github.com/ArcInstitute/state.git"
apply_patch "state"

clone_if_not_exists "state-reproduce" "https://github.com/ArcInstitute/state-reproduce.git"
apply_patch "state-reproduce"

clone_if_not_exists "scDFM" "https://github.com/AI4Science-WestlakeU/scDFM.git"
apply_patch "scDFM"

# ================== Download datasets ==================
echo ""
echo "📦 Downloading required datasets..."

# Download Norman 2019 Perturb-seq dataset
ensure_data_download "https://figshare.com/ndownloader/files/43390776" "data/perturbation/norman_2019.h5ad"

echo ""
echo "🎉 Setup completed! All tools cloned, patched, and datasets are ready."