#!/usr/bin/env python3
"""
MCP Server Status Checker and Launcher
=====================================

This script helps you:
1. Check if the MCP server is running
2. Start the server in different modes
3. Test server connectivity
4. Monitor server status
"""

import os
import sys
import json
import subprocess
import time
import signal
import threading

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def check_server_process():
    """Check if the server process is running."""
    print_header("Checking Server Process")
    
    try:
        # Check for Python processes running the server
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True
        )
        
        server_processes = []
        for line in result.stdout.split('\n'):
            if 'server.py' in line and 'python' in line:
                server_processes.append(line.strip())
        
        if server_processes:
            print("✅ Found running server processes:")
            for proc in server_processes:
                print(f"   📋 {proc}")
            return True
        else:
            print("❌ No server processes found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking processes: {e}")
        return False

def check_server_ports():
    """Check if server ports are in use."""
    print_header("Checking Server Ports")
    
    try:
        # Check for common MCP server ports
        ports_to_check = [8000, 8080, 3000]
        
        for port in ports_to_check:
            result = subprocess.run(
                ["netstat", "-tuln"], 
                capture_output=True, 
                text=True
            )
            
            if f":{port}" in result.stdout:
                print(f"✅ Port {port} is in use (possible server)")
            else:
                print(f"❌ Port {port} is available")
                
    except Exception as e:
        print(f"❌ Error checking ports: {e}")

def test_server_import():
    """Test if the server can be imported and initialized."""
    print_header("Testing Server Import")
    
    try:
        # Test importing the server module
        import server
        print("✅ Server module imported successfully")
        
        # Test importing MCP handlers
        import mcp_handlers
        print("✅ MCP handlers imported successfully")
        
        # Test importing capabilities
        from capabilities.slurm_handler import _check_slurm_available
        slurm_available = _check_slurm_available()
        print(f"✅ Slurm capabilities available: {slurm_available}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def start_server_stdio():
    """Start the server in stdio mode (for MCP clients)."""
    print_header("Starting Server in STDIO Mode")
    
    print("🚀 Starting MCP server in STDIO mode...")
    print("   This mode is for MCP client connections")
    print("   The server will communicate via stdin/stdout")
    print("   Press Ctrl+C to stop")
    
    try:
        os.chdir(os.path.dirname(__file__))
        os.environ["MCP_TRANSPORT"] = "stdio"
        
        # Start the server
        process = subprocess.Popen(
            [sys.executable, "src/server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"✅ Server started with PID: {process.pid}")
        print("📡 Server is listening for MCP protocol messages on stdio")
        print("🔧 To test: echo '{}' | python src/server.py")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def start_server_sse():
    """Start the server in SSE mode (for web clients)."""
    print_header("Starting Server in SSE Mode")
    
    print("🚀 Starting MCP server in SSE mode...")
    print("   This mode is for web-based clients")
    print("   Server will be accessible via HTTP")
    
    try:
        os.chdir(os.path.dirname(__file__))
        os.environ["MCP_TRANSPORT"] = "sse"
        os.environ["MCP_SSE_HOST"] = "0.0.0.0"
        os.environ["MCP_SSE_PORT"] = "8000"
        
        # Start the server
        process = subprocess.Popen(
            [sys.executable, "src/server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"✅ Server started with PID: {process.pid}")
        print("🌐 Server should be accessible at: http://localhost:8000")
        print("📡 Waiting for server to initialize...")
        
        # Give server time to start
        time.sleep(2)
        
        # Check if it's responding
        try:
            import requests
            response = requests.get("http://localhost:8000", timeout=5)
            print(f"✅ Server is responding! Status: {response.status_code}")
        except:
            print("⚠️  Server started but not yet responding (may need more time)")
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def test_server_functionality():
    """Test server functionality by calling MCP handlers directly."""
    print_header("Testing Server Functionality")
    
    try:
        # Import and test MCP handlers
        from mcp_handlers import get_slurm_info_handler, list_slurm_jobs_handler
        
        print("🧪 Testing cluster information...")
        cluster_info = get_slurm_info_handler()
        print(f"✅ Cluster info: {json.dumps(cluster_info, indent=2)}")
        
        print("\n🧪 Testing job listing...")
        jobs = list_slurm_jobs_handler()
        print(f"✅ Jobs: {json.dumps(jobs, indent=2)}")
        
        print("\n✅ Server functionality test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def monitor_server(process):
    """Monitor a running server process."""
    print_header("Monitoring Server")
    
    print(f"👀 Monitoring server process {process.pid}...")
    print("   Press Ctrl+C to stop monitoring")
    
    try:
        while True:
            # Check if process is still running
            poll = process.poll()
            if poll is not None:
                print(f"❌ Server process ended with code: {poll}")
                break
            
            print(f"✅ Server process {process.pid} is running...")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping monitoring...")
        
    return process

def main():
    """Main function to check and manage server status."""
    print("🎯 MCP Server Status Checker and Launcher")
    print("=" * 60)
    
    # Check current status
    is_running = check_server_process()
    check_server_ports()
    can_import = test_server_import()
    
    if not can_import:
        print("\n❌ Server cannot be imported. Please check the installation.")
        return 1
    
    # Test functionality
    test_server_functionality()
    
    # Show options
    print_header("Server Management Options")
    print("""
    How to start the MCP server:
    
    1. 📡 STDIO Mode (for MCP clients):
       python src/server.py
       
    2. 🌐 SSE Mode (for web clients):
       MCP_TRANSPORT=sse MCP_SSE_PORT=8000 python src/server.py
       
    3. 🔧 Interactive Mode:
       Choose an option below
    """)
    
    # Interactive menu
    while True:
        print("\nChoose an action:")
        print("1. Start server in STDIO mode")
        print("2. Start server in SSE mode") 
        print("3. Check server status again")
        print("4. Test server functionality")
        print("5. Exit")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == "1":
                process = start_server_stdio()
                if process:
                    monitor_server(process)
                    
            elif choice == "2":
                process = start_server_sse()
                if process:
                    monitor_server(process)
                    
            elif choice == "3":
                check_server_process()
                check_server_ports()
                
            elif choice == "4":
                test_server_functionality()
                
            elif choice == "5":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice, please try again")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return 0

if __name__ == "__main__":
    exit(main())
