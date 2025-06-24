#!/usr/bin/env python3
"""
Comprehensive Node Allocation Test Script
Tests the Slurm node allocation capabilities including salloc functionality.
"""
import sys
import os
import json
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from capabilities.node_allocation import allocate_nodes, deallocate_nodes, get_allocation_status
    from capabilities.utils import check_slurm_available
    from mcp_handlers import allocate_nodes_handler, deallocate_nodes_handler
    print("✅ Successfully imported node allocation modules")
except ImportError as e:
    print(f"❌ Failed to import node allocation modules: {e}")
    sys.exit(1)

def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*70}")
    print(f"🎯 {title}")
    print(f"{'='*70}")

def print_result(title, result):
    """Print formatted result."""
    print(f"\n📋 {title}:")
    print("-" * 60)
    print(json.dumps(result, indent=2, default=str))
    print("-" * 60)

def test_slurm_availability():
    """Test if Slurm is available for node allocation."""
    print_section("Testing Slurm Availability")
    
    available = check_slurm_available()
    print(f"Slurm available: {available}")
    
    if not available:
        print("❌ Slurm not available - cannot test node allocation")
        return False
    
    print("✅ Slurm is available for testing")
    return True

def test_basic_node_allocation():
    """Test basic node allocation functionality."""
    print_section("Testing Basic Node Allocation")
    
    print("🔄 Requesting basic allocation (1 node, 1 core, 10 minutes, immediate=True)...")
    result = allocate_nodes(
        nodes=1, 
        cores=1, 
        time_limit="00:10:00", 
        immediate=True
    )
    
    print_result("Basic Allocation Result", result)
    
    # Return allocation ID if successful for cleanup
    if result.get("status") == "allocated" and "allocation_id" in result:
        print("✅ Basic node allocation successful!")
        return result["allocation_id"]
    elif result.get("status") == "timeout":
        print("⏰ Allocation timed out - this may be normal if resources are busy")
        return None
    elif result.get("status") == "failed":
        print(f"❌ Basic allocation failed: {result.get('error', 'Unknown error')}")
        return None
    else:
        print(f"⚠️  Unexpected allocation status: {result.get('status', 'Unknown')}")
        return None

def test_mcp_handler_allocation():
    """Test allocation through MCP handlers."""
    print_section("Testing MCP Handler Allocation")
    
    print("🔄 Testing allocation through MCP handler...")
    result = allocate_nodes_handler(
        nodes=1,
        cores=1,
        memory="1G",
        time_limit="00:05:00",
        immediate=True
    )
    
    print_result("MCP Handler Allocation Result", result)
    
    if isinstance(result, dict) and "allocation_id" in result:
        print("✅ MCP handler allocation successful!")
        return result["allocation_id"]
    else:
        print(f"❌ MCP handler allocation failed or returned unexpected format")
        return None

def test_allocation_status(allocation_id):
    """Test allocation status checking."""
    if not allocation_id:
        print("⚠️  No allocation ID provided, skipping status test")
        return
        
    print_section("Testing Allocation Status")
    
    print(f"🔄 Checking status for allocation {allocation_id}...")
    status_result = get_allocation_status(allocation_id)
    
    print_result("Allocation Status", status_result)
    
    expected_fields = ["allocation_id", "status", "real_slurm"]
    missing_fields = [field for field in expected_fields if field not in status_result]
    
    if missing_fields:
        print(f"⚠️  Missing expected fields: {missing_fields}")
    else:
        print("✅ Status check completed with all expected fields")

def test_deallocation(allocation_id):
    """Test node deallocation."""
    if not allocation_id:
        print("⚠️  No allocation ID provided, skipping deallocation test")
        return
        
    print_section("Testing Node Deallocation")
    
    print(f"🔄 Deallocating allocation {allocation_id}...")
    dealloc_result = deallocate_nodes(allocation_id)
    
    print_result("Deallocation Result", dealloc_result)
    
    if dealloc_result.get("status") == "deallocated":
        print("✅ Deallocation successful!")
    elif dealloc_result.get("status") == "not_found":
        print("⚠️  Allocation not found (may have already completed)")
    else:
        print(f"❌ Deallocation failed: {dealloc_result.get('error', 'Unknown error')}")

def test_immediate_vs_blocking():
    """Test difference between immediate and blocking allocation."""
    print_section("Testing Immediate vs Blocking Allocation")
    
    # Test immediate allocation (should return quickly)
    print("🔄 Testing immediate allocation...")
    start_time = time.time()
    immediate_result = allocate_nodes(
        nodes=1, 
        cores=1, 
        time_limit="00:05:00", 
        immediate=True
    )
    immediate_time = time.time() - start_time
    
    print(f"⏱️  Immediate allocation took {immediate_time:.2f} seconds")
    print_result("Immediate Allocation", immediate_result)
    
    # Clean up if successful
    if immediate_result.get("allocation_id"):
        deallocate_nodes(immediate_result["allocation_id"])
    
    # Test blocking allocation (may take longer)
    print("\n🔄 Testing blocking allocation...")
    start_time = time.time()
    blocking_result = allocate_nodes(
        nodes=1, 
        cores=1, 
        time_limit="00:05:00", 
        immediate=False
    )
    blocking_time = time.time() - start_time
    
    print(f"⏱️  Blocking allocation took {blocking_time:.2f} seconds")
    print_result("Blocking Allocation", blocking_result)
    
    # Clean up if successful
    if blocking_result.get("allocation_id"):
        deallocate_nodes(blocking_result["allocation_id"])
    
    print(f"\n📊 Performance comparison:")
    print(f"   Immediate: {immediate_time:.2f}s")
    print(f"   Blocking:  {blocking_time:.2f}s")

def run_comprehensive_test():
    """Run all node allocation tests."""
    print("🚀 COMPREHENSIVE NODE ALLOCATION TEST")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Check Slurm availability
    if not test_slurm_availability():
        print("\n❌ Cannot proceed without Slurm")
        return
    
    allocation_id = None
    
    try:
        # Test 2: Basic allocation
        allocation_id = test_basic_node_allocation()
        
        # Test 3: Status checking
        test_allocation_status(allocation_id)
        
        # Test 4: MCP handler
        mcp_allocation_id = test_mcp_handler_allocation()
        
        # Test 5: Immediate vs blocking
        test_immediate_vs_blocking()
        
        # Clean up MCP allocation if it exists
        if mcp_allocation_id:
            test_deallocation(mcp_allocation_id)
    
    finally:
        # Always try to clean up main allocation
        if allocation_id:
            test_deallocation(allocation_id)
    
    print_section("Test Summary")
    print("All node allocation tests completed!")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_comprehensive_test()
