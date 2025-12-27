import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.paths import RAW_DATA_DIR, RESULTS_DIR

def setup_eda_dirs():
    """Create directory for EDA results."""
    eda_dir = RESULTS_DIR / "eda"
    eda_dir.mkdir(parents=True, exist_ok=True)
    return eda_dir

def plot_distributions(df, output_dir):
    """Plot histograms for numerical columns."""
    num_cols = df.select_dtypes(include=[np.number]).columns
    
    # Calculate grid size
    n_cols = 3
    n_rows = (len(num_cols) + n_cols - 1) // n_cols
    
    plt.figure(figsize=(15, 5 * n_rows))
    for i, col in enumerate(num_cols):
        plt.subplot(n_rows, n_cols, i + 1)
        sns.histplot(df[col].dropna(), kde=True)
        plt.title(f'Distribution of {col}')
    
    plt.tight_layout()
    plt.savefig(output_dir / "distributions.png")
    plt.close()
    print(f"Saved distributions to {output_dir / 'distributions.png'}")

def plot_correlations(df, output_dir):
    """Plot correlation matrix."""
    num_df = df.select_dtypes(include=[np.number])
    if num_df.empty:
        return

    plt.figure(figsize=(12, 10))
    corr = num_df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=False, cmap='coolwarm', center=0, square=True)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig(output_dir / "correlation_matrix.png")
    plt.close()
    print(f"Saved correlation matrix to {output_dir / 'correlation_matrix.png'}")

def plot_target_balance(df, target_col, output_dir):
    """Plot target variable distribution."""
    if target_col not in df.columns:
        print(f"Target column {target_col} not found.")
        return

    plt.figure(figsize=(8, 6))
    sns.countplot(x=target_col, data=df)
    plt.title(f'Distribution of Target: {target_col}')
    plt.savefig(output_dir / "target_distribution.png")
    plt.close()
    print(f"Saved target distribution to {output_dir / 'target_distribution.png'}")

def main():
    eda_dir = setup_eda_dirs()
    
    train_path = RAW_DATA_DIR / "train.csv"
    if not train_path.exists():
        print(f"Error: {train_path} not found.")
        return

    print("Loading data...")
    df = pd.read_csv(train_path)
    
    print(f"Dataset Shape: {df.shape}")
    print("\nColumn Info:")
    print(df.dtypes)
    
    print("\nMissing Values:")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    
    print("\nGenerating plots...")
    plot_distributions(df, eda_dir)
    plot_correlations(df, eda_dir)
    
    # Assuming 'diagnosed_diabetes' is the target based on the problem description
    plot_target_balance(df, 'diagnosed_diabetes', eda_dir)

if __name__ == "__main__":
    main()
