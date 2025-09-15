# A simple, static database of career paths and their required skills
CAREER_DATABASE = {
    "Data Scientist": ["python", "sql", "data science", "machine learning"],
    "Full-Stack Developer": ["python", "django", "javascript", "html", "css"],
    "Cloud Engineer": ["aws", "gcp", "azure", "python"],
    "UI/UX Designer": ["ui/ux design", "figma", "photoshop", "html", "css"],
    "Project Manager": ["project management", "agile", "scrum"],
}

def match_careers(skills):
    """
    Matches a user's skills to career paths and returns a ranked list.
    The score is based on the number of matching skills.
    """
    matches = {}
    
    # Count how many required skills match the user's skills
    for career, required_skills in CAREER_DATABASE.items():
        score = 0
        for skill in skills:
            if skill.lower() in required_skills:
                score += 1
        
        # Only suggest careers with at least one skill match
        if score > 0:
            matches[career] = score
            
    # Sort careers by match score in descending order
    sorted_matches = sorted(
        matches.items(), key=lambda item: item[1], reverse=True
    )
    
    return sorted_matches