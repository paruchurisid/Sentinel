"""
Example integration showing how to use prompt injection detection
with Datadog case creation in the chat application
"""

import os
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    # python-dotenv not installed, environment variables must be set manually
    pass

from app import initialize_gemini, chat
from prompt_injection_detector import handle_prompt_injection


def main():
    """
    Enhanced main function with prompt injection detection and Datadog case creation.
    """
    print("Initializing Gemini client...")
    client = initialize_gemini()
    
    # Get user ID (in production, this would come from authentication)
    user_id = os.getenv("USER_ID", "anonymous")
    
    print("\nGemini Chat Application with Security Monitoring")
    print("Type 'exit' or 'quit' to end the conversation\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Check for prompt injection before processing
            injection_result = handle_prompt_injection(
                prompt=user_input,
                user_id=user_id,
                create_case=True,
                additional_context={
                    "source": "chat_application",
                    "session_type": "interactive"
                }
            )
            
            if injection_result["injection_detected"]:
                print(f"\n[SECURITY ALERT] Potential prompt injection detected!")
                print(f"   Pattern matched: {injection_result.get('matched_pattern', 'N/A')}")
                
                if injection_result.get("case_created"):
                    print(f"   [SUCCESS] Datadog case created: {injection_result.get('case_id')}")
                else:
                    print(f"   [WARNING] Failed to create case: {injection_result.get('case_error', 'Unknown error')}")
                
                # Optionally block the request or allow with warning
                response = "I cannot process this request due to security concerns."
                print(f"\nGemini: {response}\n")
                continue
            
            # Process normal request
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

