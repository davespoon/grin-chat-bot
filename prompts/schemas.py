resume_schema = {
    "name": "Extract structured information from resumes",
    "description": "Extract details like name, email, phone, summary, education, work experience, skills, another useful information.",
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "Full name of the candidate"},
        "email": {"type": "string", "description": "Email address"},
        "phone": {"type": "string", "description": "Phone number"},
        "summary": {"type": "string", "description": "Summary of the candidate"},
        "education": {"type": "array", "description": "List of education details", "items": {"type": "string"}},
        "experience": {"type": "array", "description": "List of work experience", "items": {"type": "string"}},
        "skills": {"type": "array", "description": "List of key skills", "items": {"type": "string"}},
        "another_useful_information": {"type": "string", "description": "Another info about the candidate"}
    }
}
