import gzip
import os


async def handle_compression(params, req_id):
    filename = params.get("filename")
    if not filename or not os.path.exists(filename):
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32602, "message": "Invalid or missing 'filename'"}
        }

    compressed_file = filename + ".gz"
    try:
        with open(filename, 'rb') as f_in, gzip.open(compressed_file, 'wb') as f_out:
            f_out.writelines(f_in)

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "message": f"File compressed to {compressed_file}",
                "context": {"type": "compression"}
            }
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32001, "message": str(e)}
        }
