import soundfile as sf
import speech_recognition as sr
import os


def record_audio(filename="answer.wav", duration=8, samplerate=16000):
    print("🎤 Recording started...")

    recording = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    sf.write(filename, recording, samplerate)

    print("✅ Recording saved")
    return filename


def speech_to_text(filename="answer.wav"):
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:
        return "Could not understand the audio."

    except sr.RequestError:
        return "Speech recognition service is unavailable."

    except Exception as e:
        return f"Speech error: {e}"


def record_and_transcribe(duration=8):
    filename = record_audio(
        filename="answer.wav",
        duration=duration
    )

    text = speech_to_text(filename)

    return text
