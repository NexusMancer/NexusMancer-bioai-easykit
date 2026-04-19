#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Only zero-shot configuration + automatically filter out control/ctrl conditions
Generates ONLY zeroshot.toml with your EXACT desired format
"""

import anndata
import toml
from pathlib import Path
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Automatically generate BioAI zero-shot configuration zeroshot.toml (filters control)")
    parser.add_argument("--dataset-path", required=True, help="Path to norman_preprocessed.h5ad (relative or absolute)")
    parser.add_argument("--examples-dir", required=True, help="Path to examples/ folder")
    parser.add_argument("--dataset-name", default="example", help="Dataset name used in toml (default: example)")
   
    args = parser.parse_args()

    dataset_path = Path(args.dataset_path)
    examples_dir = Path(args.examples_dir)
    dataset_name = args.dataset_name

    if not dataset_path.exists():
        print(f"❌ Dataset not found: {dataset_path}")
        sys.exit(1)

    # Load data
    print(f"✅ Loading dataset: {dataset_path}")
    adata = anndata.read_h5ad(dataset_path)
    print(f"✅ Dataset loaded successfully: {adata.shape[0]:,} cells × {adata.shape[1]:,} genes")

    # Count conditions
    conditions = adata.obs["condition"].value_counts().sort_values(ascending=False)
    print(f"\n📊 condition.value_counts() (total {len(conditions)} unique conditions):")
    print(conditions.head(30))

    unique_conditions = list(conditions.index)

    # ==================== Filter out control/ctrl conditions ====================
    control_keywords = ["ctrl", "control", "Control", "CTRL", "Control"]
    non_control_conditions = [
        cond for cond in unique_conditions
        if not any(kw.lower() in str(cond).lower() for kw in control_keywords)
    ]

    print(f"   After filtering control: {len(non_control_conditions)} conditions remaining")

    # ==================== Build ZERO-SHOT ONLY configuration ====================
    zeroshot = {}
    if len(non_control_conditions) >= 3:
        selected = non_control_conditions[-3:]
    elif len(non_control_conditions) > 0:
        selected = non_control_conditions
    else:
        selected = []

    for cond in selected:
        zeroshot[f'"{dataset_name}.{cond}"'] = "test"

    # Create directory and write zeroshot.toml with EXACT format you provided
    examples_dir.mkdir(parents=True, exist_ok=True)

    zeroshot_path = examples_dir / "zeroshot.toml"
    with open(zeroshot_path, "w", encoding="utf-8") as f:
        f.write('# Dataset paths - maps dataset names to their directories\n')
        f.write('[datasets]\n')
        f.write(f'{dataset_name} = "{dataset_path}"\n\n')
        f.write('# Training specifications\n')
        f.write('# All cell types in a dataset automatically go into training (excluding zeroshot/fewshot overrides)\n')
        f.write('[training]\n')
        f.write(f'{dataset_name} = "train"\n\n')
        f.write('# Zeroshot specifications - entire cell types go to val or test\n')
        f.write('[zeroshot]\n')
        
        # Write each zeroshot entry (exactly as in your example)
        for key, value in zeroshot.items():
            f.write(f'{key} = "{value}"\n')
        
        # Extra blank line to match your example format
        f.write('\n# Fewshot specifications - explicit perturbation lists\n')
        f.write('[fewshot]\n')

    print(f"✅ Generated {zeroshot_path.name} (zero-shot only, exact format)")

    print("\n🎉 zeroshot.toml generation completed!")
    print(f"   Dataset name          : {dataset_name}")
    print(f"   Examples directory    : {examples_dir}")
    print(f"   Original condition count : {len(unique_conditions)}")
    print(f"   Non-control conditions used for zero-shot: {len(selected)}")
    print(f"   Selected zero-shot conditions: {selected}")

if __name__ == "__main__":
    main()