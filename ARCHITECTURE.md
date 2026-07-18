# Architecture Overview

> High-level design of the Watchdog perception stack. Implementation parameters,
> tuning values and the fusion logic that make this pipeline work in production are
> **intentionally withheld**.

## Design constraints

The engine was designed against the hardest realistic conditions:

- **CPU-only.** No GPU assumed, ever. Shelters run on donated hardware.
- **Night-IR footage.** Black-and-white, low contrast, noisy.
- **Sleeping animals.** A curled-up dog is the single hardest pose for off-the-shelf
  detectors — and 80% of a shelter night.
- **Moving cameras.** Consumer PTZ cameras drift and sweep. Identity must survive it.
- **Unattended runtime.** Days of operation without a human touching it.

## Pipeline

```text
                        ┌──────────────────────────────────────┐
 camera feed ──────────►│  INGEST + FRAME GUARD                │
                        │  corrupt-frame shield · self-heal    │
                        └───────────────┬──────────────────────┘
                                        │
              ┌─────────────────────────┼──────────────────────────┐
              ▼                         ▼                          ▼
 ┌────────────────────────┐ ┌────────────────────────┐ ┌────────────────────────┐
 │ EGO-MOTION UNIT        │ │ DETECTION THREAD       │ │ MOTION SENTINEL        │
 │ sub-pixel scene-shift  │ │ night-IR-tuned DNN     │ │ background model       │
 │ measurement against a  │ │ multi-profile          │ │ <1s lock-on for new    │
 │ rolling reference      │ │ inference, async       │ │ movement, size/travel  │
 │ [ params redacted ]    │ │ [ profiles redacted ]  │ │ gated  [ redacted ]    │
 └───────────┬────────────┘ └───────────┬────────────┘ └───────────┬────────────┘
             │                          │                          │
             └──────────────┬───────────┴──────────────────────────┘
                            ▼
             ┌──────────────────────────────┐
             │ PERSISTENT TRACKER           │
             │ identity fusion · long-hold  │
             │ for sleepers · texture       │
             │ verification · off-frame     │
             │ persistence through pans     │
             │ [ fusion logic redacted ]    │
             └──────────────┬───────────────┘
                            ▼
        ┌───────────────────┴────────────────────┐
        ▼                                        ▼
 ┌─────────────────────┐                 ┌─────────────────────┐
 │ BEHAVIOR & ALERTS   │                 │ OPERATOR CONSOLE    │
 │ state machine:      │                 │ HUD render · event  │
 │ SLEEPING / IDLE /   │                 │ log · room map ·    │
 │ WALKING / RUNNING   │                 │ activity pulse ·    │
 │ stillness clocks →  │                 │ session stats       │
 │ staged escalation   │                 └──────────┬──────────┘
 └─────────────────────┘                            ▼
                                          live video output
                                          (virtual camera / stream)
```

## Key engineering decisions

**Detection runs asynchronously.** The render loop never waits on inference. Boxes are
carried between sweeps by the tracker, so output stays at full frame rate on CPU.

**Sleepers get patience, movers get scrutiny.** Track lifetime policy is asymmetric:
a stationary animal's identity is held on a long horizon and verified by texture
correlation; a moving animal must keep re-confirming on a short one.

**The camera is never trusted to be still.** Scene shift is measured continuously at
sub-pixel precision against a rolling reference and applied to every track, anchor and
immobility timer. Identities survive full pans of the room — including animals that
temporarily leave the frame.

**Honesty is enforced in code.** Every number on screen traces back to a measurement.
There is no code path that fabricates a data point.

## What is not in this repository

- Model selection, inference profiles and preprocessing chain
- Tracker fusion thresholds and lifetime policy values
- Alert calibration data
- The production runtime (self-healing, watchdog-restart and output layers)

These remain closed until the audit-ready release.
