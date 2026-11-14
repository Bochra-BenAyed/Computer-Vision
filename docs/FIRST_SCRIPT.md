# Understanding `src/detection/detect_video.py`

This is the first building block of the whole project: **read a video and find the vehicles in it.**

## The big picture
A video is a sequence of images (frames), for example 25 per second. To "analyze a video" we
loop over frames and analyze each one as an image.

```
video file -> [frame 1] [frame 2] [frame 3] ...
                 |
                 v   for each frame
          YOLO model -> list of boxes (x1,y1,x2,y2, class, confidence)
                 |
                 v
     draw boxes on the frame -> write frame to output video
```

## What is YOLO?
YOLO ("You Only Look Once") is a neural network that looks at an image once and outputs, in
one pass, **bounding boxes** with a **class** (car, truck, person...) and a **confidence score**
(0 to 1). We use a version **pretrained on COCO**, a dataset with 80 classes that includes
`car` (id 2) and `truck` (id 7). So it works without training anything. This is called
*transfer learning* when we later adapt it to our own cameras.

`yolov8n.pt` is the "nano" model: small and fast, a bit less accurate. The weights file is
downloaded automatically the first time.

## Walkthrough of the script
1. **Arguments** (`argparse`): `--video` (input), `--out` (output), `--conf` (confidence
   threshold), `--max-frames` (to test quickly on a short part).
2. **Open the video**: `cv2.VideoCapture(path)` gives access to frames. We read width, height
   and fps so the output video has the same format.
3. **Load the model**: `YOLO("yolov8n.pt")`.
4. **Loop**: `cap.read()` returns `(ok, frame)`. The frame is a NumPy array of shape
   `(height, width, 3)` in **BGR** order (OpenCV uses BGR, not RGB).
5. **Detection**: `model(frame, conf=..., classes=[2, 7])`. `conf` drops uncertain detections;
   `classes` keeps only cars and trucks.
6. **Drawing**: for each box we read the corners, class and score, then draw a rectangle and a
   label with `cv2.rectangle` / `cv2.putText`.
7. **Output**: `VideoWriter` saves the annotated frames; a summary is printed at the end.

## Important limitation (this is your next learning step)
The script counts **detections per frame**. A single car crossing the scene appears in dozens of
frames, so the total is *not* the number of vehicles. To count each vehicle once we need:
1. **Tracking** (give each vehicle a persistent ID; e.g. ByteTrack, available in Ultralytics
   with `model.track(...)`),
2. a **virtual counting line**: count a vehicle when its ID crosses the line.

Each counted crossing becomes a row in the `passages` table, which feeds the flow computation.

## Experiments to try (and note in your report)
- Change `--conf` to 0.15 then 0.6. What happens to missed vehicles and false detections?
- Compare `yolov8n.pt` and `yolov8s.pt`: speed vs accuracy.
- Try a night or rainy video. Where does it fail?
- Which vehicles get mislabeled (vans, buses, motorbikes)? The spec only has car/truck.
