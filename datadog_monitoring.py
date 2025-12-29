"""
Datadog Monitoring and Case Management Integration
- Monitor creation for Denial of Wallet (DoW) detection
- Case creation for prompt injection detection
"""

import os
import json
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.model.monitor import Monitor
from datadog_api_client.v1.model.monitor_type import MonitorType
from datadog_api_client.v1.model.monitor_options import MonitorOptions
from datadog_api_client.v1.model.monitor_thresholds import MonitorThresholds

# Cases API imports - may not be available in all versions
try:
    from datadog_api_client.v2.api.cases_api import CasesApi
    from datadog_api_client.v2.model.case_create import CaseCreate
    from datadog_api_client.v2.model.case_create_attributes import CaseCreateAttributes
    from datadog_api_client.v2.model.case_create_relationships import CaseCreateRelationships
    from datadog_api_client.v2.model.case_create_relationships_assignee import CaseCreateRelationshipsAssignee
    from datadog_api_client.v2.model.case_create_relationships_assignee_data import CaseCreateRelationshipsAssigneeData
    CASES_API_AVAILABLE = True
except ImportError:
    # Cases API not available in this version of datadog-api-client
    CASES_API_AVAILABLE = False


def get_datadog_config() -> Configuration:
    """
    Initialize Datadog API configuration from environment variables.
    
    Returns:
        Configured Datadog Configuration object
    """
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


