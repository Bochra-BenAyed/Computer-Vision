# Smart Traffic: Anomaly Detection from Camera Flow

Computer Vision course project. The system uses road camera footage to **detect and
classify vehicles** (car / truck), compute **traffic flow** per 5-minute window, compare it
to a **historical reference profile**, and raise an **alert** when flow drops abnormally
(possible accident, obstacle or breakdown).

> Main goal of this project: **learn**. Every step has a small demo and a short note.

## Pipeline

```
video -> frames -> detection (YOLO) -> tracking/counting -> PASSAGES (DB)
      -> flow per sliding window -> compare to reference profile -> ALERT
```

## Repository layout

| Folder | Purpose |
|---|---|
| `src/acquisition/` | Reading video files / RTSP streams |
| `src/detection/` | Vehicle detection, tracking, classification |
| `src/aggregation/` | Flow per sliding window and statistics |
| `src/profile/` | Reference profile (mean/std per camera, weekday, time slot) |
| `src/anomaly/` | Threshold rule with temporal confirmation |
| `src/db/` | SQL schema and database access |
| `data/videos/` | Test videos (**not committed**, too large) |
| `notebooks/` | Experiments and learning notebooks |
| `tests/` | Automated tests |
| `docs/` | Setup guides, team notes, report material |
| `outputs/` | Generated results (**not committed**) |

## Quick start (WSL2 / Ubuntu)

```bash
git clone <URL_OF_YOUR_REPO>
cd trafic-intelligent
bash setup_wsl.sh            # installs tools, creates .venv, installs dependencies
source .venv/bin/activate
```

Put a test video in `data/videos/` (see `docs/DATA.md`), then run the first demo:

```bash
python src/detection/detect_video.py --video data/videos/test.mp4 --out outputs/annotated.mp4
```

It writes an annotated video with boxes around cars and trucks and prints counts.
Full explanation: `docs/FIRST_SCRIPT.md`.

## Documentation

- `docs/SETUP_WSL.md`: WSL2 setup, step by step
- `docs/GIT_WORKFLOW.md`: how we work together on GitHub
- `docs/FIRST_SCRIPT.md`: how `detect_video.py` works, line by line
- `docs/DATA.md`: where to get videos and datasets
- `docs/ROADMAP.md`: learning roadmap and team roles

## Key parameters (from the specification)

| Parameter | Value |
|---|---|
| Window size | 5 min |
| `alert_threshold` | 0.60 |
| `n` (consecutive windows) | 3 |
| `resolution_threshold` | 0.20 |
| Learning window | 4 to 8 weeks |

## Team

| Name | Role |
|---|---|
| _to fill_ | Vision |
| _to fill_ | Data / DB |
| _to fill_ | Anomaly detection |
| _to fill_ | Evaluation / report |
