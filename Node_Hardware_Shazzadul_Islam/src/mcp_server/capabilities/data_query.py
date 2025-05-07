import pandas as pd

def filter_values(csv_path: str = "data.csv", threshold: float = 50) -> list[dict]:
    """
    Read a CSV (with header 'value', or headerless single column) and
    return a list of rows (dicts) where the 'value' field > threshold.
    """
    df = pd.read_csv(csv_path)

    # If no 'value' column, but exactly one column, rename it
    if 'value' not in df.columns:
        if len(df.columns) == 1:
            df.columns = ['value']
        else:
            raise ValueError(f"Column 'value' not found in {csv_path}")

    # Convert to numeric and filter
    df['value'] = pd.to_numeric(df['value'], errors='raise')
    filtered = df[df['value'] > threshold]

    # Convert to list-of-dicts for JSON serialization
    return filtered.to_dict(orient='records')
