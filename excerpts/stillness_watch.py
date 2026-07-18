# THE WATCHDOG PROJECT — production excerpt (redacted)
# ----------------------------------------------------
# Stillness escalation: the module that exists to save lives.
# Every confirmed animal carries a live immobility clock. Cross a
# threshold and the system escalates — on-screen warning, red-flag
# status, audible alarm, logged event.
#
# Thresholds are configured per facility. Alerts fire only on tracks
# recently re-confirmed by the detector — the system never raises an
# alarm it cannot stand behind.

for track in confirmed_tracks:
    if not track.recently_confirmed(now):
        continue                      # honesty gate: no stale-box alarms

    still_min = track.still_minutes(now)

    if still_min >= IMMOBILE_ALERT_MIN:
        log.add(f"CHECK RECOMMENDED: {track.label} {still_min:.0f}m",
                RED, cooldown=300)
        audio.raise_alarm()           # double-tone, hard to ignore
        hud.flash_perimeter(5.0)      # full-frame red strobe
        stats.alerts += 1

    elif still_min >= IMMOBILE_WARN_MIN:
        log.add(f"STILLNESS WATCH: {track.label} {still_min:.0f}m",
                GRAY, cooldown=300)
        # label switches to red "STILL Xm" on the live overlay

# [ redacted: immobility measurement — anchor policy, scale-adaptive
#   movement epsilon, interaction with the motion sentinel ]
