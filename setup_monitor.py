"""
Script to set up the Denial of Wallet (DoW) monitor in Datadog
"""

import os
import sys
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    # python-dotenv not installed, environment variables must be set manually
    pass

from datadog_monitoring import create_dow_monitor, create_monitor_from_json


def main():
    """
    Create the DoW monitor either programmatically or from JSON.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "from-json":
        # Create monitor from JSON file
        json_path = "monitor_dow.json"
        if not os.path.exists(json_path):
            print(f"Error: {json_path} not found")
            sys.exit(1)
        
        print(f"Creating monitor from {json_path}...")
        result = create_monitor_from_json(json_path)
    else:
        # Create monitor programmatically
        threshold = int(os.getenv("DOW_THRESHOLD", "100000"))
        print(f"Creating DoW monitor with threshold: {threshold:,} tokens...")
        result = create_dow_monitor(threshold=threshold)
    
    if result.get("success"):
        print(f"[SUCCESS] {result.get('message')}")
        print(f"   Monitor ID: {result.get('monitor_id')}")
    else:
        print(f"[ERROR] {result.get('message')}")
        if result.get("error"):
            print(f"   Error: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()

