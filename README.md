\# Smart Grievance Analyzer (SGA)



\## AI-Powered Grievance Analysis for Sustainable Campus Management



Smart Grievance Analyzer (SGA) is an AI-powered decision-support system designed to help educational institutions analyze, prioritize, route, and manage campus grievances while identifying recurring issues and sustainability impacts.



The system uses \*\*IBM Granite through IBM watsonx.ai\*\* to transform unstructured student and staff grievances into structured, actionable information for campus administrators.



\---



\## Problem Statement



Campus grievances such as water leakage, waste accumulation, electricity wastage, infrastructure problems, transportation issues, and technical problems are often submitted as unstructured text.



This can make it difficult for administrators to:



\- Identify the type of issue quickly

\- Determine its urgency

\- Route it to the appropriate department

\- Detect recurring problems

\- Understand sustainability impacts

\- Take timely corrective action

\- Track the status of submitted grievances



\### How Might We?



> How might we use AI to analyze, prioritize, and identify patterns in campus grievances so that campus services and communities can become more sustainable?



\---



\## Proposed Solution



SGA provides \*\*two separate interfaces\*\* connected through a Flask backend and a shared SQLite database.



\### 1. Grievance Analyzer



The Grievance Analyzer is designed for \*\*students and staff\*\*.



Users submit a grievance in natural language. IBM Granite analyzes the grievance and provides:



\- Grievance ID

\- Category

\- Issue

\- Location

\- Duration

\- Priority

\- Responsible Department

\- Sustainability Impact

\- Recommended Action

\- AI Summary

\- Potentially Recurring Issue detection



Users can also enter their Grievance ID to check the current status of their grievance.



\### 2. Admin Dashboard



The Admin Dashboard is designed for \*\*college administrators and campus management\*\*.



Administrators can:



\- View total grievances

\- View high, medium, and low priority grievances

\- Identify potentially recurring issues

\- View grievance category distribution

\- View sustainability insights

\- Review recent grievances

\- Update grievance status



Available statuses:



\- Pending

\- In Progress

\- Resolved



\---



\## System Workflow



```text

Student / Staff

&#x20;      |

&#x20;      v

Grievance Analyzer

&#x20;      |

&#x20;      v

Flask Backend

&#x20;      |

&#x20;      v

IBM Granite

&#x20;      |

&#x20;      v

AI Analysis

&#x20;      |

&#x20;      +----------------------+

&#x20;      |                      |

&#x20;      v                      v

Structured Analysis     Recurring Detection

&#x20;      |                      |

&#x20;      +----------+-----------+

&#x20;                 |

&#x20;                 v

&#x20;            SQLite Database

&#x20;                 |

&#x20;                 v

&#x20;          Admin Dashboard

&#x20;                 |

&#x20;                 v

&#x20;         Admin Reviews Issue

&#x20;                 |

&#x20;                 v

&#x20;      Pending / In Progress /

&#x20;            Resolved

&#x20;                 |

&#x20;                 v

&#x20;      Student Checks Status

&#x20;      Using Grievance ID

```



\## Key AI Features



\### 1. Grievance Classification



The AI categorizes grievances into predefined categories:



\- Water \& Sanitation

\- Waste Management

\- Electricity \& Energy

\- Infrastructure

\- Maintenance

\- Transportation

\- Environment

\- IT/Technical

\- Cleanliness

\- Other



\### 2. Priority Detection



The system classifies grievances as:



\- High

\- Medium

\- Low



Priority is determined using factors such as:



\- Safety risk

\- Health risk

\- Service disruption

\- Urgency

\- Environmental impact

\- Resource wastage



\### 3. Information Extraction



The AI extracts useful information from the grievance, including:



\- Issue

\- Location

\- Duration



\### 4. Department Routing



The system identifies the department that should handle the grievance.



\### 5. Recurring Issue Detection



SGA compares new grievances with previous grievances to identify potentially recurring problems.



