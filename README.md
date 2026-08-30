# Smart Sorter

Vision system for an automatic waste sorting bin.

A camera watches the drop zone of the bin, a YOLO model recognises the material
of the object that was thrown in, and the system sends a single bin number over
a serial link to an ESP32 that physically moves the item into the right
container.

The same code runs on a laptop (development) and on a Raspberry Pi (target
device). The two setups differ **only** by `config/config.yaml`.

---

## 1. Project assumptions

These are the design rules the whole codebase follows. They are the reason the
project is split the way it is.

| # | Assumption | Consequence in the code |
|---|------------|-------------------------|
| 1 | **One frame must never trigger the mechanics.** A model can flip class for a split second. | `PredictionStabilizer` — a class is accepted only when it dominates the last N frames. |
| 2 | **Only the drop zone matters.** An object lying next to the bin is not waste to be sorted. | `ROIFilter` — a detection counts only when its box centre is inside the ROI. |
| 3 | **The hardware must not be spammed.** A servo cannot react 30 times per second. | `DecisionFilter` — cooldown between sends + "send only on change". |
| 4 | **Decision logic never talks to hardware.** | Logic returns a plain `int` (bin number); `Communication` is a separate interface. |
| 5 | **The model is replaceable.** A retrained model must not force code changes. | Class names live inside the model file, `classes.yaml` only maps name → bin number, and the mapping is verified at startup. |
| 6 | **Every implementation is swappable.** USB camera → Pi camera, YOLO → another detector, serial → MQTT. | `Camera`, `Detector`, `Communication` are interfaces (`base.py` / `detector.py`), concrete classes implement them. |
| 7 | **Display is debug only.** | `Drawer` never influences the pipeline and can be switched off (`display.enabled: false`) for a headless Pi. |
| 8 | **No behaviour is hardcoded.** Thresholds, ROI, ports, colours — all tunable. | Single `config/config.yaml`, loaded by `app/config.py`. |
| 9 | **The logic is testable without a camera and without hardware.** | Pure functions on `Prediction` objects, covered by `pytest` with fake YOLO results. |

---

## 2. Software / hardware requirements

### Software

| Component | Version / notes |
|-----------|-----------------|
| Python | 3.10+ (developed on 3.12) |
| `ultralytics` | YOLO inference engine |
| `opencv-python` | camera capture + preview window |
| `pyyaml` | configuration loading |
| `pyserial` | serial link to the ESP32 |
| `pytest` | unit tests |

Exact list: [`requirements.txt`](requirements.txt).

### Hardware

| Part | Role |
|------|------|
| Laptop **or** Raspberry Pi 4/5 | runs this repository |
| USB / CSI camera | 640×640 view of the drop zone |
| ESP32 | receives the bin number and drives the sorting mechanism |
| USB serial cable | ESP32 ↔ host (`/dev/ttyUSB0`, 115200 baud) |

### Model

A trained YOLO model file is expected at `models/model.pt`.
**It is not stored in the repository** (`*.pt` is gitignored) — copy your own
model there. The class names inside the model must match the keys in
`config/classes.yaml`.

---

## 3. Installation

```bash
git clone <repo-url>
cd Smart_Sorter

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Then put your trained model at `models/model.pt`.

## 4. Running

```bash
python -m app.main
```

Press **q** in the preview window to stop (only when `display.enabled: true`).

Quick standalone check of a new model, without the pipeline:

```bash
python tools/check_model.py     # ESC to quit
```

Tests:

```bash
pytest
```

---

## 5. How it works

```
camera frame
     |
     v
[ YoloDetector ]      raw YOLO output
     |
     v
[ PredictionParser ]  raw output  ->  Prediction[]   (border of the model)
     |
     v
[ ROIFilter ]         spatial filter: is it inside the drop zone?
     |
     v
[ PredictionStabilizer ]  time filter: is the class stable over N frames?
     |
     v
[ Decision ]          class name -> bin number   (classes.yaml)
     |
     v
[ DecisionFilter ]    cooldown + only-on-change  ->  bin number or None
     |
     v
