"""
Python application using Google Generative AI (Gemini) SDK
with Datadog LLM Observability integration
"""

import os
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    # python-dotenv not installed, environment variables must be set manually
    pass

from google import genai
from typing import Optional


def initialize_gemini(api_key: Optional[str] = None) -> genai.Client:
    """
    Initialize the Gemini client.
    
    Args:
        api_key: Google AI API key. If not provided, reads from GEMINI_API_KEY env var.
    
    Returns:
        Initialized genai.Client instance
    """
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable must be set or passed as argument"
        )
    
    # Initialize the client with API key
    client = genai.Client(api_key=api_key)
    
    return client


def chat(client: genai.Client, message: str) -> str:
    """
    Standard chat function that sends a message to Gemini and returns the response.
    
    This function will be auto-instrumented by ddtrace to capture:
    - Latency
    - Input/output tokens
    - Model metadata
    
    Args:
        client: Initialized genai.Client instance
        message: User message to send to the model
    
    Returns:
        Model response as a string
    """
    try:
        # Get model name from environment or use default
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        
        # Generate content using the new API
        response = client.models.generate_content(
            model=model_name,
            contents=message
        )
        return response.text
    except Exception as e:
        print(f"Error in chat function: {e}")
        raise


def main():
    """
    Main function to demonstrate the chat functionality.
    """
    print("Initializing Gemini client...")
    client = initialize_gemini()
    
    print("\nGemini Chat Application")
    print("Type 'exit' or 'quit' to end the conversation\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("Gemini: ", end="", flush=True)
            response = chat(client, user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()

