# THE WATCHDOG PROJECT — production excerpt (redacted)
# ----------------------------------------------------
# ACTIVITY PULSE — honesty rule, enforced in code:
# the vital sign is a metaphor rendered from MEASURED motion.
# The system never fabricates a data point. Ever.

act = max(tracked_speed_component, motion_field_component)
act_ema = act_ema * 0.94 + act * 0.06          # slow, calm envelope

bpm_target = REST_BPM + act_ema * DYNAMIC_RANGE
bpm += (bpm_target - bpm) * smoothing(dt)

# waveform + audio tick rendered from the same envelope — the beep the
# stream audience hears IS the room's measured activity
ecg_phase += dt * bpm / 60.0
if ecg_phase >= 1.0:
    ecg_phase -= 1.0
    audio.tick()

# sustained agitation — not spikes — trips the room-level alert
if act_ema > HIGH_ACTIVITY_FLOOR:
    alerts.high_activity(room)

# [ redacted: component weighting, camera-motion gating that keeps
#   pans and lighting changes out of the vital sign ]
