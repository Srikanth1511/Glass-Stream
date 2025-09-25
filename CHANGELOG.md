## [1.2] - — EE Adaptation & Orientation Fixes (2025-09-24)
### Target: Google Glass Enterprise Edition (EE)

**Core Fixes**
- Default preset = **VGA 4:3 (640×480)** → ~19–20 FPS.
- Buffering enabled by default (4 callback buffers).
- EE orientation handling done in the python viewer.

**Resolution Handling**
- `pickExactOrClosest(...)` prefers exact preset.
- `isAspectApprox(...)` runs only at configure time.
- Added logs:
  - Supported sizes dump
  - Chosen preview size + reasoning
  - Confirmed HAL preview size
  - Per-minute FPS summary

**Minor**
- Thread-local JPEG buffer reuse (1 MB).
- Intent-driven runtime knobs:
  - `preset`, `buffering`, `quality`, `rotateDegrees`.

**Known Results (EE)**
- 640×480 @ quality 60 → ~19–20 FPS, minimal tearing.
- Higher resolutions reduce FPS and raise thermals.

---

## [1.1] — MJPEG Streaming Stabilization (2025-09-22)

- Double-buffer path to avoid tearing under load.
- Snapshot copy before JPEG encode for consistent sizing.
- Logging for preset selection + frame counts.

---

## [1.0] — Initial Build (2025-09-20)

- Basic preview callback → NV21 → JPEG → socket stream.
- Simple size chooser (default often 640×480 on Glass).




## [1.1] - 2025-09-22
### Added
- **IP/URL shown in-app**: MainActivity displays `http://<GLASS_IP>:8080/stream.mjpeg`.
- **Keepalive with screen off**: Service acquires PARTIAL_WAKE_LOCK + Wi-Fi lock (app context) so streaming continues when display sleeps.
- **ADB logcat docs**: README shows `adb logcat -s StreamService` for FPS/health. Runs in cmd with platform tools folder. 

### Changed
- **Service lifecycle**: Stop streaming only on swipe-down (`isFinishing()`), not every pause.
- **Non-sticky service**: `START_NOT_STICKY` to avoid unexpected restarts.
- **Preview pipeline**: Preview-callback-with-buffer + single encoder thread; latest JPEG shared to all clients.

### Fixed
- Correct multipart MJPEG headers (`boundary=frame`) and pacing to reduce jitter.
- Removed default-locale/ hardcoded-strings warnings (moved to `strings.xml`, `Locale.US` for IP formatting).

### Notes
- Suggested preview: **640×480**, JPEG quality ~**45–55** for better FPS. this can be found in currentJpeg (), line
`yuv.compressToJpeg(new Rect(0, 0, previewW, previewH), 60, baos);`
- See README for MediaPipe viewer CLI and troubleshooting.
