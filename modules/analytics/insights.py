def generate_insights(performance):

    strengths = []
    weaknesses = []
    insights = []

    answer_quality = performance.get("answer_quality", 0)
    vision_score = performance.get("vision_score", 0)
    eye_contact = performance.get("eye_contact", 0)
    posture = performance.get("posture", 0)

    # -----------------------------
    # ANSWER QUALITY
    # -----------------------------

    if answer_quality >= 80:

        strengths.append("Strong answer quality")

    elif answer_quality < 60:

        weaknesses.append("Improve answer quality")

    # -----------------------------
    # VISION
    # -----------------------------

    if vision_score >= 80:

        strengths.append("Good visual performance")

    elif vision_score < 60:

        weaknesses.append("Improve visual presence")

    # -----------------------------
    # EYE CONTACT
    # -----------------------------

    if eye_contact >= 80:

        strengths.append("Good eye contact")

    elif eye_contact < 60:

        weaknesses.append("Improve eye contact")

    # -----------------------------
    # POSTURE
    # -----------------------------

    if posture >= 80:

        strengths.append("Good posture")

    elif posture < 60:

        weaknesses.append("Improve posture")

    # -----------------------------
    # OVERALL INSIGHTS
    # -----------------------------

    if answer_quality >= 80:
        insights.append(
            "Your answers show strong understanding of the interview questions."
        )

    elif answer_quality < 60:
        insights.append(
            "Try to provide more detailed and structured answers."
        )

    if eye_contact >= 80:
        insights.append(
            "Your eye contact is good and shows strong engagement."
        )

    elif eye_contact < 60:
        insights.append(
            "Try to maintain better eye contact with the camera."
        )

    if posture >= 80:
        insights.append(
            "Your posture is professional and stable."
        )

    elif posture < 60:
        insights.append(
            "Try to maintain a more stable and professional posture."
        )

    if vision_score >= 80:
        insights.append(
            "Your overall visual interview presence is strong."
        )

    elif vision_score < 60:
        insights.append(
            "Your visual interview presence needs improvement."
        )

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "insights": insights
    }