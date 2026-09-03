def generate_career_coaching(
    answer_score,
    vision_score,
    eye_contact,
    posture,
    resume_match,
    role,
    missing_skills=None
):

    if missing_skills is None:
        missing_skills = []

    priorities = []
    recommendations = []
    learning_plan = []

    # =================================
    # ANSWER PERFORMANCE
    # =================================

    if answer_score < 60:

        priorities.append("Answer Quality")

        recommendations.append(
            "Focus on improving technical knowledge and answer structure."
        )

        learning_plan.append(
            "Practice technical interview questions."
        )

    elif answer_score < 80:

        recommendations.append(
            "Practice giving structured and detailed answers."
        )

        learning_plan.append(
            "Practice explaining concepts using examples."
        )

    else:

        recommendations.append(
            "Your answer performance is strong. Continue practicing advanced questions."
        )

    # =================================
    # EYE CONTACT
    # =================================

    if eye_contact < 60:

        priorities.append("Eye Contact")

        recommendations.append(
            "Practice looking toward the camera while answering."
        )

        learning_plan.append(
            "Practice mock interviews while maintaining camera focus."
        )

    # =================================
    # POSTURE
    # =================================

    if posture < 60:

        priorities.append("Posture")

        recommendations.append(
            "Maintain a stable and professional posture during interviews."
        )

        learning_plan.append(
            "Practice sitting posture during mock interviews."
        )

    # =================================
    # VISION
    # =================================

    if vision_score < 60:

        priorities.append("Interview Presence")

        recommendations.append(
            "Improve your overall professional presence during interviews."
        )

    # =================================
    # RESUME MATCH
    # =================================

    if resume_match < 60:

        priorities.append("Skill Gap")

        recommendations.append(
            f"Improve skills required for the {role} role."
        )

    elif resume_match >= 80:

        recommendations.append(
            "Your resume has a strong match with the selected role."
        )

    # =================================
    # MISSING SKILLS
    # =================================

    for skill in missing_skills:

        learning_plan.append(
            f"Learn and practice {skill}."
        )

    # =================================
    # ROLE BASED PREPARATION
    # =================================

    learning_plan.append(
        f"Practice {role} interview questions."
    )

    learning_plan.append(
        "Prepare clear explanations of your projects."
    )

    learning_plan.append(
        "Practice common HR interview questions."
    )

    return {
        "priorities": priorities,
        "recommendations": recommendations,
        "learning_plan": learning_plan
    }