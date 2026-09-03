import json
import os


def get_questions(role):
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "questions.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get(role, [])

def get_resume_questions(role, skills):

    questions = []

    skill_questions = {

        "Python": [
            "You mentioned Python in your resume. Explain the difference between a list and a tuple.",
            "You mentioned Python. What are decorators?"
        ],

        "SQL": [
            "You mentioned SQL in your resume. Explain the difference between WHERE and HAVING.",
            "How would you find duplicate records in SQL?"
        ],

        "Pandas": [
            "You mentioned Pandas. How do you handle missing values in a DataFrame?",
            "What is the difference between loc and iloc in Pandas?"
        ],

        "Machine Learning": [
            "You mentioned Machine Learning. What is overfitting?",
            "Explain the difference between classification and regression."
        ],

        "Power BI": [
            "You mentioned Power BI. What is the difference between a measure and a calculated column?"
        ],

        "OpenCV": [
            "You mentioned OpenCV. How is OpenCV used in computer vision?"
        ]
    }

    for skill in skills:

        if skill in skill_questions:

            questions.extend(
                skill_questions[skill]
            )

    if not questions:

        questions = get_questions(role)

    return questions

# =====================================================
# ADAPTIVE QUESTION SELECTION
# =====================================================

def get_adaptive_question(
    current_score,
    current_index,
    role,
    skills=None
):

    # -----------------------------------------
    # Get available questions
    # -----------------------------------------

    if skills:

        questions = get_resume_questions(
            role,
            skills
        )

    else:

        questions = get_questions(
            role
        )

    # -----------------------------------------
    # Safety check
    # -----------------------------------------

    if not questions:

        return None

    # -----------------------------------------
    # EASY LEVEL
    # -----------------------------------------

    if current_score < 60:

        index = current_index % len(questions)

        return questions[index]

    # -----------------------------------------
    # MEDIUM LEVEL
    # -----------------------------------------

    elif current_score < 80:

        index = (
            current_index + 1
        ) % len(questions)

        return questions[index]

    # -----------------------------------------
    # HARD LEVEL
    # -----------------------------------------

    else:

        index = (
            current_index + 2
        ) % len(questions)

        return questions[index]