"""First demo: read a video, run YOLO on every frame, draw boxes, count vehicles.

Usage:
    python src/detection/detect_video.py --video data/videos/test.mp4 --out outputs/annotated.mp4

What it does, step by step:
    1. Open the video with OpenCV and read its properties (size, fps).
    2. Load a pretrained YOLO model (it already knows "car" and "truck").
    3. For each frame: run the model, keep only cars and trucks, draw the boxes.
    4. Write the annotated frames to a new video and print a summary.

Note: this counts *detections per frame*, NOT unique vehicles. The same car
appears in many frames. Counting unique vehicles needs tracking (next step).
"""
import argparse
from collections import Counter
from pathlib import Path

import cv2
from ultralytics import YOLO

# COCO class ids that YOLO uses: 2 = car, 7 = truck
VEHICLE_CLASSES = {2: "voiture", 7: "camion"}
COLORS = {"voiture": (0, 200, 0), "camion": (0, 140, 255)}  # BGR


def parse_args():
    p = argparse.ArgumentParser(description="Run YOLO on a video file.")
    p.add_argument("--video", required=True, help="input video path")
    p.add_argument("--out", default="outputs/annotated.mp4", help="output video path")
    p.add_argument("--model", default="yolov8n.pt",
                   help="YOLO weights (n=nano is fastest; try yolov8s.pt for better accuracy)")
    p.add_argument("--conf", type=float, default=0.35,
                   help="minimum confidence to keep a detection (0 to 1)")
    p.add_argument("--max-frames", type=int, default=0,
                   help="stop after N frames (0 = whole video), handy for quick tests")
    return p.parse_args()


def main():
    args = parse_args()

    # 1. Open the video
    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        raise SystemExit(f"Cannot open video: {args.video}")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    print(f"Video: {width}x{height} at {fps:.1f} fps")

    # Prepare the output video writer
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(args.out, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    # 2. Load the model (downloads the weights the first time)
    model = YOLO(args.model)

    totals = Counter()   # detections summed over all frames
    frame_idx = 0

    # 3. Loop over frames
    while True:
        ok, frame = cap.read()          # ok=False at end of video
        if not ok:
            break

        # Run detection. classes=[2,7] tells YOLO to ignore everything but car/truck.
        result = model(frame, conf=args.conf, classes=list(VEHICLE_CLASSES), verbose=False)[0]

        for box in result.boxes:
            label = VEHICLE_CLASSES[int(box.cls)]
            score = float(box.conf)
            x1, y1, x2, y2 = map(int, box.xyxy[0])   # corners of the box in pixels
            totals[label] += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), COLORS[label], 2)
            cv2.putText(frame, f"{label} {score:.2f}", (x1, max(y1 - 6, 12)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[label], 2)

        writer.write(frame)
        frame_idx += 1
        if frame_idx % 50 == 0:
            print(f"  {frame_idx} frames processed")
        if args.max_frames and frame_idx >= args.max_frames:
            break

    # 4. Clean up and summarize
    cap.release()
    writer.release()
    print(f"\nDone: {frame_idx} frames. Annotated video saved to {args.out}")
    print(f"Detections summed over frames: {dict(totals)}")


if __name__ == "__main__":
    main()
