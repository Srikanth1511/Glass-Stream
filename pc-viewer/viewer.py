import argparse, time
import cv2, requests, numpy as np

BOUNDARY = b"--frame"

def iter_jpeg_frames(url, timeout=10):
    """Robust MJPEG reader: finds JPEG SOI/EOI markers and yields JPEG bytes."""
    while True:
        try:
            r = requests.get(url, stream=True, timeout=timeout)
            r.raise_for_status()
            buf = b""
            for chunk in r.iter_content(chunk_size=8192):
                if not chunk:
                    break
                buf += chunk
                a = buf.find(b'\xff\xd8')  # SOI
                b = buf.find(b'\xff\xd9')  # EOI
                if a != -1 and b != -1 and b > a:
                    jpg = buf[a:b+2]
                    buf = buf[b+2:]
                    yield jpg
        except Exception as e:
            print("[WARN] stream error:", e)
            time.sleep(0.5)  # brief backoff then reconnect

def apply_rotation(img, mode):
    if mode == "cw":
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif mode == "ccw":
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif mode == "180":
        return cv2.rotate(img, cv2.ROTATE_180)
    elif mode == "auto":
        h, w = img.shape[:2]
        if h > w:
            return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="e.g. http://<GLASS_IP>:8080/stream.mjpeg")
    ap.add_argument("--flip", action="store_true", help="mirror horizontally")
    ap.add_argument("--rotate", choices=["none", "cw", "ccw", "180", "auto"], default="none",
                    help="Rotate frame: 90° cw/ccw, 180°, or auto portrait→landscape")
    args = ap.parse_args()

    print("Connecting to", args.url)
    cv2.namedWindow("Glass Live", cv2.WINDOW_AUTOSIZE)

    last = time.time()
    frames = 0
    fps = 0.0

    for jpg in iter_jpeg_frames(args.url):
        img = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            continue

        if args.flip:
            img = cv2.flip(img, 1)
        if args.rotate != "none":
            img = apply_rotation(img, args.rotate)

        frames += 1
        now = time.time()
        if now - last >= 1.0:
            fps = frames / (now - last)
            last, frames = now, 0

        cv2.putText(img, f"FPS~{fps:.1f} rot={args.rotate} flip={args.flip}",
                    (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2, cv2.LINE_AA)
        cv2.imshow("Glass Live", img)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
