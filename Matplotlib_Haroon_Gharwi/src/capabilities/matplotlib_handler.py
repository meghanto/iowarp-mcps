#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt


# Tool 1: Function to plot data as scatter plot from the loaded csv file and save the plot as an image
def plot_csv_columns(csv_path: str, x_column: str, y_column: str) -> dict:
    """
    Goal: Load the data file from the path and provide a scatter plot between columns x and y
    
    Input: csv_path: str, x_column: str, y_column: str
    
    Output: scatter plot path
    
    """
    
    # Load data from client file path:
    df = pd.read_csv(csv_path)
    
    
    # Create the scatter plot
    plt.figure()
    plt.scatter(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{x_column} vs {y_column}")
    
    # Save plot to path: images/plot.png
    save_dir = "images"
    save_filename = "plot.png"
    save_path = f"{save_dir}/{save_filename}"
    plt.savefig(save_path)
    plt.close()
    
    return {"plot_path": save_path}


# (Extra) Tool 2: Function to plot data as line plot from the loaded csv file and save the plot as an image
def line_plot_csv_columns(csv_path: str, x_column: str, y_column: str) -> dict:
    
    """
    Goal: Load the data file from the path and provide a line plot between columns x and y
    
    Input: csv_path: str, x_column: str, y_column: str
    
    Output: line plot path
    
    """
    
    # Load data from client file path:
    df = pd.read_csv(csv_path)
    
    ## Create the line plot
    plt.figure()
    plt.plot(df[x_column], df[y_column])
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{x_column} vs {y_column}")
    
    # Save plot to path: images/plot.png
    save_dir = "images"
    save_filename = "plot.png"
    save_path = f"{save_dir}/{save_filename}"
    plt.savefig(save_path)
    plt.close()
    
    return {"plot_path": save_path}