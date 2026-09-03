import cv2
import mediapipe as mp
import numpy as np

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


while True:

    ret, frame = cap.read()

    if not ret:
        print("Camera open nahi ho raha")
        break

    h, w, _ = frame.shape

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

        # Important face points
        nose = landmarks[1]
        left_face = landmarks[234]
        right_face = landmarks[454]
        forehead = landmarks[10]
        chin = landmarks[152]

        # Convert normalized coordinates to pixels
        nose_x = nose.x * w
        nose_y = nose.y * h

        left_x = left_face.x * w
        right_x = right_face.x * w

        forehead_y = forehead.y * h
        chin_y = chin.y * h

        # Horizontal head position
        face_center_x = (left_x + right_x) / 2

        horizontal_ratio = (
            nose_x - left_x
        ) / (
            right_x - left_x
        )

        # Vertical head position
        face_height = chin_y - forehead_y

        vertical_ratio = (
            nose_y - forehead_y
        ) / face_height

        # Head left / right
        if horizontal_ratio < 0.40:
            horizontal_status = "Head Left"

        elif horizontal_ratio > 0.60:
            horizontal_status = "Head Right"

        else:
            horizontal_status = "Head Center"

        # Head up / down
        if vertical_ratio < 0.40:
            vertical_status = "Head Up"

        elif vertical_ratio > 0.60:
            vertical_status = "Head Down"

        else:
            vertical_status = "Head Normal"

        status = horizontal_status

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            vertical_status,
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Draw important points
        for point in [
            nose,
            left_face,
            right_face,
            forehead,
            chin
        ]:

            x = int(point.x * w)
            y = int(point.y * h)

            cv2.circle(
                frame,
                (x, y),
                4,
                (0, 255, 0),
                -1
            )

    else:

        cv2.putText(
            frame,
            "No Face Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "AI Interview - Head Pose",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
landmarker.close()
cv2.destroyAllWindows()