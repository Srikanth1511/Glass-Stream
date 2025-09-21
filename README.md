
# Glass XE → PC Minimal MJPEG Stream (and Viewer)

This bundle contains:
- **android-glass-streamer/** — Android (KitKat/API 19) project to run on **Google Glass XE**.  
  Opens the camera and serves MJPEG at `http://<GLASS_IP>:8080/stream.mjpeg`.  
  **MainActivity** shows the actual Glass IP/URL on screen.
- **pc-viewer/** — Python OpenCV viewer that connects to the stream and shows live video.
- **viewer_mediapipe.py** — Python + MediaPipe Hands viewer that overlays hand landmarks.

Run with Glass IP arg in terminal:
```bash
python viewer_mediapipe.py --url http://<GLASS_IP>:8080/stream.mjpeg --stride 2
````

---

## 1) Build & install on Glass (Android Studio)

1. Open **Android Studio** → *Open an existing project* → select `android-glass-streamer`.
2. Let it sync. (Keep `compileSdkVersion`/`targetSdkVersion` at **19**).
3. Connect Glass over ADB (`adb devices` should show it).
4. **Run** the `app` on Glass. (Or build + install manually):

   ```bash
   gradlew assembleDebug
   adb install -r app/build/outputs/apk/debug/app-debug.apk
   ```

### Start/Stop streaming

* On Glass, launch **GlassStream**.
* Tap **Start Stream** → foreground service starts, streaming MJPEG.
  The IP/URL is shown on screen (auto-detected).
* Tap **Stop Stream** → service stops.

---

## 2) View on PC (Python)

```bash
cd pc-viewer
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python viewer.py --url http://<GLASS_IP>:8080/stream.mjpeg
```

* Press **ESC** to quit.

---

## 3) Quick sanity check in a browser

On your PC:

```
http://<GLASS_IP>:8080/
```

You should see a simple page with `<img>` updating.

---

## 4) Find Glass IP

* On Glass: **Settings → Device Info → Status → IP address**
* Or from PC:

  ```bash
  adb shell ip addr show wlan0
  ```

---

## 5) Debugging FPS & Frames with adb logcat

StreamService logs frame capture/encode counts every \~30–60 frames.
On PC, run:

```bash
adb logcat -s StreamService
```

Typical output:

```
I/StreamService( 2827): Captured frames: 300 (640x480)
I/StreamService( 2827): Encoded JPEGs: 600 (320x240)
```

Use this to compare different preview sizes, JPEG quality, or stride settings.

---

## Notes

* The app uses the **legacy Camera API** + a simple **ServerSocket MJPEG server** (works on API 19).
* Recommended preview size: **640x480** (change in `StreamService.java`).
* Lower JPEG quality (40–55) = higher FPS.
* Glass and PC must be on the same Wi-Fi; allow port **8080** through firewall.

---

## Which IDE?

* **Android part** → use **Android Studio**
* **Python viewers** → run from terminal; edit in VS Code, PyCharm, etc.