def create_dow_monitor(
    threshold: int = 100000,
    evaluation_window: str = "last_5m",
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a Datadog monitor for Denial of Wallet (DoW) attack detection.
    
    This monitor alerts when llm.usage.total_tokens exceeds a threshold,
    indicating potential DoW attacks.
    
    Args:
        threshold: Token threshold to trigger alert (default: 100000)
        evaluation_window: Time window for evaluation (default: "last_5m")
        api_key: Datadog API key (optional, uses DD_API_KEY env var if not provided)
        app_key: Datadog Application key (optional, uses DD_APP_KEY env var if not provided)
        site: Datadog site (optional, uses DD_SITE env var if not provided)
    
    Returns:
        Dictionary containing monitor creation response
    """
    # Temporarily override env vars if provided
    if api_key:
        os.environ["DD_API_KEY"] = api_key
    if app_key:
        os.environ["DD_APP_KEY"] = app_key
    if site:
        os.environ["DD_SITE"] = site
    
    configuration = get_datadog_config()
    
    with ApiClient(configuration) as api_client:
        monitors_api = MonitorsApi(api_client)
        
        query = f"sum({evaluation_window}):sum:llm.usage.total_tokens{{*}}.as_count() > {threshold}"
        
        monitor = Monitor(
            type=MonitorType("metric alert"),
            query=query,
            name="LLM Denial of Wallet (DoW) Attack Detection",
            message=(
                f"Alert: Potential Denial of Wallet attack detected. "
                f"Total LLM tokens exceeded threshold of {threshold:,} in the {evaluation_window}. "
                f"This may indicate an attacker attempting to exhaust API quota by generating excessive token usage.\n\n"
                f"@slack-alerts @email-security-team"
            ),
            tags=["llm", "security", "dow", "denial-of-wallet"],
            options=MonitorOptions(
                notify_audit=True,
                require_full_window=False,
                notify_no_data=False,
                renotify_interval=60,
                escalation_message=(
                    "Escalation: DoW attack still active. "
                    "Consider rate limiting or blocking suspicious user sessions."
                ),
                thresholds=MonitorThresholds(
                    critical=float(threshold),
                    warning=float(threshold * 0.5)
                ),
                evaluation_delay=0,
                new_host_delay=300,
                include_tags=True
            ),
            priority=1
        )
        
        try:
            response = monitors_api.create_monitor(monitor)
            return {
                "success": True,
                "monitor_id": response.id,
                "message": f"Monitor created successfully with ID: {response.id}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create monitor: {e}"
            }


def create_prompt_injection_case(
    user_id: str,
    offending_prompt: str,
    additional_context: Optional[Dict[str, Any]] = None,
    assignee_id: Optional[str] = None,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a Datadog Case in Case Management when prompt injection is detected.
    
    Args:
        user_id: ID of the user who triggered the prompt injection
        offending_prompt: The prompt string that was flagged as injection
        additional_context: Optional dictionary with additional context (e.g., timestamp, session_id)
        assignee_id: Optional Datadog user ID to assign the case to
        api_key: Datadog API key (optional, uses DD_API_KEY env var if not provided)
        app_key: Datadog Application key (optional, uses DD_APP_KEY env var if not provided)
        site: Datadog site (optional, uses DD_SITE env var if not provided)
    
    Returns:
        Dictionary containing case creation response
    """
    if not CASES_API_AVAILABLE:
        return {
            "success": False,
            "error": "Cases API not available in this version of datadog-api-client",
            "message": "Cases API is not available. Please use Datadog API directly or upgrade datadog-api-client."
        }
    
    # Temporarily override env vars if provided
    if api_key:
        os.environ["DD_API_KEY"] = api_key
    if app_key:
        os.environ["DD_APP_KEY"] = app_key
    if site:
        os.environ["DD_SITE"] = site
    
    configuration = get_datadog_config()
    
    with ApiClient(configuration) as api_client:
        cases_api = CasesApi(api_client)
        
        # Build case title and description
        title = f"Prompt Injection Detected - User: {user_id}"
        
        description = f"""**Prompt Injection Security Alert**

**User ID:** {user_id}
**Offending Prompt:** 
```
{offending_prompt[:500]}{'...' if len(offending_prompt) > 500 else ''}
```

**Full Prompt Length:** {len(offending_prompt)} characters

**Action Required:**
- Review user session and activity
- Consider blocking or rate limiting this user
- Investigate for potential security breach
"""
        
        # Add additional context if provided
        if additional_context:
            description += "\n**Additional Context:**\n"
            for key, value in additional_context.items():
                description += f"- **{key}:** {value}\n"
        
        # Build case attributes
        attributes = CaseCreateAttributes(
            title=title,
            description=description,
            priority="high",
            state="open"
        )
        
        # Build relationships (assignee if provided)
        relationships = None
        if assignee_id:
            relationships = CaseCreateRelationships(
                assignee=CaseCreateRelationshipsAssignee(
                    data=CaseCreateRelationshipsAssigneeData(
                        id=assignee_id,
                        type="users"
                    )
                )
            )
        
        case_create = CaseCreate(
            attributes=attributes,
            relationships=relationships
        )
        
        try:
            response = cases_api.create_case(case_create)
            return {
                "success": True,
                "case_id": response.data.id,
                "case_number": getattr(response.data.attributes, "case_number", None),
                "message": f"Case created successfully with ID: {response.data.id}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create case: {e}"
            }


def load_monitor_from_json(json_path: str) -> Dict[str, Any]:
    """
    Load monitor definition from JSON file.
    
    Args:
        json_path: Path to JSON file containing monitor definition
    
    Returns:
        Dictionary containing monitor definition
    """
    with open(json_path, 'r') as f:
        return json.load(f)


def create_monitor_from_json(
    json_path: str,
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a Datadog monitor from a JSON definition file.
    
    Args:
        json_path: Path to JSON file containing monitor definition
        api_key: Datadog API key (optional, uses DD_API_KEY env var if not provided)
        app_key: Datadog Application key (optional, uses DD_APP_KEY env var if not provided)
        site: Datadog site (optional, uses DD_SITE env var if not provided)
    
    Returns:
        Dictionary containing monitor creation response
    """
    monitor_def = load_monitor_from_json(json_path)
    
    # Temporarily override env vars if provided
    if api_key:
        os.environ["DD_API_KEY"] = api_key
    if app_key:
        os.environ["DD_APP_KEY"] = app_key
    if site:
        os.environ["DD_SITE"] = site
    
    configuration = get_datadog_config()
    
    with ApiClient(configuration) as api_client:
        monitors_api = MonitorsApi(api_client)
        
        monitor = Monitor(**monitor_def)
        
        try:
            response = monitors_api.create_monitor(monitor)
            return {
                "success": True,
                "monitor_id": response.id,
                "message": f"Monitor created successfully with ID: {response.id}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create monitor: {e}"
            }


# Example usage and testing functions
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "create-monitor":
        # Create DoW monitor
        result = create_dow_monitor(threshold=100000)
        print(json.dumps(result, indent=2))
    
    elif len(sys.argv) > 1 and sys.argv[1] == "create-case":
        # Example: Create a prompt injection case
        if len(sys.argv) < 4:
            print("Usage: python datadog_monitoring.py create-case <user_id> <offending_prompt>")
            sys.exit(1)
        
        user_id = sys.argv[2]
        prompt = sys.argv[3]
        
        context = {
            "detection_timestamp": "2025-01-01T12:00:00Z",
            "session_id": "session_12345",
            "ip_address": "192.168.1.100"
        }
        
        result = create_prompt_injection_case(
            user_id=user_id,
            offending_prompt=prompt,
            additional_context=context
        )
        print(json.dumps(result, indent=2))
    
    else:
        print("Usage:")
        print("  python datadog_monitoring.py create-monitor")
        print("  python datadog_monitoring.py create-case <user_id> <offending_prompt>")

