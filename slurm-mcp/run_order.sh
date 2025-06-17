#!/bin/bash
# Quick Start Guide - Run these commands one by one
# File: /home/sislam6/Illinois_Tech/PhD/Spring25_iit/CS550/scientific-mcps/slurm-mcp/

echo "🎯 SLURM MCP SERVER - FILES TO RUN IN ORDER"
echo "==========================================="
echo ""
echo "📂 Current Directory: $(pwd)"
echo ""

echo "1️⃣  CHECK SERVER STATUS"
echo "   File: server_manager.sh" 
echo "   Command: ./server_manager.sh status"
echo ""

echo "2️⃣  START THE SERVER"
echo "   File: server_manager.sh"
echo "   Command: ./server_manager.sh start"
echo ""

echo "3️⃣  VERIFY EVERYTHING WORKS"
echo "   File: final_verification.py"
echo "   Command: python final_verification.py"
echo ""

echo "4️⃣  RUN SIMPLE DEMO"
echo "   File: simple_job_demo.py"
echo "   Command: python simple_job_demo.py"
echo ""

echo "5️⃣  RUN COMPLETE DEMO"
echo "   File: complete_demo.py" 
echo "   Command: python complete_demo.py"
echo ""

echo "6️⃣  RUN ALL TESTS"
echo "   Directory: tests/"
echo "   Command: python -m pytest tests/ -v"
echo ""

echo "7️⃣  STOP SERVER WHEN DONE"
echo "   File: server_manager.sh"
echo "   Command: ./server_manager.sh stop"
echo ""

echo "📋 ALTERNATIVE DEMOS (Optional):"
echo "   • python quick_demo.py"
echo "   • python step_by_step_demo.py" 
echo "   • python practical_slurm_demo.py"
echo "   • python complete_server_demo.py"
echo ""

echo "🔧 MANAGEMENT FILES:"
echo "   • ./server_manager.sh [start|stop|status|logs|restart]"
echo "   • python server_status_checker.py (interactive)"
echo ""

echo "📚 DOCUMENTATION:"
echo "   • EXECUTION_ORDER.md (detailed guide)"
echo "   • SERVER_STATUS_GUIDE.md (troubleshooting)"
echo "   • COMPLETE_DEMO_RESULTS.md (previous results)"
echo ""

echo "⚠️  IMPORTANT:"
echo "   - Always start with: ./server_manager.sh status"
echo "   - Server must be running before demos"
echo "   - Check logs if issues: ./server_manager.sh logs"
echo "   - Stop cleanly: ./server_manager.sh stop"
