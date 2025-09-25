# Google Glass XE / EE → PC MJPEG Stream & Viewer

Stream the **camera feed from Google Glass** (Explorer or Enterprise Edition) over Wi-Fi to a PC viewer.

---

## Branches

- **main** → for **Glass XE (Explorer Edition)**
  - KitKat / API 19 project
  - Orientation matches XE sensor (no rotation flags needed)
  - Recommended preset: **640×480, JPEG quality 45–55** → smoother FPS

- **glass-ee** → for **Glass EE (Enterprise Edition)**
  - Orientation requires **270° rotation**
  - Default preset: **VGA 640×480 (4:3)** with **buffering ON** (4 buffers)
  - Runtime flags (`adb am startservice`) control:
    - `preset`, `buffering`, `quality`, `rotateDegrees`
  - Typical EE performance: **~19–20 FPS** steady @ quality 50–60
  - PC viewer adds `--rotate` arg to orient EE streams correctly

---

## PC Viewer

Works for both XE and EE:

```bash
cd pc-viewer

# XE (default orientation)
python viewer.py --url http://<GLASS_IP>:8080/stream.mjpeg

# EE (rotate to match display)
python viewer.py --url http://<GLASS_IP>:8080/stream.mjpeg --rotate cw
```

---

## Build & Install on Glass

1. Open **Android Studio** → *Open an existing project* → select `android-glass-streamer`.
2. Let it sync (keep `compileSdkVersion` / `targetSdkVersion` = **19**).
3. Connect Glass over ADB (`adb devices` should show it).
4. Run `app` on Glass (or build + install manually).

---

## Starting & Stopping the Stream

**On Glass:**
- Launch **GlassStream** → tap **Start Stream**
  - Foreground service starts, IP/URL auto-detected & shown on screen
- Tap **Stop Stream** to stop

**From PC (Windows cmd inside `platform-tools`):**

```bash
adb shell am start -W -a android.intent.action.MAIN     -c android.intent.category.LAUNCHER     -n com.srikanth.glassstream/.MainActivity
```

---

## Sanity Checks

- **Test stream link:** open in browser
  ```
  http://<GLASS_IP>:8080/
  ```  
  You should see a simple `<img>` refreshing.

- **Find Glass IP:**
  - On Glass: *Settings → Device Info → Status → IP address*
  - Or via PC:
    ```bash
    adb shell ip addr show wlan0
    ```  

- **Check FPS via logcat:**
  ```bash
  adb logcat -s StreamService
  ```  
  Example output:
  ```
  I/StreamService(2827): Captured frames: 300 (640x480)
  I/StreamService(2827): Encoded JPEGs: 600 (320x240)
  ```  
  Use to compare preview sizes, JPEG quality, stride, and EE presets.

---

## Notes

- Uses **legacy Camera API** + **ServerSocket MJPEG server** (API 19-compatible).
- Recommended preview: **640×480** (set in `StreamService.java`).
- Lower JPEG quality (40–50) = higher FPS.  
  Current line in `currentJpeg()`:
  ```java
  yuv.compressToJpeg(new Rect(0, 0, previewW, previewH), 60, baos);
  ```
- Glass & PC must share same Wi-Fi; open port **8080** in firewall.
- EE defaults: 640×480, ~19–20 FPS with buffering.
  - For **1080p (1920×1080)**: switch to `preset 2` at line 44 in `StreamService.java` (EE branch).  
    Performance: ~8–12 FPS, unstable.

---

## IDEs

- **Android code:** Android Studio
- **Python viewer:** run from terminal; edit with VS Code, PyCharm, etc.  
