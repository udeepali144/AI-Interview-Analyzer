import re
import time

from .speech_to_text import record_and_transcribe


FILLER_WORDS = [
    "um",
    "uh",
    "umm",
    "hmm",
    "like",
    "you know",
    "basically",
    "actually"
]


def analyze_speech(text, duration):
    """
    Analyze candidate's speech.
    """

    words = re.findall(r"\b[\w']+\b", text.lower())

    word_count = len(words)

    # Words per minute
    if duration > 0:
        wpm = (word_count / duration) * 60
    else:
        wpm = 0

    # Filler words
    filler_count = 0

    for filler in FILLER_WORDS:

        filler_count += text.lower().count(filler)

    # Basic speech score
    score = 100

    # Too many fillers
    if filler_count >= 5:
        score -= 20

    elif filler_count >= 3:
        score -= 10

    # Speaking speed
    if wpm < 80:
        score -= 10

    elif wpm > 180:
        score -= 10

    score = max(0, min(100, score))

    return {
        "word_count": word_count,
        "wpm": round(wpm, 1),
        "filler_words": filler_count,
        "speech_score": score
    }


def get_voice_answer(duration=8):

    start_time = time.time()

    answer = record_and_transcribe(duration)

    end_time = time.time()

    actual_duration = end_time - start_time

    analysis = analyze_speech(
        answer,
        actual_duration
    )

    return {
        "text": answer,
        "duration": round(actual_duration, 1),
        "word_count": analysis["word_count"],
        "wpm": analysis["wpm"],
        "filler_words": analysis["filler_words"],
        "speech_score": analysis["speech_score"]
    }