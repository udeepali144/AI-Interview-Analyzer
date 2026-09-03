import cv2
import mediapipe as mp
import math
import json
import os


from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from behaviour import BehaviourTracker
from vision_score import calculate_vision_score, generate_feedback


# =====================================================
# MODEL PATHS
# =====================================================

FACE_MODEL = "models/face_landmarker.task"
POSE_MODEL = "models/pose_landmarker.task"


# =====================================================
# FACE LANDMARKER
# =====================================================

face_base_options = python.BaseOptions(
    model_asset_path=FACE_MODEL
)

face_options = vision.FaceLandmarkerOptions(
    base_options=face_base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_faces=1,
    output_face_blendshapes=True
)

face_landmarker = vision.FaceLandmarker.create_from_options(
    face_options
)


# =====================================================
# POSE LANDMARKER
# =====================================================

pose_base_options = python.BaseOptions(
    model_asset_path=POSE_MODEL
)

pose_options = vision.PoseLandmarkerOptions(
    base_options=pose_base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_poses=1
)

pose_landmarker = vision.PoseLandmarker.create_from_options(
    pose_options
)


# =====================================================
# HELPER FUNCTION
# =====================================================

def distance(p1, p2):

    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


def get_blendshape(blendshapes, name):

    for item in blendshapes:

        if item.category_name == name:
            return item.score

    return 0.0


# =====================================================
# CAMERA
# =====================================================

# ==========================================
# VISION RESULT FILE
# ==========================================

vision_file = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "vision_result.json"
    )
)

if os.path.exists(vision_file):
    os.remove(vision_file)

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("Camera open nahi ho raha")
    exit()
tracker = BehaviourTracker()

timestamp = 0


# =====================================================
# MAIN LOOP
# =====================================================

while True:

    ret, frame = cap.read()

    if not ret:

        print("Frame nahi mil raha")
        break


    h, w, _ = frame.shape


    # -------------------------------------------------
    # BGR -> RGB
    # -------------------------------------------------

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )


    timestamp += 1


    # =================================================
    # FACE ANALYSIS
    # =================================================

    face_result = face_landmarker.detect_for_video(
        mp_image,
        timestamp
    )


    face_status = "No Face"
    eye_status = "Unknown"
    gaze_status = "Unknown"
    head_status = "Unknown"
    expression_status = "Unknown"


    if face_result.face_landmarks:

        landmarks = face_result.face_landmarks[0]

        face_status = "Face Detected"


        # ------------------------------------------------
        # EYE OPEN / CLOSED
        # ------------------------------------------------

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


        if average_eye_open > 0.015:

            eye_status = "Eyes Open"

        else:

            eye_status = "Eyes Closed"


        # ------------------------------------------------
        # GAZE
        # ------------------------------------------------

        if average_eye_open > 0.015:

            left_iris = landmarks[468]
            right_iris = landmarks[473]

            left_eye_left = landmarks[33]
            left_eye_right = landmarks[133]

            right_eye_left = landmarks[362]
            right_eye_right = landmarks[263]


            left_ratio = (
                left_iris.x -
                left_eye_left.x
            ) / (
                left_eye_right.x -
                left_eye_left.x
            )


            right_ratio = (
                right_iris.x -
                right_eye_left.x
            ) / (
                right_eye_right.x -
                right_eye_left.x
            )


            gaze_ratio = (
                left_ratio +
                right_ratio
            ) / 2


            if 0.40 <= gaze_ratio <= 0.60:

                gaze_status = "Looking Center"

            elif gaze_ratio < 0.40:

                gaze_status = "Looking Left"

            else:

                gaze_status = "Looking Right"


        # ------------------------------------------------
        # HEAD POSITION
        # ------------------------------------------------

        nose = landmarks[1]

        left_face = landmarks[234]
        right_face = landmarks[454]


        horizontal_ratio = (
            nose.x - left_face.x
        ) / (
            right_face.x - left_face.x
        )


        if horizontal_ratio < 0.40:

            head_status = "Head Left"

        elif horizontal_ratio > 0.60:

            head_status = "Head Right"

        else:

            head_status = "Head Center"


        # ------------------------------------------------
        # FACIAL CUES
        # ------------------------------------------------

        if face_result.face_blendshapes:

            blendshapes = face_result.face_blendshapes[0]


            smile_left = get_blendshape(
                blendshapes,
                "mouthSmileLeft"
            )

            smile_right = get_blendshape(
                blendshapes,
                "mouthSmileRight"
            )


            smile = (
                smile_left +
                smile_right
            ) / 2


            if smile > 0.45:

                expression_status = "Smile Cue"

            else:

                expression_status = "Neutral Cue"


        # ------------------------------------------------
        # DRAW FACE LANDMARKS
        # ------------------------------------------------

        for point in landmarks:

            x = int(point.x * w)
            y = int(point.y * h)

            cv2.circle(
                frame,
                (x, y),
                1,
                (0, 255, 0),
                -1
            )


    # =================================================
    # POSE ANALYSIS
    # =================================================

    pose_result = pose_landmarker.detect_for_video(
        mp_image,
        timestamp
    )


    posture_status = "No Pose"


    if pose_result.pose_landmarks:

        pose = pose_result.pose_landmarks[0]


        left_shoulder = pose[11]
        right_shoulder = pose[12]

        left_hip = pose[23]
        right_hip = pose[24]


        shoulder_center_x = (
            left_shoulder.x +
            right_shoulder.x
        ) / 2


        hip_center_x = (
            left_hip.x +
            right_hip.x
        ) / 2


        torso_difference = (
            hip_center_x -
            shoulder_center_x
        )


        if torso_difference > 0.08:

            posture_status = "Leaning Left"

        elif torso_difference < -0.08:

            posture_status = "Leaning Right"

        else:

            posture_status = "Upright"


        # Draw shoulders

        cv2.line(
            frame,
            (
                int(left_shoulder.x * w),
                int(left_shoulder.y * h)
            ),
            (
                int(right_shoulder.x * w),
                int(right_shoulder.y * h)
            ),
            (255, 0, 0),
            3
        )


        # Draw hips

        cv2.line(
            frame,
            (
                int(left_hip.x * w),
                int(left_hip.y * h)
            ),
            (
                int(right_hip.x * w),
                int(right_hip.y * h)
            ),
            (255, 0, 0),
            3
        )



        # =================================================
