# Glass XE → PC Minimal MJPEG Stream (and Viewer)

This bundle contains:
- **android-glass-streamer/** — an Android (KitKat/API 19) project to run on **Google Glass XE**. It opens the camera and serves MJPEG on `http://<GLASS_IP>:8080/stream.mjpeg`.
- **pc-viewer/** — a tiny Python OpenCV viewer that connects to the above URL and shows the live feed.

## 1) Build & install on Glass (Android Studio)
1. Open **Android Studio** → *Open an existing project* → select `android-glass-streamer`.
2. Let it sync. (Keep `compileSdkVersion`/`targetSdkVersion` at **19**).
3. Connect Glass over ADB (`adb devices` should show it).
4. **Run** the `app` on Glass. (Or `adb install -r app-debug.apk` after building).

### Start/Stop streaming
- On Glass, launch **GlassStream** app.
- Tap **Start Stream** → It starts a foreground service and streams MJPEG.
- The URL will be `http://<GLASS_IP>:8080/stream.mjpeg`. Replace `<GLASS_IP>` with the IP Glass gets from your Wi‑Fi.

## 2) View on PC (Python)
```bash
cd pc-viewer
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python viewer.py
```
- Edit `URL` in `viewer.py` to match your Glass IP before running.
- Press **ESC** to quit.

## 3) Quick sanity check in a browser
On your PC, open:  
`http://<GLASS_IP>:8080/`  
You should see a page with the live `<img>`.

## 4)Find Glass IP
- On Glass: **Settings → Device Info → Status → IP address**, or
- From PC: `adb shell ip addr show wlan0` (look for `inet x.x.x.x`).

## Notes
- The Android app uses the **legacy Camera API** and a **simple ServerSocket** MJPEG server for maximum compatibility on Glass XE (Android 4.4).
- Keep preview size around **640x480** for good FPS over Wi‑Fi.
- If you see a black preview, make sure no other app is using the camera.
- You can later switch to H.264/RTSP or WebRTC for better bandwidth once bring-up is proven.

## Which IDE?
- **Android part** → open in **Android Studio**.
- **Python viewer** → run from terminal; you can edit in any editor (VS Code, PyCharm, etc.).
