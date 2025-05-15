import pandas as pd
import matplotlib.pyplot as plt
import asyncio
import os


async def handle_plot(params, req_id):
    file_path = params.get("filename")
    x_col = params.get("x_column")
    y_col = params.get("y_column")

    if not all([file_path, x_col, y_col]) or not os.path.exists(file_path):
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32602, "message": "Missing or invalid filename or column names"}
        }

    try:
        await asyncio.sleep(0.5)  # Simulate async I/O
        df = pd.read_csv(file_path)

        if x_col not in df.columns or y_col not in df.columns:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": "Column names not found in file"}
            }

        plot_file = f"{x_col}_vs_{y_col}.png"
        df.plot(x=x_col, y=y_col)
        plt.title(f"{y_col} vs {x_col}")
        plt.savefig(plot_file)
        plt.close()

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "message": f"Plot saved as {plot_file}",
                "context": {
                    "type": "plot",
                    "x": x_col,
                    "y": y_col
                }
            }
        }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32001, "message": str(e)}
        }
