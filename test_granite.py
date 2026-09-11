import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONX_URL"), api_key=os.getenv("WATSONX_APIKEY")
)

model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
)

prompt = """
You are an AI Smart Grievance Analyzer for sustainable campus management.

Analyze the following campus grievance.

Grievance:
"There is a water leakage near Block B for the last 3 days."

Use ONLY these categories:
- Water & Sanitation
- Waste Management
- Electricity & Energy
- Infrastructure
- Maintenance
- Transportation
- Environment
- IT/Technical
- Cleanliness
- Other

Use ONLY these priority levels:
- High
- Medium
- Low

Return exactly these fields:

Category:
Issue:
Location:
Duration:
Priority:
Responsible Department:
Sustainability Impact:
Recommended Action:
Summary:

Rules:
1. Do not invent information that is not present in the grievance.
2. If information is missing, write "Not specified".
3. Choose exactly one category from the allowed categories.
4. Choose exactly one priority: High, Medium, or Low.
5. Keep the response concise and suitable for a campus administrator.
6. Do not add extra fields.
"""

response = model.generate_text(prompt=prompt, params={"max_new_tokens": 300})

print("\n--- GRANITE RESPONSE ---")
print(response)