The system provides:



\- Similarity score

\- Matched grievance ID



Recurring detection is presented as a potential match rather than absolute certainty.



\### 6. Sustainability Analysis



The AI identifies environmental or resource-related impacts of grievances.



Examples include:



\- Water wastage

\- Energy wastage

\- Waste accumulation

\- Environmental pollution

\- Resource inefficiency



\### 7. Recommended Actions



The system generates practical actions that administrators can consider.



\### 8. AI Summary



Each grievance is converted into a concise summary for easier administrative review.



\## Sustainability Alignment



\### Primary SDG



SDG 11 – Sustainable Cities and Communities



SGA supports sustainable community management by helping institutions identify and address recurring infrastructure, waste, water, energy, and environmental problems.



\### Secondary SDGs



\- SDG 6 – Clean Water and Sanitation

\- SDG 7 – Affordable and Clean Energy

\- SDG 12 – Responsible Consumption and Production



\## Example



\### User Grievance



There is a water leakage near the girls hostel for the last 3 days, and a large amount of water is being wasted.



\### AI Analysis



\*\*Category:\*\*

Water \& Sanitation



\*\*Priority:\*\*

High



\*\*Location:\*\*

Girls Hostel



\*\*Duration:\*\*

3 days



\*\*Responsible Department:\*\*

Facilities Management



\*\*Sustainability Impact:\*\*

Water wastage due to the ongoing leakage.



\*\*Recommended Action:\*\*

Inspect and repair the leakage immediately.



If a similar grievance already exists, SGA can identify it as:



\*\*Potentially Recurring Issue\*\*



and provide a similarity score.



\## Grievance Tracking



Every submitted grievance receives a unique ID.



Examples:



\- SGA-001

\- SGA-002

\- SGA-003



Students and staff can use the Grievance ID to check the current status of their grievance.



Example:



\*\*Grievance ID:\*\*

SGA-006



\*\*Status:\*\*

Resolved



The status is updated by the administrator through the Admin Dashboard.



\## Responsible AI



SGA follows responsible AI principles during analysis and decision support.



\*\*Fairness\*\*

Predefined categories and priority levels are used to promote consistent classification.



\*\*Transparency\*\*

AI-generated analysis and recommendations are displayed clearly to users and administrators.



\*\*Privacy\*\*

Users are encouraged not to include unnecessary personal or sensitive information in grievances.



\*\*Human Review\*\*

AI recommendations support administrators but do not replace human decision-making.



\*\*Uncertainty\*\*

Recurring issue detection is presented as a potential match instead of claiming certainty.



\*\*Controlled Output\*\*

The AI is instructed to use predefined categories and priorities and avoid inventing missing information.



\## Technology Stack



| Component | Technology |

|---|---|

| Frontend | HTML, CSS, JavaScript |

| Backend | Python, Flask |

| Database | SQLite |

| AI Model | IBM Granite 4 H Small |

| AI Platform | IBM watsonx.ai |

| Development | Visual Studio Code |

| Version Control | Git |

| Repository | GitHub |



\## Project Architecture

&#x20;      

&#x20;                SGA SYSTEM

&#x20;                   |

&#x20;       +-----------+-----------+

&#x20;       |                       |

&#x20;       v                       v

Grievance Analyzer        Admin Dashboard

&#x20;Students / Staff         College Admin

&#x20;       |                       |

&#x20;       +-----------+-----------+

&#x20;                   |

&#x20;                   v

&#x20;             Flask Backend

&#x20;                   |

&#x20;         +---------+---------+

&#x20;         |                   |

&#x20;         v                   v

&#x20;     IBM Granite          SQLite

&#x20;         |

&#x20;         v

&#x20;      AI Analysis



\## Project Structure



smart-grievance-analyzer/

│

├── static/

│

├── templates/

│ ├── index.html

│ └── dashboard.html

│

├── app.py

├── database.py

