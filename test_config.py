import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WATSONX_APIKEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
url = os.getenv("WATSONX_URL")

print("API key loaded:", bool(api_key))
print("Project ID:", project_id)
print("Watsonx URL:", url)
