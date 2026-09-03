def match_skills(resume_skills, required_skills):

    resume_set = {
        skill.lower()
        for skill in resume_skills
    }

    required_set = {
        skill.lower()
        for skill in required_skills
    }

    matched = resume_set.intersection(required_set)

    missing = required_set - resume_set

    if required_set:

        percentage = (
            len(matched) / len(required_set)
        ) * 100

    else:

        percentage = 0

    return {
        "matched": list(matched),
        "missing": list(missing),
        "match_percentage": round(
            percentage,
            2
        )
    }