├── recurring.py

│

├── check\_database.py

├── check\_models.py

├── test\_config.py

├── test\_granite.py

├── test\_granite\_json.py

├── test\_recurring.py

│

├── requirements.txt

├── README.md

└── .gitignore



\## How the Prototype Works



\### Step 1 — Submit a Grievance



A student or staff member enters a campus grievance through the Grievance Analyzer.



\### Step 2 — AI Analysis



The Flask backend sends the grievance to IBM Granite through IBM watsonx.ai.



\### Step 3 — Structured Output



The AI identifies the category, priority, issue, location, duration, department, sustainability impact, and recommended action.



\### Step 4 — Recurring Detection



The system compares the new grievance with previous grievances to identify potential recurring issues.



\### Step 5 — Database Storage



The analyzed grievance is stored in the SQLite database along with its unique Grievance ID.



\### Step 6 — Admin Review



Administrators can review grievances through the separate Admin Dashboard.



\### Step 7 — Status Tracking



Administrators can update the grievance status:



Pending → In Progress → Resolved



Students can check the latest status using their Grievance ID.



\## Impact



SGA aims to help educational institutions move from reactive complaint handling toward data-driven and sustainability-focused campus management.



Potential benefits include:



\- Faster grievance classification

\- Better prioritization

\- More efficient department routing

\- Identification of recurring issues

\- Improved resource management

\- Reduced water and energy wastage

\- Better waste management

\- Improved transparency of grievance status

\- Data-supported administrative decisions



\## Future Scope



Future versions of SGA could include:



\- Email and notification alerts

\- Mobile application

\- Authentication and role-based access

\- Advanced analytics and trend prediction

\- Geographical visualization of recurring issues

\- Integration with institutional ticketing systems

\- Multilingual grievance submission

\- More advanced sustainability metrics

\- Automated escalation of unresolved high-priority issues



\## Running the Project Locally



\### 1. Clone the Repository

git clone https://github.com/Manoj29981/smart-grievance-analyzer.git



\### 2. Open the Project Directory

cd smart-grievance-analyzer



\### 3. Create a Virtual Environment



Windows:



```bash

python -m venv venv

```



\### 4. Activate the Virtual Environment



```bash

venv\\Scripts\\activate

```

\### 5. Install Dependencies

pip install -r requirements.txt



\### 6. Configure Environment Variables



Create a .env file in the project root:

WATSONX\_APIKEY=your\_ibm\_watsonx\_api\_key

WATSONX\_PROJECT\_ID=your\_watsonx\_project\_id

WATSONX\_URL=your\_watsonx\_url



Do not commit the .env file to GitHub.



\### 7. Initialize the Database

python database.py



\### 8. Start the Application

python app.py



Open the Grievance Analyzer:



http://127.0.0.1:5000



Open the Admin Dashboard:



http://127.0.0.1:5000/dashboard



\## Demo



The current prototype demonstrates:



\- AI-powered grievance analysis

\- Category classification

\- Priority detection

\- Information extraction

\- Department routing

\- Recurring grievance detection

\- Sustainability impact analysis

\- Recommended actions

\- Unique Grievance IDs

\- Separate Admin Dashboard

\- Grievance status management

\- Student/staff status checking



\## Project Information



\*\*Project:\*\* Smart Grievance Analyzer (SGA)



\*\*Long Title:\*\* AI Smart Grievance Analyzer for Sustainable Campus Management



\*\*Program:\*\* 1M1B AI for Sustainability Virtual Internship



\*\*Collaboration:\*\* 1M1B × IBM SkillsBuild × AICTE



\*\*Primary SDG:\*\* SDG 11 – Sustainable Cities and Communities



\*\*Institution:\*\* Guru Nanak Institute of Technology



\*\*Developer:\*\* Manoj Kumar Pochamolla



\## Repository



GitHub:



https://github.com/Manoj29981/smart-grievance-analyzer

