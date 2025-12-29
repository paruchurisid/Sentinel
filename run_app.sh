#!/bin/bash

# Shell script to run the Python application with Datadog LLM Observability
# This script sets the necessary environment variables and executes the app using ddtrace-run

# Set Datadog environment variables
export DD_API_KEY="${DD_API_KEY:-your-datadog-api-key-here}"
export DD_SITE="${DD_SITE:-datadoghq.com}"
export DD_LLMOBS_ENABLED=1

# Optional: Set service name and environment
export DD_SERVICE="${DD_SERVICE:-gemini-chat-app}"
export DD_ENV="${DD_ENV:-development}"

# Optional: Enable additional tracing features
export DD_TRACE_ENABLED=true
export DD_LOGS_INJECTION=true

# Check if GEMINI_API_KEY is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Warning: GEMINI_API_KEY environment variable is not set."
    echo "Please set it before running the application:"
    echo "  export GEMINI_API_KEY=your-gemini-api-key"
    echo ""
fi

# Run the application with ddtrace-run for auto-instrumentation
echo "Starting application with Datadog LLM Observability..."
ddtrace-run python app.py

