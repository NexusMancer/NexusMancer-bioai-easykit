"""
Norman dataset preprocessing pipeline.

This script provides a unified workflow for preprocessing Norman h5ad data:
1. Prepare observation metadata (condition, control columns)
2. Replace 'ctrl' with 'control' in condition column
3. Filter cells by vocabulary conditions

Example:
    python norman_preprocessing_pipeline.py \\
        --input /xxx/norman_2019_adata.h5ad.h5ad \\
        --vocab /xxx/norman_5000_highly_vocab.json \\
        --output /xxx/norman.h5ad
"""

import argparse
import json
import re
import sys
from pathlib import Path

import anndata as ad
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / 'dataset' / 'perturbation' / 'norman_2019_adata.h5ad'
VOCAB_PATH = PROJECT_ROOT / 'tools' / 'scDFM' / 'src' / 'tokenizer' / 'norman_5000_highly_vocab.json'
OUTPUT_PATH = PROJECT_ROOT / 'dataset' / 'perturbation' / 'norman.h5ad'


def load_vocab(vocab_path):
    """Load vocabulary from JSON file and return token set.
    
    Reads a JSON file containing vocabulary tokens and converts keys to a set
    for efficient membership testing during validation.
    
    Args:
        vocab_path: File path to the vocabulary JSON file.
        
    Returns:
        set: A set of vocabulary tokens (keys from the JSON file).
    """
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab = json.load(f)
    return set(vocab.keys())


def split_condition(condition):
    """Split condition string into individual gene tokens.
    
    Parses a condition string and extracts individual tokens separated by
    various delimiters (+, comma, semicolon, or pipe). Handles edge cases
    like NaN, empty strings, and whitespace trimming.
    
    Supported delimiters:
    - Plus sign: CBL+CNN1
    - Comma: CBL,CNN1
    - Semicolon: CBL;CNN1
    - Pipe: CBL|CNN1
    
    Args:
        condition: Condition string or NaN value to split.
        
    Returns:
        list: List of individual gene tokens (strings), or empty list if condition is NaN or empty.
    """
    if pd.isna(condition):
        return []

    condition = str(condition).strip()
    if condition == "":
        return []

    tokens = re.split(r"[+,;|]", condition)
    tokens = [t.strip() for t in tokens if t.strip() != ""]
    return tokens


def condition_is_valid(condition, vocab_tokens, allowed_special_tokens=None):
    """Validate that all tokens in a condition exist in the vocabulary.
    
    Checks whether all gene tokens in a condition string are present in the
    provided vocabulary set. Special tokens (like 'control') can be exempted
    from vocabulary checks via the allowed_special_tokens parameter.
    
    Args:
        condition: Condition string to validate (may contain multiple tokens).
        vocab_tokens: Set of valid vocabulary tokens to check against.
        allowed_special_tokens: Set of special tokens allowed outside vocabulary (default: None).
        
    Returns:
        tuple: (is_valid, missing_tokens) where is_valid is bool and missing_tokens is list
               of tokens not found in vocab_tokens or allowed_special_tokens.
    """
    if allowed_special_tokens is None:
        allowed_special_tokens = set()

    tokens = split_condition(condition)

    missing = []
    for token in tokens:
        if token in allowed_special_tokens:
            continue
        if token not in vocab_tokens:
            missing.append(token)

    return len(missing) == 0, missing