# BEHAVIOUR TRACKING
# =================================================

        face_detected = (
         face_status == "Face Detected"
)

        eye_contact = (
          gaze_status == "Looking Center"
)

        head_center = (
          head_status == "Head Center"
)

        upright = (
          posture_status == "Upright"
)

        tracker.update(
          face_detected,
          eye_contact,
          head_center,
          upright
)


    # =================================================
    # DISPLAY INFORMATION
    # =================================================

    cv2.putText(
        frame,
        face_status,
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    cv2.putText(
        frame,
        eye_status,
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    cv2.putText(
        frame,
        "Gaze: " + gaze_status,
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    cv2.putText(
        frame,
        head_status,
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    cv2.putText(
        frame,
        posture_status,
        (20, 150),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    cv2.putText(
        frame,
        expression_status,
        (20, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


    # =================================================
    # SHOW CAMERA
    # =================================================
# ==========================================
    # LIVE VISION RESULT
    # ==========================================

    live_report = tracker.get_report()

    live_vision_score = calculate_vision_score(
        live_report["eye_contact"],
        live_report["head_stability"],
        live_report["upright_posture"],
        live_report["face_presence"]
    )

    live_feedback = generate_feedback(
        live_report["eye_contact"],
        live_report["head_stability"],
        live_report["upright_posture"],
        live_report["face_presence"]
    )

    live_vision_result = {
        "vision_score": live_vision_score,
        "eye_contact": live_report["eye_contact"],
        "head_stability": live_report["head_stability"],
        "posture": live_report["upright_posture"],
        "face_presence": live_report["face_presence"],
        "feedback": live_feedback
    }

    with open(
        vision_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            live_vision_result,
            file,
            indent=4
        )


    cv2.imshow(
        "AI Interview - Vision Engine",
        frame
    )


    # Press Q to quit

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break

    # ==========================================
# FINAL VISION INTERVIEW REPORT
# ==========================================

report = tracker.get_report()

print("\n==============================")
print("VISION INTERVIEW REPORT")
print("==============================")

print("Face Presence:", report["face_presence"], "%")
print("Eye Contact:", report["eye_contact"], "%")
print("Head Stability:", report["head_stability"], "%")
print("Upright Posture:", report["upright_posture"], "%")


# ==========================================
# VISION SCORE
# ==========================================

vision_score = calculate_vision_score(
    report["eye_contact"],
    report["head_stability"],
    report["upright_posture"],
    report["face_presence"]
)

print("\nVision Score:", vision_score, "/ 100")



# ==========================================
# VISION FEEDBACK
# ==========================================

feedback = generate_feedback(
    report["eye_contact"],
    report["head_stability"],
    report["upright_posture"],
    report["face_presence"]
)

print("\nFeedback:")

for item in feedback:
    print("-", item)

# Save final vision result

vision_result = {
    "vision_score": vision_score,
    "eye_contact": report["eye_contact"],
    "head_stability": report["head_stability"],
    "posture": report["upright_posture"],
    "face_presence": report["face_presence"],
    "feedback": feedback
}

print("\nFINAL_VISION_RESULT")

print(json.dumps(vision_result))

# Save result to JSON file

# ==========================================
# SAVE FINAL VISION RESULT TO JSON
# ==========================================





with open(vision_file, "w", encoding="utf-8") as file:

    json.dump(
        vision_result,
        file,
        indent=4
    )

print("\n✅ Vision result saved successfully!")
print("📁 Saved at:", vision_file)








# =====================================================
# CLEANUP
# =====================================================

cap.release()

face_landmarker.close()

pose_landmarker.close()

cv2.destroyAllWindows()