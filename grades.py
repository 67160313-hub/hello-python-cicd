def grade(score):
    """Convert a score from 0 to 100 into a letter grade."""
    if not 0 <= score <= 100:
        raise ValueError("Score must be between 0 and 100")
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def average(scores):
    """Return the average score rounded to two decimal places."""
    if not scores:
        raise ValueError("At least one score is required")
    return round(sum(scores) / len(scores), 2)
