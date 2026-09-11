from difflib import SequenceMatcher


def similarity(text1, text2):
    """
    Calculate similarity between two pieces of text.

    The comparison considers both:
    1. Normal text similarity
    2. Word-based similarity

    This helps recognize phrases such as:
    "Overflowing garbage bins"
    and
    "Garbage bins overflowing"
    as similar.
    """

    text1 = str(text1 or "").lower().strip()
    text2 = str(text2 or "").lower().strip()

    if not text1 or not text2:
        return 0

    # Normal text similarity
    sequence_score = SequenceMatcher(None, text1, text2).ratio()

    # Word-based similarity
    words1 = set(text1.split())
    words2 = set(text2.split())

    if words1 and words2:

        common_words = words1.intersection(words2)

        word_score = 2 * len(common_words) / (len(words1) + len(words2))

    else:
        word_score = 0

    # Use the stronger of the two scores
    return max(sequence_score, word_score)


def check_recurring_issue(current_result, previous_grievances):
    """
    Compare the current grievance with previous grievances.

    A grievance is considered potentially recurring only when:
    - The category matches
    - The issue description is sufficiently similar
    - The location is the same or very similar
    """

    best_match = None
    best_score = 0

    current_category = str(current_result.get("category", "")).lower().strip()

    current_issue = str(current_result.get("issue", "")).lower().strip()

    current_location = str(current_result.get("location", "")).lower().strip()

    for grievance in previous_grievances:

        previous_category = str(grievance["category"] or "").lower().strip()

        previous_issue = str(grievance["issue"] or "").lower().strip()

        previous_location = str(grievance["location"] or "").lower().strip()

        # Category must match
        if current_category != previous_category:
            continue

        # Calculate issue similarity
        issue_score = similarity(current_issue, previous_issue)

        # Calculate location similarity
        location_score = similarity(current_location, previous_location)

        # Require sufficiently similar issue
        # This prevents unrelated complaints in the same category
        # from being marked as recurring.
        if issue_score < 0.65:
            continue

        # Calculate final score
        score = issue_score * 0.60 + location_score * 0.40

        if score > best_score:

            best_score = score
            best_match = grievance

    # Final recurring threshold
    recurring = best_score >= 0.70

    return recurring, best_match, best_score
