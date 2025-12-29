# API Keys and Environment Variables Setup

## Required API Keys

### 1. Google Gemini API Key
- **Variable Name:** `GEMINI_API_KEY`
- **Purpose:** Authenticate with Google's Generative AI (Gemini) service
- **How to Get:**
  1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
  2. Sign in with your Google account
  3. Click "Create API Key"
  4. Copy the generated key

### 2. Datadog API Key
- **Variable Name:** `DD_API_KEY`
- **Purpose:** 
  - Send traces and metrics to Datadog
  - Authenticate API requests for creating monitors and cases
- **How to Get:**
  1. Log in to your Datadog account
  2. Go to **Organization Settings** → **API Keys**
  3. Click **New Key**
  4. Give it a name (e.g., "LLM Observability")
  5. Copy the generated key

### 3. Datadog Application Key
- **Variable Name:** `DD_APP_KEY`
- **Purpose:** Authenticate API requests for creating monitors and cases (read/write operations)
- **How to Get:**
  1. Log in to your Datadog account
  2. Go to **Organization Settings** → **Application Keys**
  3. Click **New Key**
  4. Give it a name (e.g., "LLM Monitoring")
  5. Copy the generated key

## Optional Environment Variables

### Datadog Configuration
- **`DD_SITE`**: Your Datadog site (default: `datadoghq.com`)
  - US: `datadoghq.com`
  - EU: `datadoghq.eu`
  - US3: `us3.datadoghq.com`
  - US5: `us5.datadoghq.com`
  - AP1: `ap1.datadoghq.com`

- **`DD_SERVICE`**: Service name for traces (default: `gemini-chat-app`)
- **`DD_ENV`**: Environment name (default: `development`)

### Gemini Configuration
- **`GEMINI_MODEL`**: Model to use (default: `gemini-pro`)
  - Options: `gemini-pro`, `gemini-pro-vision`, etc.

### Application Configuration
- **`USER_ID`**: User identifier for prompt injection detection (default: `anonymous`)
- **`DOW_THRESHOLD`**: Token threshold for DoW monitor (default: `100000`)

## Setting Environment Variables

### Windows PowerShell
```powershell
$env:GEMINI_API_KEY="your-gemini-api-key"
$env:DD_API_KEY="your-datadog-api-key"
$env:DD_APP_KEY="your-datadog-app-key"
$env:DD_SITE="datadoghq.com"
```

### Windows Command Prompt
```cmd
set GEMINI_API_KEY=your-gemini-api-key
set DD_API_KEY=your-datadog-api-key
set DD_APP_KEY=your-datadog-app-key
set DD_SITE=datadoghq.com
```

### Linux/macOS
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export DD_API_KEY="your-datadog-api-key"
export DD_APP_KEY="your-datadog-app-key"
export DD_SITE="datadoghq.com"
```

### Using .env file (recommended)
Create a `.env` file in the project directory:
```
GEMINI_API_KEY=your-gemini-api-key
DD_API_KEY=your-datadog-api-key
DD_APP_KEY=your-datadog-app-key
DD_SITE=datadoghq.com
DD_SERVICE=gemini-chat-app
DD_ENV=development
```

Then use `python-dotenv` to load it:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Quick Setup Checklist

- [ ] Get Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- [ ] Get Datadog API key from Datadog → Organization Settings → API Keys
- [ ] Get Datadog Application key from Datadog → Organization Settings → Application Keys
- [ ] Set environment variables (or create `.env` file)
- [ ] Verify keys are set: `echo $env:DD_API_KEY` (PowerShell) or `echo $DD_API_KEY` (bash)

## Security Notes

⚠️ **Never commit API keys to version control!**
- Add `.env` to `.gitignore`
- Use environment variables or secure secret management
- Rotate keys regularly
- Use different keys for development and production

