import cv2
import mediapipe as mp
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


MODEL_PATH = "models/face_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1
)

landmarker = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

timestamp = 0


def distance(p1, p2):
    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera open nahi ho raha")
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

    status = "No Face"

    if result.face_landmarks:

        landmarks = result.face_landmarks[0]

        # Eye landmarks
        left_eye_top = landmarks[159]
        left_eye_bottom = landmarks[145]

        right_eye_top = landmarks[386]
        right_eye_bottom = landmarks[374]

        left_eye_open = distance(
            left_eye_top,
            left_eye_bottom
        )

        right_eye_open = distance(
            right_eye_top,
            right_eye_bottom
        )

        average_eye_open = (
            left_eye_open +
            right_eye_open
        ) / 2

        if average_eye_open < 0.015:
            status = "Eyes Closed"

        else:

            # Iris landmarks
            left_iris = landmarks[468]
            right_iris = landmarks[473]

            left_eye_left = landmarks[33]
            left_eye_right = landmarks[133]

            right_eye_left = landmarks[362]
            right_eye_right = landmarks[263]

            left_ratio = (
                left_iris.x - left_eye_left.x
            ) / (
                left_eye_right.x - left_eye_left.x
            )

            right_ratio = (
                right_iris.x - right_eye_left.x
            ) / (
                right_eye_right.x - right_eye_left.x
            )

            gaze_ratio = (
                left_ratio + right_ratio
            ) / 2

            if 0.40 <= gaze_ratio <= 0.60:
                status = "Looking at Camera"

            elif gaze_ratio < 0.40:
                status = "Looking Left"

            else:
                status = "Looking Right"

    cv2.putText(
        frame,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "AI Interview - Eye Contact",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
landmarker.close()
cv2.destroyAllWindows()