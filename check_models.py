import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONX_URL"), api_key=os.getenv("WATSONX_APIKEY")
)

project_id = os.getenv("WATSONX_PROJECT_ID")

model = ModelInference(
    model_id="ibm/granite-4-h-small", credentials=credentials, project_id=project_id
)

print("IBM watsonx connection object created successfully!")
print("Model: ibm/granite-4-h-small")
print("Project ID:", project_id)
