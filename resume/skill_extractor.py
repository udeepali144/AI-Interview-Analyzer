SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Pandas",
    "NumPy",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Power BI",
    "Excel",
    "OpenCV",
    "NLP",
    "Generative AI",
    "Git",
    "Docker",
    "AWS"
]


def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills