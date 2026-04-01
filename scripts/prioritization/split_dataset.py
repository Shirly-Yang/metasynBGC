#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


def main() -> None:
    parser = argparse.ArgumentParser(description="Split Chemprop dataset into train/test CSVs.")
    parser.add_argument("--input", required=True, help="Input CSV with at least smiles and label columns.")
    parser.add_argument("--outdir", required=True, help="Output directory for split files.")
    parser.add_argument("--test-size", type=float, default=0.2, help="Fraction for test set. Default: 0.2")
    parser.add_argument("--seed", type=int, default=42, help="Random seed. Default: 42")
    parser.add_argument("--smiles-col", default="smiles", help="SMILES column name. Default: smiles")
    parser.add_argument("--label-col", default="label", help="Label column name. Default: label")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)

    required = {args.smiles_col, args.label_col}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Keep only rows with both SMILES and labels present
    df = df.dropna(subset=[args.smiles_col, args.label_col]).copy()

    # Force binary integer labels
    df[args.label_col] = df[args.label_col].astype(int)

    # Stratified split to preserve class ratio
    train_df, test_df = train_test_split(
        df,
        test_size=args.test_size,
        random_state=args.seed,
        stratify=df[args.label_col]
    )

    train_path = outdir / "train.csv"
    test_path = outdir / "test.csv"

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    # Save basic summary
    summary = pd.DataFrame([
        {
            "dataset": "train",
            "n_total": len(train_df),
            "n_positive": int((train_df[args.label_col] == 1).sum()),
            "n_negative": int((train_df[args.label_col] == 0).sum()),
        },
        {
            "dataset": "test",
            "n_total": len(test_df),
            "n_positive": int((test_df[args.label_col] == 1).sum()),
            "n_negative": int((test_df[args.label_col] == 0).sum()),
        }
    ])
    summary.to_csv(outdir / "split_summary.csv", index=False)

    print(f"Saved: {train_path}")
    print(f"Saved: {test_path}")
    print(f"Saved: {outdir / 'split_summary.csv'}")


if __name__ == "__main__":
    main()
