# Quick Start Guide - Getting Data into Datadog

## To Get LLM Metrics Showing in Your Monitor:

### Option 1: Run with ddtrace-run (Recommended)

**Windows PowerShell:**
```powershell
cd C:\Users\paruc\OneDrive\Desktop\Code\DatadogChallenge\DatadogHackathon
$env:DD_API_KEY="your-datadog-api-key"
$env:DD_SITE="datadoghq.com"
$env:DD_LLMOBS_ENABLED="1"
$env:DD_SERVICE="gemini-chat-app"
ddtrace-run python app.py
```

**Windows Command Prompt:**
```cmd
cd C:\Users\paruc\OneDrive\Desktop\Code\DatadogChallenge\DatadogHackathon
set DD_API_KEY=your-datadog-api-key
set DD_SITE=datadoghq.com
set DD_LLMOBS_ENABLED=1
set DD_SERVICE=gemini-chat-app
ddtrace-run python app.py
```

**Or use the batch file:**
```cmd
run_app.bat
```

### Option 2: Run the Example Integration (with Security)

```powershell
$env:DD_API_KEY="your-datadog-api-key"
$env:DD_LLMOBS_ENABLED="1"
ddtrace-run python example_integration.py
```

## What Happens:

1. **ddtrace-run** automatically instruments your Gemini API calls
2. When you make chat requests, it captures:
   - Token usage (input/output tokens)
   - Latency
   - Model metadata
   - Request/response data

3. Metrics are sent to Datadog as `llm.usage.total_tokens`
4. Your monitor will start showing data within 1-2 minutes

## Test It:

1. Run the app with ddtrace-run
2. Type a few messages to generate LLM calls
3. Wait 1-2 minutes
4. Check your monitor: https://app.datadoghq.com/monitors/247042971

## Verify Data is Flowing:

```bash
python view_monitor.py 247042971
```

The status should change from "No Data" to "OK" once metrics start flowing.

