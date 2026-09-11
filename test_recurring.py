from recurring import check_recurring_issue

# Simulated previous grievance
previous_grievances = [
    {
        "category": "Waste Management",
        "issue": "Overflowing garbage bins",
        "location": "Near the college canteen",
    }
]


# New grievance analyzed by Granite
current_result = {
    "category": "Waste Management",
    "issue": "Garbage bins overflowing",
    "location": "Near the college canteen",
}


recurring, matched_grievance, score = check_recurring_issue(
    current_result, previous_grievances
)


print("\n--- RECURRING ISSUE TEST ---")

print("Recurring:", recurring)
print("Similarity Score:", round(score * 100, 2), "%")

if matched_grievance:
    print("Matched Previous Issue:", matched_grievance["issue"])
    print("Matched Location:", matched_grievance["location"])
else:
    print("No similar grievance found.")
