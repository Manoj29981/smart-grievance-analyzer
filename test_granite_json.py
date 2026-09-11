import os
import json
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

grievance = """
The garbage bins near the college canteen have been overflowing
for the past 2 days and there is a bad smell around the area.
"""

messages = [
    {
        "role": "system",
        "content": """
You are an AI Smart Grievance Analyzer for sustainable campus management.

Analyze the user's campus grievance and return ONLY valid JSON.

The JSON must contain exactly these fields:

category
issue
location
duration
priority
responsible_department
sustainability_impact
recommended_action
summary

Allowed categories:
Water & Sanitation
Waste Management
Electricity & Energy
Infrastructure
Maintenance
Transportation
Environment
IT/Technical
Cleanliness
Other

Allowed priorities:
High
Medium
Low

Rules:
- Select exactly one allowed category.
- Select exactly one allowed priority.
- Do not invent facts.
- If information is missing, use "Not specified".
- The location should be extracted when it is present in the grievance.
- The responsible department may be inferred from the category.
- Sustainability impact should describe environmental or resource impact.
- Recommended action should be practical and concise.
- Summary should be one short sentence.
""",
    },
    {"role": "user", "content": grievance},
]

params = {
    "temperature": 0,
    "max_tokens": 300,
    "response_format": {"type": "json_object"},
}

response = model.chat(messages=messages, params=params)

content = response["choices"][0]["message"]["content"]

print("\n--- RAW GRANITE RESPONSE ---")
print(content)

print("\n--- PARSED JSON ---")

try:
    result = json.loads(content)
    print(json.dumps(result, indent=4))
except json.JSONDecodeError:
    print("ERROR: Granite did not return valid JSON.")
