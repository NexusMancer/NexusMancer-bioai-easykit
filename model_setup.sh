#!/bin/bash
set -e

echo "🚀 Starting model setup: clone + automatic patching..."

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
    echo "Applying patch for $tool: $patch_file ..."
    cd "tools/$tool"
   
    git apply --ignore-whitespace --verbose "../../$patch_file" || {
      echo "⚠️ Patch may already be applied or has minor conflicts, continuing..."
    }
   
    cd ../..
    echo "✅ $tool patch applied successfully"
  fi
}

# ================== Add your tools here ==================
clone_if_not_exists "state" "https://github.com/ArcInstitute/state.git"
apply_patch "state"

clone_if_not_exists "state-reproduce" "https://github.com/ArcInstitute/state-reproduce.git"
apply_patch "state-reproduce"

clone_if_not_exists "scDFM" "https://github.com/AI4Science-WestlakeU/scDFM.git"
apply_patch "scDFM"


echo "🎉 Setup completed! All tools cloned and patched."