[ SerialESP32 ]       "3\n"  ->  ESP32
```

`Drawer` and `ModelLogger` hang off the side of the pipeline: they receive
**all** detections (including the ones rejected by the ROI) so a badly set ROI
is visible on the image, but they never affect the decision.

### Data model

Everything after the parser works on `Prediction` objects
(`class_id`, `class_name`, `confidence`, `x1`, `y1`, `x2`, `y2`, `center()`),
so no part of the system except `PredictionParser` and `YoloDetector` knows
that YOLO is being used at all.

---

## 6. Repository layout

```
app/
  main.py                    wiring: builds every component and starts the pipeline
  config.py                  loads config.yaml + classes.yaml, resolves paths

  camera/
    base.py                  Camera interface
    opencv_camera.py         USB / CSI camera via OpenCV

  vision/
    detector.py              Detector interface
    yolo_detector.py         Ultralytics YOLO implementation
    prediction.py            Prediction — one detection
    parser.py                raw YOLO results -> Prediction[]
    filter.py                ROIFilter (spatial) + DecisionFilter (rate limit)
    stabilization.py         PredictionStabilizer (time filter)

  decision/
    decision.py              Prediction[] -> bin number

  communication/
    base.py                  Communication interface
    serial_esp32.py          serial implementation

  output/
    drawer.py                preview window, boxes, ROI, confidence colours
    model_logger.py          console debug log

  pipeline/
    vision_pipeline.py       the order of the steps, works on interfaces only

config/
  config.yaml                all tunable parameters
  classes.yaml               class name -> bin number

models/model.pt              trained model (not in git)
tools/check_model.py         standalone model check
tests/                       unit tests of the logic
```

---

## 7. Configuration

All parameters live in [`config/config.yaml`](config/config.yaml).

| Section | Key | Meaning |
|---------|-----|---------|
| `camera` | `type`, `camera_id`, `width`, `height`, `fps` | which camera implementation and how it is opened |
| `model` | `path`, `confidence`, `image_size` | model file and YOLO inference settings |
| `roi` | `x1`,`y1`,`x2`,`y2` | drop zone; only boxes centred here are considered |
| `stabilization` | `frames`, `threshold` | history length and required agreement (e.g. 5 frames, 0.6 → 3/5 must agree) |
| `decision_filter` | `cooldown_frames`, `send_only_on_change` | minimum gap between two sends; block repeating the same command |
| `display` | `enabled`, `window_name`, `debug_log_every`, box/text styling, `low_confidence`, `medium_confidence` | preview window; colour thresholds: red < low ≤ yellow < medium ≤ green |
| `communication` | `enabled`, `type`, `port`, `baudrate` | serial link; set `enabled: false` to develop without the ESP32 |

Class mapping is in [`config/classes.yaml`](config/classes.yaml):

```yaml
classes:
  Glass: 1
  Aluminium_Metal: 2
  Plastic: 3
```

At startup `main.py` compares the model's own class names with these keys and
prints a warning for anything missing — otherwise the system would silently
produce no decision for that class.

### Typical setups

**Laptop / development**

```yaml
display:       { enabled: true }
communication: { enabled: false }
```

**Raspberry Pi / production**

```yaml
display:       { enabled: false }
communication: { enabled: true, port: /dev/ttyUSB0 }
```

---

## 8. Communication protocol

One decision = one line of ASCII text on the serial port:

```
3\n
```

The number is the bin number from `classes.yaml`. Nothing is sent when no
stable object is present, when the cooldown has not elapsed, or when the same
decision is already active.

---

## 9. Extending the system

| Goal | What to do |
|------|------------|
| New camera (e.g. Pi Camera) | implement `Camera` in `app/camera/`, swap it in `main.py` |
| New detector | implement `Detector` + a parser producing `Prediction[]` |
| New transport (MQTT, HTTP, GPIO) | implement `Communication` in `app/communication/` |
| New waste class | retrain the model, add the class name → bin number to `classes.yaml` |
| Different sensitivity | change `confidence`, `stabilization`, `roi` in `config.yaml` — no code change |

Nothing above requires touching `VisionPipeline`, which is the point of the
interface split.

---

## 10. Tests

`pytest` covers the parts that carry the logic, without a camera or hardware:

| File | Covers |
|------|--------|
| `tests/test_parser.py` | YOLO output → `Prediction`, using fake YOLO objects |
| `tests/test_filter.py` | ROI in/out, cooldown, send-only-on-change |
| `tests/test_stabilization.py` | stable class accepted, single wrong frame ignored, highest confidence wins |
| `tests/test_decision.py` | known class → bin number, unknown class → `None` |

`conftest.py` makes the `app` package importable from the project root.
