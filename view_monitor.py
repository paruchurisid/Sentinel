"""
Script to view and review the DoW monitor in Datadog
"""

import os
import sys
import json
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi


def get_datadog_config() -> Configuration:
    """Initialize Datadog API configuration"""
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")
    site = os.getenv("DD_SITE", "datadoghq.com")
    
    if not api_key:
        raise ValueError("DD_API_KEY environment variable must be set")
    if not app_key:
        raise ValueError("DD_APP_KEY environment variable must be set")
    
    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = api_key
    configuration.api_key["appKeyAuth"] = app_key
    configuration.server_variables["site"] = site
    
    return configuration


def list_monitors():
    """List all monitors, especially DoW monitors"""
    configuration = get_datadog_config()
    
    with ApiClient(configuration) as api_client:
        monitors_api = MonitorsApi(api_client)
        
        # Search for monitors with "dow" tag
        try:
            monitors = monitors_api.list_monitors(tags="dow,denial-of-wallet")
            
            print("=" * 60)
            print("DoW Monitors Found:")
            print("=" * 60)
            
            if not monitors:
                print("No monitors found with 'dow' or 'denial-of-wallet' tags")
                print("\nSearching all monitors...")
                monitors = monitors_api.list_monitors()
            
            for monitor in monitors:
                if "dow" in [tag.lower() for tag in (monitor.tags or [])] or "denial" in monitor.name.lower():
                    print(f"\nMonitor ID: {monitor.id}")
                    print(f"Name: {monitor.name}")
                    print(f"Query: {monitor.query}")
                    print(f"Status: {monitor.overall_state}")
                    print(f"Tags: {', '.join(monitor.tags or [])}")
                    print(f"URL: https://app.datadoghq.com/monitors/{monitor.id}")
                    print("-" * 60)
            
            return monitors
            
        except Exception as e:
            print(f"Error listing monitors: {e}")
            return []


def get_monitor_details(monitor_id: int):
    """Get detailed information about a specific monitor"""
    configuration = get_datadog_config()
    
    with ApiClient(configuration) as api_client:
        monitors_api = MonitorsApi(api_client)
        
        try:
            monitor = monitors_api.get_monitor(monitor_id=monitor_id)
            
            print("=" * 60)
            print(f"Monitor Details: {monitor.name}")
            print("=" * 60)
            print(f"ID: {monitor.id}")
            print(f"Name: {monitor.name}")
            print(f"Type: {monitor.type}")
            print(f"Query: {monitor.query}")
            print(f"Status: {monitor.overall_state}")
            print(f"Message: {monitor.message}")
            print(f"Tags: {', '.join(monitor.tags or [])}")
            print(f"\nOptions:")
            if monitor.options:
                print(f"  - Notify Audit: {monitor.options.notify_audit}")
                print(f"  - Require Full Window: {monitor.options.require_full_window}")
                if monitor.options.thresholds:
                    print(f"  - Critical Threshold: {monitor.options.thresholds.critical}")
                    print(f"  - Warning Threshold: {monitor.options.thresholds.warning}")
            
            print(f"\nDirect URL: https://app.datadoghq.com/monitors/{monitor.id}")
            print("=" * 60)
            
            return monitor
            
        except Exception as e:
            print(f"Error getting monitor details: {e}")
            return None


def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Get specific monitor by ID
        try:
            monitor_id = int(sys.argv[1])
            get_monitor_details(monitor_id)
        except ValueError:
            print(f"Invalid monitor ID: {sys.argv[1]}")
            print("Usage: python view_monitor.py [monitor_id]")
    else:
        # List all DoW monitors
        monitors = list_monitors()
        
        if monitors:
            print(f"\nFound {len(monitors)} monitor(s)")
            print("\nTo view details of a specific monitor, run:")
            print("  python view_monitor.py <monitor_id>")
            print("\nExample:")
            if monitors:
                print(f"  python view_monitor.py {monitors[0].id}")


if __name__ == "__main__":
    main()

