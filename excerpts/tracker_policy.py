# THE WATCHDOG PROJECT — production excerpt (redacted)
# ----------------------------------------------------
# Sleeping dogs don't move — so intermittent detections are fused into
# one persistent identity instead of a flickering box. Lifetime policy
# is asymmetric: patience for sleepers, scrutiny for movers.

if track.is_stationary():
    ttl = LONG_HOLD                    # sleepers keep their identity
    if track.content_changed(frame):   # texture verification
        track.strikes += 1             # 3 strikes -> box is stale, drop
    else:
        track.strikes = 0
else:
    ttl = SHORT_HOLD                   # movers must keep confirming

# Off-frame persistence: a stationary animal panned out of view is NOT
# forgotten. Its coordinates keep shifting with the measured scene
# motion; when the camera sweeps back, the detector re-matches it in
# place — same identity, same immobility clock.

if not track.in_view:
    track.survive_until(far_out_of_world or ttl_expired)

# [ redacted: identity fusion — association metric, cross-class
#   suppression, confirmation policy, merge rules ]
