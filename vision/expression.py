import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


MODEL_PATH = "models/face_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1,
    output_face_blendshapes=True
)

landmarker = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open nahi ho raha")
    exit()

timestamp = 0


def get_blendshape(blendshapes, name):

    for item in blendshapes:

        if item.category_name == name:
            return item.score

    return 0.0


while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame nahi mil raha")
        break

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp += 1

    result = landmarker.detect_for_video(
        mp_image,
        timestamp
    )

    expression = "Neutral"

    if result.face_blendshapes:

        blendshapes = result.face_blendshapes[0]

        smile_left = get_blendshape(
            blendshapes,
            "mouthSmileLeft"
        )

        smile_right = get_blendshape(
            blendshapes,
            "mouthSmileRight"
        )

        blink_left = get_blendshape(
            blendshapes,
            "eyeBlinkLeft"
        )

        blink_right = get_blendshape(
            blendshapes,
            "eyeBlinkRight"
        )

        brow_up = get_blendshape(
            blendshapes,
            "browInnerUp"
        )

        smile = (smile_left + smile_right) / 2
        blink = (blink_left + blink_right) / 2

        if smile > 0.45:
            expression = "Smile Cue"

        elif blink > 0.60:
            expression = "Blink"

        elif brow_up > 0.45:
            expression = "Brow Raised"

        else:
            expression = "Neutral Cue"

        cv2.putText(
            frame,
            f"Expression: {expression}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Smile: {smile:.2f}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "No Face",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "AI Interview - Facial Cues",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
landmarker.close()
cv2.destroyAllWindows()