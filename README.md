# Sentinel

A security monitoring system for LLM applications with Google Gemini integration and Datadog observability. Detects prompt injection attacks and Denial of Wallet (DoW) threats.

## Features

- **Prompt Injection Detection**: Pattern-based detection of injection attempts with automatic Datadog case creation
- **Denial of Wallet (DoW) Monitoring**: Token usage monitoring to detect excessive API consumption
- **Datadog LLM Observability**: Automatic instrumentation with ddtrace for latency, token usage, and model metadata
- **Security Case Management**: Automatic case creation in Datadog when security threats are detected

## Prerequisites

- Python 3.8+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Datadog account with API and Application keys

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Sentinel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (see [API_KEYS_SETUP.md](API_KEYS_SETUP.md) for details):
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `DD_API_KEY`: Your Datadog API key
   - `DD_APP_KEY`: Your Datadog Application key
   - `DD_SITE`: Your Datadog site (default: `datadoghq.com`)

## Quick Start

### Option 1: Basic Chat Application

**Windows:**
```cmd
run_app.bat
```

**Linux/macOS:**
```bash
chmod +x run_app.sh
./run_app.sh
```

**Manual:**
```bash
set DD_LLMOBS_ENABLED=1
ddtrace-run python app.py
```

### Option 2: Chat with Security Monitoring

```bash
set DD_LLMOBS_ENABLED=1
ddtrace-run python example_integration.py
```

### Setup Datadog Monitor

Create the DoW monitor:
```bash
python setup_monitor.py
```

Or from JSON:
```bash
python setup_monitor.py from-json
```

## Usage

### Basic Chat

Run `app.py` for a simple chat interface with Gemini. All LLM calls are automatically instrumented and sent to Datadog.

### Security-Enhanced Chat

Run `example_integration.py` to enable prompt injection detection. When an injection attempt is detected:
- A security alert is displayed
- A Datadog case is automatically created
- The request is blocked

### View Monitor Status

```bash
python view_monitor.py <monitor_id>
```

## Project Structure

```
Sentinel/
├── app.py                      # Basic Gemini chat application
├── example_integration.py      # Chat with security monitoring
├── prompt_injection_detector.py # Injection detection logic
├── datadog_monitoring.py       # Datadog monitor and case management
├── setup_monitor.py            # Monitor setup script
├── view_monitor.py             # Monitor status viewer
├── requirements.txt            # Python dependencies
├── monitor_dow.json            # DoW monitor definition
├── API_KEYS_SETUP.md          # API key setup guide
└── QUICK_START.md             # Quick start guide
```

## Configuration

### Environment Variables

See [API_KEYS_SETUP.md](API_KEYS_SETUP.md) for complete configuration options.

**Required:**
- `GEMINI_API_KEY`
- `DD_API_KEY`
- `DD_APP_KEY`

**Optional:**
- `DD_SITE`: Datadog site (default: `datadoghq.com`)
- `DD_SERVICE`: Service name (default: `gemini-chat-app`)
- `DD_ENV`: Environment (default: `development`)
- `GEMINI_MODEL`: Model name (default: `gemini-2.0-flash-exp`)
- `DOW_THRESHOLD`: Token threshold for DoW monitor (default: `100000`)

### Using .env File

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-key
DD_API_KEY=your-key
DD_APP_KEY=your-key
DD_SITE=datadoghq.com
```

## Security Features

### Prompt Injection Detection

Detects common injection patterns:
- Instruction override attempts
- System prompt extraction
- Role-playing/jailbreak attempts
- Encoding-based attacks
- Token flooding

### Denial of Wallet Protection

Monitors total token usage and alerts when thresholds are exceeded, indicating potential DoW attacks.

## Monitoring

All LLM interactions are automatically tracked in Datadog:
- **Metrics**: Token usage, latency, request counts
- **Traces**: Full request/response traces
- **Monitors**: Automated DoW detection
- **Cases**: Security incident tracking

## Documentation

- [API_KEYS_SETUP.md](API_KEYS_SETUP.md) - API key configuration guide
- [QUICK_START.md](QUICK_START.md) - Quick start instructions

## License

[Add your license here]