def step_1_prepare_obs(adata):
    """Step 1: Prepare observation metadata for State model training/inference.
    
    This function processes the 'guide_merged' column to create the columns
    required by the State model (especially 'pert_col'):
    
    - 'condition': Copy of the original 'guide_merged' values
    - 'pert_col': Standardized perturbation column.
                  All control conditions (detected via keywords,
                  case-insensitive) are converted to "non-targeting".
                  *** IMPORTANT: Converted to pandas Categorical at the end ***
    - 'control': Binary indicator (1 = control, 0 = perturbed)
    - 'cell_type': Copy of 'gene_program' values (also Categorical)
    - 'gem_group': Copy of 'gemgroup' (if exists, also Categorical)
    
    Args:
        adata: AnnData object to prepare.
        
    Returns:
        AnnData: Updated AnnData object with new standardized columns in .obs.
        
    Raises:
        ValueError: If 'guide_merged' column is not found in adata.obs.
    """
    print("\n" + "="*60)
    print("STEP 1: Prepare observation metadata")
    print("="*60)
    
    if "guide_merged" not in adata.obs.columns:
        raise ValueError(
            f"Missing 'guide_merged' column in obs. Available columns: {list(adata.obs.columns)}"
        )

    # Extract raw columns as string type (with stripping for safety)
    gm_raw = adata.obs["guide_merged"].astype(str).str.strip()
    gp_raw = adata.obs["gene_program"].astype(str).str.strip()

    # Create condition column as direct copy of guide_merged (preserves original)
    adata.obs["condition"] = gm_raw.copy()

    # Create pert_col (the key column required by State model)
    adata.obs["pert_col"] = gm_raw.copy()

    # ===================================================================
    # CONTROL STANDARDIZATION LOGIC (case-insensitive keyword matching)
    # ===================================================================
    control_keywords = ["ctrl", "control", "Control", "CTRL", "Control"]

    # Create mask for control cells
    lower_pert = adata.obs["pert_col"].str.lower()
    is_control = lower_pert.apply(
        lambda x: any(kw.lower() in x for kw in control_keywords)
    )

    # Replace all detected control values with "non-targeting"
    adata.obs.loc[is_control, "pert_col"] = "non-targeting"

    # Create binary control column
    adata.obs["control"] = is_control.astype(int)

    # Create cell_type column
    adata.obs["cell_type"] = gp_raw.copy()

    # Optional: create gem_group
    if "gemgroup" in adata.obs.columns:
        gm_group_raw = adata.obs["gemgroup"].astype(str).str.strip()
        adata.obs["gem_group"] = gm_group_raw.copy()
        print(f"√ Created 'gem_group' column (copy of gemgroup)")
        print(f"   - Unique gemgroup values: {adata.obs['gemgroup'].nunique()}")
    else:
        print(f"X 'gemgroup' column not found, skipping gem_group creation")
    
    # ===================================================================
    # CRITICAL FIX: Convert to Categorical dtype (required by cell_load / State)
    # ===================================================================
    # This is what was missing - without it, .h5ad will not have /categories
    adata.obs["pert_col"] = adata.obs["pert_col"].astype("category")
    adata.obs["cell_type"] = adata.obs["cell_type"].astype("category")
    if "gem_group" in adata.obs.columns:
        adata.obs["gem_group"] = adata.obs["gem_group"].astype("category")
    
    print(f"√ Created 'condition' column (copy of guide_merged)")
    print(f"√ Created 'pert_col' column (controls standardized to 'non-targeting')")
    print(f"  - Standardized to 'non-targeting': {is_control.sum()} cells")
    print(f"√ Created 'control' column (binary indicator)")
    print(f"  - control=1: {is_control.sum()} cells")
    print(f"  - control=0: {(~is_control).sum()} cells")
    print(f"√ Created 'cell_type' column (copy of gene_program)")
    print(f"√ Converted 'pert_col', 'cell_type' (and 'gem_group' if exists) to Categorical dtype")

    return adata


def step_2_replace_ctrl(adata, condition_col="condition"):
    """Step 2: Replace 'ctrl' with 'control' in condition column.
    
    Finds all instances of 'ctrl' in the condition column and replaces them
    with 'control'. This handles both standalone 'ctrl' values and combinations
    like 'ctrl+KLF1'.
    
    Args:
        adata: AnnData object to modify.
        condition_col: Column name in obs storing condition (default: 'condition').
        
    Returns:
        AnnData: Updated object with replaced values.
        
    Raises:
        ValueError: If condition column is not found.
    """
    print("\n" + "="*60)
    print("STEP 2: Replace 'ctrl' with 'control'")
    print("="*60)
    
    if condition_col not in adata.obs.columns:
        raise ValueError(
            f"Column '{condition_col}' not found in obs. Available columns: {list(adata.obs.columns)}"
        )
    
    # Show values before modification
    print(f"\nBefore modification - unique values in '{condition_col}':")
    before_counts = adata.obs[condition_col].value_counts(dropna=False)
    print(before_counts)
    
    # Replace 'ctrl' with 'control'
    adata.obs[condition_col] = (
        adata.obs[condition_col]
        .astype(str)
        .str.replace("ctrl", "control")
    )
    
    # Show values after modification
    print(f"\nAfter modification - unique values in '{condition_col}':")
    after_counts = adata.obs[condition_col].value_counts(dropna=False)
    print(after_counts)
    print("√ Replacement complete")
    
    return adata


