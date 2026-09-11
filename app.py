from flask import Flask, render_template, request, jsonify
import os
import json

from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from database import initialize_database, get_connection
from recurring import check_recurring_issue

load_dotenv()

app = Flask(__name__)


# Initialize database
initialize_database()


# IBM watsonx.ai credentials
credentials = Credentials(
    url=os.getenv("WATSONX_URL"), api_key=os.getenv("WATSONX_APIKEY")
)


# IBM Granite model
model = ModelInference(
    model_id="ibm/granite-4-h-small",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
)


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------


@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------------
# ADMIN DASHBOARD
# ---------------------------------------------------------


@app.route("/dashboard")
def dashboard():

    connection = get_connection()

    # Total grievances
    total_grievances = connection.execute("""
        SELECT COUNT(*) AS count
        FROM grievances
    """).fetchone()["count"]

    # High priority grievances
    high_priority = connection.execute("""
        SELECT COUNT(*) AS count
        FROM grievances
        WHERE priority = 'High'
    """).fetchone()["count"]

    # Medium priority grievances
    medium_priority = connection.execute("""
        SELECT COUNT(*) AS count
        FROM grievances
        WHERE priority = 'Medium'
    """).fetchone()["count"]

    # Low priority grievances
    low_priority = connection.execute("""
        SELECT COUNT(*) AS count
        FROM grievances
        WHERE priority = 'Low'
    """).fetchone()["count"]

    # Recurring grievances
    recurring_issues = connection.execute("""
        SELECT COUNT(*) AS count
        FROM grievances
        WHERE recurring_issue = 1
    """).fetchone()["count"]

    # Category distribution
    categories = connection.execute("""
        SELECT
            category,
            COUNT(*) AS count
        FROM grievances
        GROUP BY category
        ORDER BY count DESC
    """).fetchall()

    # Recent grievances
    recent_grievances = connection.execute("""
    SELECT
        id,
        category,
        issue,
        location,
        priority,
        recurring_issue,
        status,
        created_at
    FROM grievances
    ORDER BY id DESC
    LIMIT 10
""").fetchall()

    sustainability_insights = connection.execute("""
    SELECT
        category,
        issue,
        location,
        sustainability_impact,
        recommended_action,
        recurring_issue
    FROM grievances
    WHERE sustainability_impact IS NOT NULL
      AND sustainability_impact != ''
    ORDER BY recurring_issue DESC, id DESC
    LIMIT 5
""").fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        total_grievances=total_grievances,
        high_priority=high_priority,
        medium_priority=medium_priority,
        low_priority=low_priority,
        recurring_issues=recurring_issues,
        categories=categories,
        recent_grievances=recent_grievances,
        sustainability_insights=sustainability_insights,
    )


@app.route("/check_status", methods=["POST"])
def check_status():
    data = request.get_json()

    grievance_id = str(data.get("grievance_id", "")).strip().upper()

    if not grievance_id:
        return jsonify({"error": "Please enter a Grievance ID."}), 400

    # Accept IDs such as SGA-001, SGA-005, etc.
    if not grievance_id.startswith("SGA-"):
        return (
            jsonify(
                {"error": "Invalid Grievance ID. Please use a format like SGA-001."}
            ),
            400,
        )

    try:
        numeric_id = int(grievance_id.replace("SGA-", ""))
    except ValueError:
        return (
            jsonify(
                {"error": "Invalid Grievance ID. Please use a format like SGA-001."}
            ),
            400,
        )

    connection = get_connection()

    grievance = connection.execute(
        """
        SELECT
            id,
            category,
            issue,
            location,
            priority,
            responsible_department,
            status,
            created_at
        FROM grievances
        WHERE id = ?
    """,
        (numeric_id,),
    ).fetchone()

    connection.close()

    if not grievance:
        return (
            jsonify(
                {"error": "Grievance ID not found. Please check the ID and try again."}
            ),
            404,
        )

    return jsonify(
        {
            "grievance_id": f"SGA-{grievance['id']:03d}",
            "category": grievance["category"],
            "issue": grievance["issue"],
            "location": grievance["location"],
            "priority": grievance["priority"],
            "responsible_department": grievance["responsible_department"],
            "status": grievance["status"],
            "created_at": grievance["created_at"],
        }
    )


