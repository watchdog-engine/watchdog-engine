# THE WATCHDOG PROJECT — production excerpt (redacted)
# ----------------------------------------------------
# Cameras drift. Tracks must not.
#
# Consumer shelter cameras sweep the room slowly — slowly enough that
# frame-to-frame measurement drowns in noise. Scene shift is therefore
# measured sub-pixel against a ROLLING REFERENCE frame, where it
# accumulates into a clean signal, then applied to every track.
# Identities and immobility timers survive full pans of the room.

(sdx, sdy), _ = cv2.phaseCorrelate(ref_frame, current_frame)
total_shift = hypot(sdx, sdy)

if total_shift > NOISE_FLOOR:
    delta = to_full_res(sdx - applied.x, sdy - applied.y)
    world.shift_all_tracks(delta)     # boxes, anchors, trails — everything
    applied.update(sdx, sdy)

if reference_expired(ref_frame) or total_shift > CORRELATION_LIMIT:
    carry_residual_shift()            # nothing is lost between references
    ref_frame = promote(current_frame)

# fast pans are a separate mode: analysis pauses, shift integrates
# frame-to-frame, tracks re-align on settle.
# [ redacted: reference cycling cadence, noise floor calibration,
#   interaction with detection-result alignment ]