def step_3_filter_by_vocab(adata, vocab_tokens, condition_col="condition"):
    """Step 3: Filter cells by condition vocabulary.
    
    Keeps only cells where all gene tokens in the condition column exist
    in the provided vocabulary. Generates a summary report.
    
    Args:
        adata: AnnData object to filter.
        vocab_tokens: Set of valid vocabulary tokens.
        condition_col: Column name in obs storing condition (default: 'condition').
        
    Returns:
        AnnData: Filtered object containing only valid cells.
        
    Raises:
        ValueError: If condition column is not found.
    """
    print("\n" + "="*60)
    print("STEP 3: Filter cells by vocabulary condition")
    print("="*60)
    
    if condition_col not in adata.obs.columns:
        raise ValueError(
            f"Column '{condition_col}' not found in obs. Available columns: {list(adata.obs.columns)}"
        )
    
    # These tokens are allowed even if they are not in the vocabulary
    allowed_special_tokens = {"control"}
    
    conditions = adata.obs[condition_col].astype(str)
    
    keep_mask = []
    invalid_examples = []
    
    for idx, condition in enumerate(conditions):
        is_valid, missing_tokens = condition_is_valid(
            condition=condition,
            vocab_tokens=vocab_tokens,
            allowed_special_tokens=allowed_special_tokens,
        )
        
        keep_mask.append(is_valid)
        
        if not is_valid and len(invalid_examples) < 20:
            invalid_examples.append(
                {
                    "cell_index": adata.obs_names[idx],
                    "condition": condition,
                    "missing_tokens": missing_tokens,
                }
            )
    
    keep_mask = pd.Series(keep_mask, index=adata.obs_names)
    
    # Filter the data
    n_before = adata.n_obs
    adata_filtered = adata[keep_mask.values].copy()
    n_after = adata_filtered.n_obs
    n_removed = n_before - n_after
    
    # Print summary
    print("\nFiltering summary:")
    print(f"  Cells before filtering: {n_before}")
    print(f"  Cells removed:          {n_removed}")
    print(f"  Cells kept:             {n_after}")
    
    if invalid_examples:
        print("\nExamples of removed cells (first 20):")
        for ex in invalid_examples:
            print(
                f"  cell={ex['cell_index']}, "
                f"condition={ex['condition']}, "
                f"missing={ex['missing_tokens']}"
            )
    
    print("√ Filtering complete")
    
    return adata_filtered


def main():
    """Main entry point for the preprocessing pipeline."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--input",
        type=str,
        default=str(INPUT_PATH),
        help=f"Input h5ad file path (default: {INPUT_PATH})",
    )
    parser.add_argument(
        "--vocab",
        type=str,
        default=str(VOCAB_PATH),
        help=f"Vocabulary JSON file path (default: {VOCAB_PATH})",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(OUTPUT_PATH),
        help=f"Output h5ad file path (default: {OUTPUT_PATH})",
    )
    parser.add_argument(
        "--condition-col",
        type=str,
        default="condition",
        help="Column name in adata.obs storing perturbation condition (default: 'condition')",
    )
    parser.add_argument(
        "--guide-merged-col",
        type=str,
        default="guide_merged",
        help="Column name in adata.obs storing guide information (default: 'guide_merged')",
    )
    
    args = parser.parse_args()
    
    # Validate input files exist
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    if not Path(args.vocab).exists():
        print(f"Error: Vocabulary file not found: {args.vocab}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("Norman Dataset Preprocessing Pipeline")
    print("="*60)
    print(f"Input:     {args.input}")
    print(f"Vocabulary: {args.vocab}")
    print(f"Output:    {args.output}")
    
    try:
        # Load input data
        print(f"\nLoading input file...")
        adata = ad.read_h5ad(args.input)
        print(f"√ Loaded successfully | Cells: {adata.n_obs} | Genes: {adata.n_vars}")
        
        # Load vocabulary
        print(f"\nLoading vocabulary...")
        vocab_tokens = load_vocab(args.vocab)
        print(f"√ Loaded successfully | Tokens: {len(vocab_tokens)}")
        
        # Execute pipeline steps
        adata = step_1_prepare_obs(adata)
        adata = step_2_replace_ctrl(adata, condition_col=args.condition_col)
        adata = step_3_filter_by_vocab(adata, vocab_tokens, condition_col=args.condition_col)
        
        # Save output
        print("\n" + "="*60)
        print("Saving output")
        print("="*60)
        adata.write_h5ad(args.output)
        print(f"√ Saved to: {args.output}")
        print(f"  Final cells: {adata.n_obs}")
        print(f"  Final genes: {adata.n_vars}")
        
        print("\n" + "="*60)
        print("Pipeline complete!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