# ---------------------------------------------------------
# AI GRIEVANCE ANALYSIS
# ---------------------------------------------------------


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    grievance = data.get("grievance", "").strip()

    # Check empty grievance
    if not grievance:
        return jsonify({"error": "Please enter a grievance."}), 400

    # Prompt for IBM Granite
    prompt = f"""
You are the AI engine of a campus grievance analysis system.

Analyze ONLY the grievance between the <GRIEVANCE> tags.

<GRIEVANCE>
{grievance}
</GRIEVANCE>

Return ONLY valid JSON.

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

Priority criteria:

- High: Use when the grievance involves a safety or health risk,
  major service disruption, urgent infrastructure failure,
  or significant environmental/resource wastage.

- Medium: Use when the grievance causes moderate disruption,
  ongoing inconvenience, or noticeable resource inefficiency
  but does not create an immediate serious risk.

- Low: Use when the grievance is a minor inconvenience,
  cosmetic issue, or non-urgent request.

Rules:

- Select exactly one allowed category.
- Select exactly one allowed priority.
- Do not invent facts.
- If information is missing, use "Not specified".
- Extract the location when it is present in the grievance.
- The responsible department may be inferred from the category.
- Sustainability impact should describe environmental or resource impact.
- Recommended action should be practical and concise.
- Summary should be one short sentence.
"""

    # Messages sent to Granite
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": grievance},
    ]

    # Model parameters
    params = {
        "temperature": 0,
        "max_tokens": 300,
        "response_format": {"type": "json_object"},
    }

    try:

        # Send grievance to IBM Granite
        response = model.chat(messages=messages, params=params)

        # Extract AI response
        content = response["choices"][0]["message"]["content"]

        # Convert JSON string to Python dictionary
        result = json.loads(content)

        # -------------------------------------------------
        # RECURRING ISSUE DETECTION
        # -------------------------------------------------

        connection = get_connection()

        # Get previous grievances
        previous_grievances = connection.execute("""
            SELECT
                id,
                category,
                issue,
                location
            FROM grievances
            ORDER BY id DESC
        """).fetchall()

        # Compare current grievance with previous grievances
        recurring, matched_grievance, similarity_score = check_recurring_issue(
            result, previous_grievances
        )

        # Add recurring information
        result["recurring_issue"] = recurring

        result["similarity_score"] = round(similarity_score * 100, 2)

        # Store matched grievance ID
        if matched_grievance:

            result["matched_grievance_id"] = matched_grievance["id"]

        else:

            result["matched_grievance_id"] = None

        # -------------------------------------------------
        # SAVE TO DATABASE
        # -------------------------------------------------

        cursor = connection.execute(
            """
            INSERT INTO grievances (
                grievance,
                category,
                issue,
                location,
                duration,
                priority,
                responsible_department,
                sustainability_impact,
                recommended_action,
                summary,
                recurring_issue,
                matched_grievance_id,
                similarity_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                grievance,
                result.get("category"),
                result.get("issue"),
                result.get("location"),
                result.get("duration"),
                result.get("priority"),
                result.get("responsible_department"),
                result.get("sustainability_impact"),
                result.get("recommended_action"),
                result.get("summary"),
                int(recurring),
                result.get("matched_grievance_id"),
                result.get("similarity_score"),
            ),
        )
        grievance_id = cursor.lastrowid
        # Save changes
        connection.commit()
        connection.close()

        result["grievance_id"] = f"SGA-{grievance_id:03d}"

        return jsonify(result)

    except json.JSONDecodeError:

        return jsonify({"error": "AI returned an invalid JSON response."}), 500

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------
# UPDATE GRIEVANCE STATUS
# ---------------------------------------------------------


@app.route("/update_status/<int:grievance_id>", methods=["POST"])
def update_status(grievance_id):

    data = request.get_json()

    status = data.get("status")

    allowed_statuses = ["Pending", "In Progress", "Resolved"]

    if status not in allowed_statuses:
        return jsonify({"error": "Invalid status."}), 400

    connection = get_connection()

    connection.execute(
        """
        UPDATE grievances
        SET status = ?
        WHERE id = ?
    """,
        (status, grievance_id),
    )

    connection.commit()
    connection.close()

    return jsonify({"message": "Status updated successfully.", "status": status})


# ---------------------------------------------------------
# START FLASK APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)
