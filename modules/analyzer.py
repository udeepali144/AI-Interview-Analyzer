from nlp.similarity import calculate_similarity


def analyze_answer(question, answer):

    # -----------------------------
    # CHECK ANSWER
    # -----------------------------

    if not answer or not answer.strip():

        return {
            "score": 0,
            "feedback": "No answer was provided.",
            "similarity": 0.0,
            "word_count": 0
        }

    # -----------------------------
    # CLEAN ANSWER
    # -----------------------------

    answer = answer.strip()

    # -----------------------------
    # BASIC ANALYSIS
    # -----------------------------

    words = answer.split()
    word_count = len(words)

    # -----------------------------
    # SIMILARITY
    # -----------------------------

    similarity = calculate_similarity(
        question,
        answer
    )

    # Convert similarity into score
    relevance_score = similarity * 100

    # -----------------------------
    # LENGTH SCORE
    # -----------------------------

    if word_count < 5:
        length_score = 20

    elif word_count < 15:
        length_score = 50

    elif word_count < 30:
        length_score = 75

    else:
        length_score = 90

    # -----------------------------
    # FINAL SCORE
    # -----------------------------

    final_score = (
        (relevance_score * 0.60)
        +
        (length_score * 0.40)
    )

    final_score = round(
        min(final_score, 100)
    )

    # -----------------------------
    # FEEDBACK
    # -----------------------------

    if final_score < 40:

        feedback = (
            "Your answer needs improvement. "
            "Try to directly address the question "
            "and explain the concept with an example."
        )

    elif final_score < 60:

        feedback = (
            "Good attempt, but your answer could be "
            "more relevant and detailed."
        )

    elif final_score < 80:

        feedback = (
            "Good answer. The response is reasonably "
            "relevant. Add a practical example for improvement."
        )

    else:

        feedback = (
            "Excellent answer. Your response is relevant "
            "and provides good detail."
        )

    # -----------------------------
    # RETURN RESULT
    # -----------------------------

    return {
        "score": final_score,
        "feedback": feedback,
        "similarity": similarity,
        "word_count": word_count
    }