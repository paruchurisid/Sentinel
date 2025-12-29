"""
Quick test script to verify API keys and dependencies are set up correctly
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        from google import genai
        print("[OK] google-genai imported successfully")
    except ImportError as e:
        print(f"[ERROR] google-genai not found: {e}")
        return False
    
    try:
        import ddtrace
        print("[OK] ddtrace imported successfully")
    except ImportError as e:
        print(f"[ERROR] ddtrace not found: {e}")
        return False
    
    try:
        from datadog_api_client import ApiClient, Configuration
        print("[OK] datadog-api-client imported successfully")
    except ImportError as e:
        print(f"❌ datadog-api-client not found: {e}")
        return False
    
    return True

def test_env_vars():
    """Test if environment variables are set"""
    print("\nTesting environment variables...")
    
    gemini_key = os.getenv("GEMINI_API_KEY")
    dd_api_key = os.getenv("DD_API_KEY")
    dd_app_key = os.getenv("DD_APP_KEY")
    
    if gemini_key and gemini_key != "your-gemini-api-key-here":
        print(f"[OK] GEMINI_API_KEY is set (length: {len(gemini_key)})")
    else:
        print("[ERROR] GEMINI_API_KEY is not set or is placeholder")
    
    if dd_api_key and dd_api_key != "your-datadog-api-key-here":
        print(f"[OK] DD_API_KEY is set (length: {len(dd_api_key)})")
    else:
        print("[ERROR] DD_API_KEY is not set or is placeholder")
    
    if dd_app_key and dd_app_key != "your-datadog-app-key-here":
        print(f"[OK] DD_APP_KEY is set (length: {len(dd_app_key)})")
    else:
        print("[ERROR] DD_APP_KEY is not set or is placeholder")
    
    return all([
        gemini_key and gemini_key != "your-gemini-api-key-here",
        dd_api_key and dd_api_key != "your-datadog-api-key-here",
        dd_app_key and dd_app_key != "your-datadog-app-key-here"
    ])

def main():
    print("=" * 50)
    print("Python Environment Setup Test")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()
    
    imports_ok = test_imports()
    env_ok = test_env_vars()
    
    print("\n" + "=" * 50)
    if imports_ok and env_ok:
        print("[SUCCESS] All checks passed! You're ready to run the app.")
        print("\nTo run the app:")
        print("  python app.py")
        print("\nTo run with prompt injection detection:")
        print("  python example_integration.py")
    else:
        print("[ERROR] Some checks failed. Please fix the issues above.")
    print("=" * 50)

if __name__ == "__main__":
    main()

