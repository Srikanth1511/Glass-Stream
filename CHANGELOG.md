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
