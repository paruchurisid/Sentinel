@echo off
REM Windows batch script to run the Python application with Datadog LLM Observability

REM Set Datadog environment variables
set DD_API_KEY=%DD_API_KEY%
set DD_SITE=%DD_SITE%
if "%DD_SITE%"=="" set DD_SITE=datadoghq.com
set DD_LLMOBS_ENABLED=1

REM Optional: Set service name and environment
set DD_SERVICE=%DD_SERVICE%
if "%DD_SERVICE%"=="" set DD_SERVICE=gemini-chat-app
set DD_ENV=%DD_ENV%
if "%DD_ENV%"=="" set DD_ENV=development

REM Optional: Enable additional tracing features
set DD_TRACE_ENABLED=true
set DD_LOGS_INJECTION=true

REM Check if GEMINI_API_KEY is set
if "%GEMINI_API_KEY%"=="" (
    echo Warning: GEMINI_API_KEY environment variable is not set.
    echo Please set it before running the application:
    echo   set GEMINI_API_KEY=your-gemini-api-key
    echo.
)

REM Run the application with ddtrace-run for auto-instrumentation
echo Starting application with Datadog LLM Observability...
ddtrace-run python app.py

