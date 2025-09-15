def extract_skills(text):
    """
    Simulates extracting skills from resume text.
    In a real project, this would use a more advanced NLP library like spaCy.
    """
    # A list of predefined keywords to search for
    keywords = [
        "python", "django", "javascript", "react", "html", "css",
        "sql", "nosql", "aws", "gcp", "azure",
        "machine learning", "artificial intelligence", "data science",
        "project management", "agile", "scrum",
        "ui/ux design", "figma", "photoshop"
    ]
    
    # Extract skills by checking for keyword presence in the text
    found_skills = [
        keyword for keyword in keywords if keyword in text.lower()
    ]
    
    return found_skills