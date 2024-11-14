from dotenv import load_dotenv
import os
# Load environment variables from .env file
def Api_init():
    load_dotenv()

    # Retrieve the API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set GROQ_API_KEY in your environment or .env file.")
    else:
        return(api_key)