import cv2
import mediapipe as mp
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# =========================
# MODEL
# =========================

MODEL_PATH = "models/pose_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_poses=1,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

landmarker = vision.PoseLandmarker.create_from_options(options)


# =========================
# WEBCAM
# =========================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open nahi ho raha")
    exit()


timestamp = 0


# =========================
# HELPER FUNCTION
# =========================

def calculate_angle(x1, y1, x2, y2):

    angle = math.degrees(
        math.atan2(
            y2 - y1,
            x2 - x1
        )
    )

    return angle


# =========================
# MAIN LOOP
# =========================

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame nahi mil raha")
        break

    h, w, _ = frame.shape

    # BGR -> RGB
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

    posture = "No Pose Detected"

    if result.pose_landmarks:

        landmarks = result.pose_landmarks[0]

        # MediaPipe Pose landmarks
        nose = landmarks[0]

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        left_hip = landmarks[23]
        right_hip = landmarks[24]

        # =========================
        # SHOULDER POINTS
        # =========================

        lx = left_shoulder.x * w
        ly = left_shoulder.y * h

        rx = right_shoulder.x * w
        ry = right_shoulder.y * h

        # =========================
        # HIP POINTS
        # =========================

        lhx = left_hip.x * w
        lhy = left_hip.y * h

        rhx = right_hip.x * w
        rhy = right_hip.y * h

        # =========================
        # SHOULDER ANGLE
        # =========================

        shoulder_angle = calculate_angle(
            lx,
            ly,
            rx,
            ry
        )

        # =========================
        # BODY CENTER
        # =========================

        shoulder_center_x = (
            left_shoulder.x +
            right_shoulder.x
        ) / 2

        shoulder_center_y = (
            left_shoulder.y +
            right_shoulder.y
        ) / 2

        hip_center_x = (
            left_hip.x +
            right_hip.x
        ) / 2

        hip_center_y = (
            left_hip.y +
            right_hip.y
        ) / 2

        # =========================
        # TORSO ANGLE
        # =========================

        torso_angle = math.degrees(
            math.atan2(
                hip_center_x - shoulder_center_x,
                hip_center_y - shoulder_center_y
            )
        )

        # =========================
        # POSTURE CLASSIFICATION
        # =========================

        if torso_angle > 8:

            posture = "Leaning Left"

        elif torso_angle < -8:

            posture = "Leaning Right"

        elif abs(shoulder_angle) > 12:

            posture = "Shoulders Tilted"

        else:

            posture = "Upright Posture"

        # =========================
        # DRAW LANDMARKS
        # =========================

        points = [
            nose,
            left_shoulder,
            right_shoulder,
            left_hip,
            right_hip
        ]

        for point in points:

            x = int(point.x * w)
            y = int(point.y * h)

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )

        # =========================
        # DRAW SHOULDERS
        # =========================

        cv2.line(
            frame,
            (int(lx), int(ly)),
            (int(rx), int(ry)),
            (0, 255, 0),
            3
        )

        # =========================
        # DRAW TORSO
        # =========================

        cv2.line(
            frame,
            (
                int(shoulder_center_x * w),
                int(shoulder_center_y * h)
            ),
            (
                int(hip_center_x * w),
                int(hip_center_y * h)
            ),
            (255, 0, 0),
            3
        )

        # =========================
        # DISPLAY
        # =========================

        cv2.putText(
            frame,
            f"Posture: {posture}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Torso Angle: {torso_angle:.1f}",
            (20, 75),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "No Pose Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "AI Interview - Posture Analysis",
        frame
    )

    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# =========================
# CLEANUP
# =========================

cap.release()
landmarker.close()
cv2.destroyAllWindows()