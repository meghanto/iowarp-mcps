"""
Unit tests for data_query.filter_values function.

Covers:
 - Basic filtering behavior
 - Edge‑case threshold yielding empty list
 - File‑not‑found error
 - Missing 'value' column error
"""

import os
import pandas as pd
import pytest
from mcp_server.capabilities import data_query

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")


def test_filter_values_basic():
    print("\n=== Running test_filter_values_basic ===")
    threshold = 50
    print(f"Threshold: {threshold}, CSV path: {TEST_DATA_PATH}")
    df = pd.read_csv(TEST_DATA_PATH)
    print("DataFrame head:\n", df.head())
    if 'value' not in df.columns and len(df.columns) == 1:
        df.columns = ['value']
    df['value'] = pd.to_numeric(df['value'], errors='raise')
    expected = df[df['value'] > threshold]['value'].tolist()
    print("Expected values:", expected)

    rows = data_query.filter_values(TEST_DATA_PATH, threshold)
    print("Filtered rows:", rows)
    values = [row['value'] for row in rows]

    assert values == expected


def test_filter_values_threshold_edge():
    print("\n=== Running test_filter_values_threshold_edge ===")
    df = pd.read_csv(TEST_DATA_PATH)
    if 'value' not in df.columns and len(df.columns) == 1:
        df.columns = ['value']
    df['value'] = pd.to_numeric(df['value'], errors='raise')
    max_val = df['value'].max()
    print(f"Using max threshold: {max_val}")

    rows = data_query.filter_values(TEST_DATA_PATH, max_val)
    print("Filtered rows (should be empty):", rows)

    assert rows == [] or len(rows) == 0


def test_filter_values_file_not_found():
    print("\n=== Running test_filter_values_file_not_found ===")
    with pytest.raises(FileNotFoundError) as excinfo:
        data_query.filter_values("nonexistent.csv", 50)
    print("Caught exception:", excinfo.value)


def test_filter_values_missing_column(tmp_path):
    print("\n=== Running test_filter_values_missing_column ===")
    temp_file = tmp_path / "temp.csv"
    temp_file.write_text("A,B\n1,2\n3,4\n")
    print(f"Temporary CSV path: {temp_file}")
    with pytest.raises(ValueError) as excinfo:
        data_query.filter_values(str(temp_file), 10)
    print("Caught exception:", excinfo.value)