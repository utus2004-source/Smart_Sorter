# Standalone script for a quick check of a new model.
# It is not part of the pipeline and is run directly.
from ultralytics import YOLO
import cv2

# Update the path here when a new model is used
model = YOLO("models/model.pt")
frame_count = 0

results = model(source=0, show=True, conf=0.5, imgsz=640, stream=True, verbose=False)

for r in results:
    frame_count += 1

    if frame_count % 30 == 0:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                print(f"DETECTED: {r.names[cls]} ({conf:.2f})")
        else:
            print("NOTHING")

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break
