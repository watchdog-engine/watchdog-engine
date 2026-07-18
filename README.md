<div align="center">

# 🐕‍🦺 THE WATCHDOG PROJECT

**`WATCHING OVER THOSE WHO CAN'T CALL FOR HELP`**

Real-time computer vision monitoring for animal shelters and home care of sick or disabled dogs.

![Status](https://img.shields.io/badge/status-v0.3_SENTINEL-39ff74?style=flat-square&labelColor=0a120c)
![Runtime](https://img.shields.io/badge/runtime-CPU--only-39ff74?style=flat-square&labelColor=0a120c)
![Uptime](https://img.shields.io/badge/soak_test-32min_·_0_faults-39ff74?style=flat-square&labelColor=0a120c)
![Source](https://img.shields.io/badge/source-excerpts_only-ff3b3b?style=flat-square&labelColor=0a120c)
![Token](https://img.shields.io/badge/$WATCHDOG-CA:_SOON-3ea6ff?style=flat-square&labelColor=0a120c)

</div>

---

## What is this?

Shelters are understaffed. Night shifts are thin. A sick dog that stops moving in a
corner kennel can go unnoticed for hours — and hours are what decide outcomes.

The Watchdog Project is a **real-time perception layer** that plugs into ordinary
security cameras, tracks every animal in the room around the clock, and escalates to a
human the moment something stops looking normal. It is engineered for the worst footage
imaginable: black-and-white night vision, low contrast, curled-up sleeping animals, and
lenses that slowly sweep the room.

A significant part of the system is **already built and running** against real shelter
footage — you can watch it operate live during our public demonstration streams.

> ⚠️ **This repository intentionally contains functional excerpts, not the full
> pipeline.** The complete engine stays closed until the audit-ready release.
> What you see here is real production code with the reproducing parts redacted.

## Live output

Frames captured directly from the engine — every box, label, trail and vital sign is
computed in real time from measured data. The system renders **no synthetic data, ever.**

| | |
|:---:|:---:|
| ![Multi-track night analysis](docs/frame-01.png) | ![Stillness watch escalation](docs/frame-02.png) |
| *Multi-track night analysis* | *Stillness Watch escalation* |
| ![Motion lock and state labels](docs/frame-03.png) | ![Room map and activity pulse](docs/frame-04.png) |
| *Motion lock & state labels* | *Room map & Activity Pulse* |

## System modules

| # | Module | Status | What it does |
|---|--------|--------|--------------|
| 01 | **Detection Engine** | 🟢 ACTIVE | Night-IR-tuned deep learning detector; multi-profile inference recovers curled-up sleeping animals that low-contrast video usually hides |
| 02 | **Persistent Tracking** | 🟢 ACTIVE | Stable identities (`K9-01`, `K9-02`…) held across minutes; sleepers keep their track through intermittent detections; texture verification clears stale boxes |
| 03 | **Camera-Motion Compensation** | 🟢 ACTIVE | Sub-pixel ego-motion measurement; identities and immobility timers survive full camera pans — even off-frame |
| 04 | **Stillness Watch** | 🟢 ACTIVE | Per-animal immobility clock with staged escalation: on-screen warning → red flag → audible alarm → logged event |
| 05 | **Activity Pulse** | 🟢 ACTIVE | Room activity rendered as a live vital sign (waveform / BPM / audio tick) driven purely by measured motion |
| 06 | **Motion Sentinel** | 🟢 ACTIVE | Background-model layer locks onto new movement in under a second, hands it to the detector for confirmation |
| 07 | **Operator Console** | 🟢 ACTIVE | Status strip, event log, room-map radar, session stats, state labels (`SLEEPING / IDLE / WALKING / RUNNING`) |
| 08 | **Self-Healing Runtime** | 🟢 ACTIVE | Detects and repairs its own failure modes — corrupt frames, stalled readers, dropped outputs — unattended |
| 09 | **Camera Integration Layer** | 🟡 IN DEV | v1.0 target: direct RTSP/ONVIF-class ingestion, multi-room sessions, remote alert delivery |

## Field data

All figures below come from validation runs against genuine shelter night-camera footage.

```text
Detection uplift vs. baseline pipeline (24-frame set)   +73%
Sleeping / curled animals recovered in night IR         majority coverage
Moving-animal lock-on latency                           < 1.0 s
Inference cadence (CPU-only, no GPU present)            ~2.5 sweeps / s
Identity persistence through full camera pans           maintained
Continuous immobility timing verified                   11+ min unbroken
Unattended soak test  (crash / fault / manual repair)   32 min — 0 / 0 / 0
End-to-end alert chain (label→log→flash→audio)          verified
Synthetic data rendered on screen                       none — by policy
```

## A taste of the engine

From [`excerpts/stillness_watch.py`](excerpts/stillness_watch.py) — the module that
exists to save lives:

```python
for track in confirmed_tracks:
    still_min = track.still_minutes(now)
    if still_min >= IMMOBILE_ALERT_MIN:
        log.add(f"CHECK RECOMMENDED: {track.label} {still_min:.0f}m",
                RED, cooldown=300)
        audio.raise_alarm()          # double-tone, hard to ignore
        hud.flash_perimeter(5.0)     # full-frame red strobe
    elif still_min >= IMMOBILE_WARN_MIN:
        log.add(f"STILLNESS WATCH: {track.label} {still_min:.0f}m")
```

More excerpts in [`excerpts/`](excerpts/). Architecture overview in
[`ARCHITECTURE.md`](ARCHITECTURE.md).

## Roadmap

- [x] **v0.1 — FIRST LIGHT** · proof of concept on real shelter footage
- [x] **v0.2 — TECHNICAL** · operator console, alert engine, self-healing runtime
- [x] **v0.3 — SENTINEL** · perception overhaul: night-IR detection, persistent tracking, ego-motion compensation *(current build — shown in live streams)*
- [ ] **v0.9 — FIELD KIT** · real camera integration (RTSP/ONVIF), remote alerts *(funded by launch)*
- [ ] **v1.0 — DEPLOYMENT** · pilot shelters & home care — **applications open**

## Funding

The Watchdog Project is announced through a community token launch — **$WATCHDOG**.
Proceeds attributable to the project fund one thing: development. Camera integration,
field hardware for pilot shelters, and the engineering hours between v0.3 and v1.0.

The software already exists and you can watch it run live. The token is how a community
puts a monitoring system into shelters that could never afford one.

**Contract address: `SOON`** — published only on our official channels. Treat anything
else claiming to be us as fake.

## Links

- 🌐 **Website** — coming online with launch
- 𝕏 **X / Twitter** — [x.com](https://x.com)
- 💊 **pump.fun** — [live technical demonstrations](https://pump.fun)

---

<sub>The Watchdog Project is software in active development. It assists human caregivers
and does not replace veterinary care. All telemetry shown here is produced from real
measurements — the system renders no synthetic data. $WATCHDOG is a community token
created to fund development; nothing in this repository is financial advice.</sub>
