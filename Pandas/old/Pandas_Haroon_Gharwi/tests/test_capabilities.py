#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Import libraries for testing:
import pytest
import pandas as pd
import os
from src.capabilities.pandas_handler import filter_csv_data
from src.capabilities.matplotlib_handler import plot_csv_columns

# Create a dummy csv file for testing:
@pytest.fixture
def sample_csv(tmp_path):
    csv_file = tmp_path / "sample.csv"
    df = pd.DataFrame({
        "x": [1, 2, 4, 10],
        "y": [10, 100, 51, 40]
    })
    df.to_csv(csv_file, index=False)
    return str(csv_file)


# Test Tool1: Pandas
# check the functionality of filtering:
def test_filter_csv_file_success(sample_csv):
    result = filter_csv_data(csv_path=sample_csv, column="y",threshold=50)
    
    assert len(result) == 2 #should return only two rows
    assert result[0]["y"] == 100  #the first rwo has x=2 and y=100

# Check the filtering function with incorrect file path:
def test_filter_csv_file_invalid_path():
    with pytest.raises(FileNotFoundError): 
        filter_csv_data("non_existent.csv", column="y",threshold=50)
        
        

# Test Tool2: Matblotlib
# Check the functionality of scatter plot:
def test_scatter_plot_csv_columns_success(sample_csv):
    result = plot_csv_columns(sample_csv, x_column="x", y_column="y")

    assert "plot_path" in result
    assert os.path.exists(result["plot_path"])
    # clean the generated image 
    os.remove(result["plot_path"])

# Check the scatter plot with invalid column name:
def test_scatter_plot_csv_columns_invalid_column(sample_csv):
    with pytest.raises(KeyError):
        plot_csv_columns(sample_csv, x_column="a", y_column="b")

# Check the functionality of line plot:        
def test_line_plot_csv_columns_success(sample_csv):
    result = plot_csv_columns(sample_csv, x_column="x", y_column="y")

    assert "plot_path" in result
    assert os.path.exists(result["plot_path"])
    # clean the generated image 
    os.remove(result["plot_path"])

# Check the functionality of line plot with invalid column name: 
def test_line_plot_csv_columns_invalid_column(sample_csv):
    with pytest.raises(KeyError):
        plot_csv_columns(sample_csv, x_column="a", y_column="b")
