"""
prepare_dataset.py
===================
Combines True.csv and Fake.csv from the dataset directory into a single
standardized training CSV file containing 'text' and 'label' columns.

- 'title' is selected as the text source since it matches the typical length
  and style of claims extracted by the pipeline at inference time.
- Label 1 is assigned to True news, and label 0 is assigned to Fake news.
- The dataset is shuffled to ensure a uniform distribution of classes.
- Supports sampling a subset for faster training runs.
"""

import argparse
import os
import pandas as pd
from pathlib import Path

def prepare_data(dataset_dir: str, output_path: str, sample_size: int = None):
    dataset_path = Path(dataset_dir)
    true_csv = dataset_path / "True.csv"
    fake_csv = dataset_path / "Fake.csv"

    if not true_csv.exists():
        raise FileNotFoundError(f"True.csv not found in {dataset_dir}")
    if not fake_csv.exists():
        raise FileNotFoundError(f"Fake.csv not found in {dataset_dir}")

    print("Loading True.csv...")
    df_true = pd.read_csv(true_csv)
    print("Loading Fake.csv...")
    df_fake = pd.read_csv(fake_csv)

    print(f"Loaded {len(df_true)} true news articles and {len(df_fake)} fake news articles.")

    # Select title as training text (matches the short claim format used at inference time)
    df_true = df_true[['title']].copy()
    df_true.rename(columns={'title': 'text'}, inplace=True)
    df_true['label'] = 1

    df_fake = df_fake[['title']].copy()
    df_fake.rename(columns={'title': 'text'}, inplace=True)
    df_fake['label'] = 0

    # Concatenate datasets
    combined_df = pd.concat([df_true, df_fake], ignore_index=True)

    # Drop any missing entries
    combined_df = combined_df.dropna(subset=['text', 'label'])
    combined_df['label'] = combined_df['label'].astype(int)

    print(f"Total entries after cleaning: {len(combined_df)}")

    # Shuffle the dataset
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # Apply sampling if requested
    if sample_size and sample_size < len(combined_df):
        print(f"Sampling a balanced subset of size {sample_size}...")
        # To maintain class balance:
        half_sample = sample_size // 2
        df_true_sampled = combined_df[combined_df['label'] == 1].sample(n=half_sample, random_state=42)
        df_fake_sampled = combined_df[combined_df['label'] == 0].sample(n=half_sample, random_state=42)
        combined_df = pd.concat([df_true_sampled, df_fake_sampled], ignore_index=True)
        # Shuffle again after sampling
        combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
        print(f"Sampled dataset size: {len(combined_df)} (Real: {len(df_true_sampled)}, Fake: {len(df_fake_sampled)})")

    # Save to output path
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(output_file, index=False)
    print(f"Successfully saved prepared dataset to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare True/Fake dataset for RoBERTa fine-tuning.")
    parser.add_argument("--dir", default="dataset", help="Directory containing True.csv and Fake.csv")
    parser.add_argument("--output", default="dataset/combined.csv", help="Output CSV file path")
    parser.add_argument("--sample-size", type=int, default=None, help="If set, samples a balanced subset of this size (e.g. 10000)")

    args = parser.parse_args()
    prepare_data(args.dir, args.output, args.sample_size)
