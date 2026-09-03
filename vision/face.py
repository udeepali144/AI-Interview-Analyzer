import cv2
import mediapipe as mp
from pathlib import Path


# --------------------------------------------------
# 1. Model ka path
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "face_detector.tflite"

print("Model path:", MODEL_PATH)

if not MODEL_PATH.exists():
    print("ERROR: face_detector.tflite nahi mila!")
    print("Expected path:", MODEL_PATH)
    exit()


# --------------------------------------------------
# 2. MediaPipe Face Detector setup
# --------------------------------------------------

BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions

options = FaceDetectorOptions(
    base_options=BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    min_detection_confidence=0.5
)

detector = FaceDetector.create_from_options(options)

print("Face detector successfully load ho gaya!")


# --------------------------------------------------
# 3. Camera
# --------------------------------------------------

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera open nahi ho raha")
    exit()

print("Camera started. Q dabakar exit karo.")


# --------------------------------------------------
# 4. Main loop
# --------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame nahi mil raha")
        break

    # OpenCV BGR -> MediaPipe RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # MediaPipe image
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    # Face detection
    result = detector.detect(mp_image)

    # --------------------------------------------------
    # 5. Detected faces par rectangle
    # --------------------------------------------------

    for detection in result.detections:

        bbox = detection.bounding_box

        x = bbox.origin_x
        y = bbox.origin_y
        w = bbox.width
        h = bbox.height

        # Green rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Confidence
        score = detection.categories[0].score

        cv2.putText(
            frame,
            f"Face {score:.2f}",
            (x, max(30, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # --------------------------------------------------
    # 6. Status text
    # --------------------------------------------------

    if len(result.detections) > 0:
        status = "FACE DETECTED"
        color = (0, 255, 0)
    else:
        status = "NO FACE"
        color = (0, 0, 255)

    cv2.putText(
        frame,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2
    )


    # Show camera
    cv2.imshow("AI Interview - Face Detection", frame)


    # Q = quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# 7. Cleanup
# --------------------------------------------------

cap.release()
cv2.destroyAllWindows()
detector.close()