def calculate_score(answer_analysis):

    word_count = answer_analysis["word_count"]
    total_fillers = answer_analysis["total_fillers"]

    # Length score
    if word_count < 10:
        length_score = 30
    elif word_count < 30:
        length_score = 60
    elif word_count < 60:
        length_score = 80
    else:
        length_score = 90

    # Filler score
    if total_fillers == 0:
        filler_score = 100
    elif total_fillers <= 2:
        filler_score = 90
    elif total_fillers <= 5:
        filler_score = 75
    elif total_fillers <= 8:
        filler_score = 60
    else:
        filler_score = 40

    final_score = (length_score * 0.6) + (filler_score * 0.4)

    return round(final_score, 2)