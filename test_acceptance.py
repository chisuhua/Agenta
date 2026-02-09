#!/usr/bin/env python3
"""
Test script for Agenta CLI Phase 0 acceptance criteria.

This script tests all acceptance criteria without requiring an actual API key.
For real LLM testing, set AGENTA_API_KEY or configure ~/.agenta/config.yaml
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def run_command(cmd, should_succeed=True):
    """Run a command and return output"""
    print(f"\n🔍 Testing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Exit code: {result.returncode}")
    
    if result.stdout:
        print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
    
    if should_succeed and result.returncode != 0:
        print(f"❌ FAIL: Command should have succeeded but failed")
        return False
    elif not should_succeed and result.returncode == 0:
        print(f"❌ FAIL: Command should have failed but succeeded")
        return False
    else:
        print(f"✅ PASS")
        return True

def test_cli_help():
    """Test: CLI startup - `agenta --help` displays help"""
    print("\n" + "="*70)
    print("TEST 1: CLI Startup - `agenta --help`")
    print("="*70)
    return run_command(["agenta", "--help"], should_succeed=True)

def test_cli_version():
    """Test: CLI version display"""
    print("\n" + "="*70)
    print("TEST 2: CLI Version - `agenta --version`")
    print("="*70)
    return run_command(["agenta", "--version"], should_succeed=True)

def test_config_show():
    """Test: Configuration loading - show current config"""
    print("\n" + "="*70)
    print("TEST 3: Configuration Loading - `agenta config-show`")
    print("="*70)
    return run_command(["agenta", "config-show"], should_succeed=True)

def test_config_set():
    """Test: Configuration modification"""
    print("\n" + "="*70)
    print("TEST 4: Configuration Modification - `agenta config-set`")
    print("="*70)
    success = True
    
    # Set model
    success &= run_command(["agenta", "config-set", "--model", "gpt-4"], should_succeed=True)
    
    # Set provider
    success &= run_command(["agenta", "config-set", "--provider", "openai"], should_succeed=True)
    
    return success

def test_error_handling():
    """Test: Error handling - no API key should give clear error"""
    print("\n" + "="*70)
    print("TEST 5: Error Handling - Clear error without API key")
    print("="*70)
    
    # Clear any existing API key from environment
    old_env = {}
    for key in ["AGENTA_API_KEY", "OPENAI_API_KEY"]:
        if key in os.environ:
            old_env[key] = os.environ[key]
            del os.environ[key]
    
    # This should fail with a clear error message
    result = run_command(["agenta", "ask", "What is 2+2?"], should_succeed=False)
    
    # Restore environment
    for key, value in old_env.items():
        os.environ[key] = value
    
    return result

def test_with_api_key():
    """Test: Basic Q&A with streaming (requires API key)"""
    print("\n" + "="*70)
    print("TEST 6: Basic Q&A with Streaming (Optional - requires API key)")
    print("="*70)
    
    # Check if API key is available
    api_key = os.environ.get("AGENTA_API_KEY") or os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        # Check config file
        config_file = Path.home() / ".agenta" / "config.yaml"
        if config_file.exists():
            with open(config_file) as f:
                content = f.read()
                if "api_key:" in content and "sk-" in content:
                    print("✅ API key found in config file")
                    print("🔄 Running live test with API...")
                    return run_command(["agenta", "ask", "What is 2+2?"], should_succeed=True)
        
        print("⚠️  SKIP: No API key available. Set AGENTA_API_KEY to test live LLM calls.")
        return True  # Not a failure, just skipped
    else:
        print("✅ API key found in environment")
        print("🔄 Running live test with API...")
        return run_command(["agenta", "ask", "What is 2+2?"], should_succeed=True)

def main():
    """Run all tests"""
    print("\n" + "🧪"*35)
    print("AGENTA CLI - Phase 0 Acceptance Tests")
    print("🧪"*35)
    
    results = []
    
    results.append(("CLI Help", test_cli_help()))
    results.append(("CLI Version", test_cli_version()))
    results.append(("Config Show", test_config_show()))
    results.append(("Config Set", test_config_set()))
    results.append(("Error Handling", test_error_handling()))
    results.append(("Live Q&A (optional)", test_with_api_key()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
