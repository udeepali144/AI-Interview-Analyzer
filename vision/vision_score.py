def calculate_vision_score(
    eye_contact,
    head_stability,
    posture,
    face_presence
):

    score = (
        eye_contact * 0.35 +
        head_stability * 0.20 +
        posture * 0.30 +
        face_presence * 0.15
    )

    return round(score, 2)


def generate_feedback(
    eye_contact,
    head_stability,
    posture,
    face_presence
):

    feedback = []

    if eye_contact < 60:

        feedback.append(
            "Try to maintain more consistent camera-facing gaze."
        )

    if head_stability < 60:

        feedback.append(
            "Try to keep head movement more stable."
        )

    if posture < 60:

        feedback.append(
            "Maintain a more upright sitting posture."
        )

    if face_presence < 80:

        feedback.append(
            "Keep your face clearly visible to the camera."
        )

    if len(feedback) == 0:

        feedback.append(
            "Observed interview behaviour was consistent."
        )

    return feedback