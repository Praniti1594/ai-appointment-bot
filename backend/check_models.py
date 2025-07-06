from google.generativeai import list_models, configure
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List available models and supported generation methods
for m in list_models():
    print(m.name, "->", m.supported_generation_methods)
