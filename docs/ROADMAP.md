# Learning roadmap

| Step | What we learn | Demo |
|---|---|---|
| 0. Foundations | Reading video, frames, color spaces, Git workflow | Script that saves frames |
| 1. Classical CV | Background subtraction (MOG2), thresholding, morphology, contours | Moving-object boxes |
| 2. Deep detection | YOLO, confidence, NMS, transfer learning | Cars and trucks detected (`detect_video.py`) |
| 3. Tracking and counting | Persistent IDs, line crossing | Per-vehicle count |
| 4. Time series | Sliding windows, baseline mean/std | Flow curve vs baseline |
| 5. Anomaly detector | Threshold, temporal confirmation, hysteresis | Alerts on a simulated incident |
| 6. Evaluation | Precision, recall, detection latency | Results table and plots |

Compare step 1 (MOG2) and step 2 (YOLO): measure where each fails (shadows, night, rain, trucks).

## Roles (rotate at least once)
- **Vision**: detection, tracking, classification
- **Data / DB**: schema, aggregation, synthetic history
- **Anomaly**: profile, detector, calibration
- **Evaluation / report**: test scenarios, metrics, report, demo

## Open questions for the supervisor
- Real footage available? Live RTSP or files only?
- Synthetic history acceptable for the profile?
- The spec requires 3 confirmation windows (15 min) but also an alert under 5 min: which wins?
- `profil_reference` has no primary key and alerts have no location field in the spec; we
  added a composite PK and a `cameras` table with coordinates.
