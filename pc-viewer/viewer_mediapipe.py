import argparse, time, sys
import cv2, requests, numpy as np
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

def iter_jpeg_frames(url, timeout=10):
    """Robust MJPEG reader: ignores multipart headers; finds JPEG SOI/EOI markers."""
    while True:
        try:
            r = requests.get(url, stream=True, timeout=timeout)
            r.raise_for_status()
            buf = b""
            for chunk in r.iter_content(chunk_size=8192):
                if not chunk:
                    break
                buf += chunk
                a = buf.find(b'\xff\xd8')  # JPEG SOI
                b = buf.find(b'\xff\xd9')  # JPEG EOI
                if a != -1 and b != -1 and b > a:
                    jpg = buf[a:b+2]
                    buf = buf[b+2:]
                    yield jpg
        except Exception as e:
            print("[WARN] stream error:", e)
            time.sleep(0.5)  # brief backoff, then reconnect

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)  # e.g. http://<GLASS_IP>:8080/stream.mjpeg
    ap.add_argument("--max_hands", type=int, default=2)
    ap.add_argument("--min_det", type=float, default=0.5)
    ap.add_argument("--min_track", type=float, default=0.5)
    ap.add_argument("--stride", type=int, default=1, help="run MediaPipe every N frames")
    ap.add_argument("--flip", action="store_true")
    ap.add_argument("--rotate", choices=["none", "cw", "ccw", "180", "auto"], default="none",
                    help="Rotate frame: 90° cw/ccw, 180°, or auto portrait→landscape")

    ap.add_argument("--save", default="", help="CSV path to log landmarks")
    args = ap.parse_args()

    csv_file = None
    if args.save:
        csv_file = open(args.save, "w", buffering=1)
        cols = (["t_ms","hand_idx","label"] +
                [f"x{i}" for i in range(21)] +
                [f"y{i}" for i in range(21)] +
                [f"z{i}" for i in range(21)])
        csv_file.write(",".join(cols) + "\n")

    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=args.max_hands,
                           model_complexity=1,
                           min_detection_confidence=args.min_det,
                           min_tracking_confidence=args.min_track)

    last = time.time()
    frames = 0
    fps = 0.0

    cv2.namedWindow("Glass Camera + MediaPipe Hands", cv2.WINDOW_AUTOSIZE)

    for jpg in iter_jpeg_frames(args.url):
        img = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            continue

        if args.flip:
            img = cv2.flip(img, 1)

        # Rotate if requested
        if args.rotate == "cw":
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif args.rotate == "ccw":
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif args.rotate == "180":
            img = cv2.rotate(img, cv2.ROTATE_180)
        elif args.rotate == "auto":
            # If portrait, rotate to landscape automatically
            h, w = img.shape[:2]
            if h > w:
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

        frames += 1
        run = (frames % args.stride) == 0
        if run:
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = hands.process(rgb)
            if res.multi_hand_landmarks:
                for idx, lm in enumerate(res.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(img, lm, mp_hands.HAND_CONNECTIONS,
                                              mp_styles.get_default_hand_landmarks_style(),
                                              mp_styles.get_default_hand_connections_style())
                if csv_file and res.multi_handedness:
                    t_ms = int(time.time()*1000)
                    for hand_idx, (lm, handed) in enumerate(zip(res.multi_hand_landmarks, res.multi_handedness)):
                        label = handed.classification[0].label
                        xs = [f"{p.x:.6f}" for p in lm.landmark]
                        ys = [f"{p.y:.6f}" for p in lm.landmark]
                        zs = [f"{p.z:.6f}" for p in lm.landmark]
                        row = [str(t_ms), str(hand_idx), label] + xs + ys + zs
                        csv_file.write(",".join(row) + "\n")

        now = time.time()
        if now - last >= 1.0:
            fps = frames / (now - last)
            last, frames = now, 0

        # Debug: confirm what we're actually displaying
        h, w = img.shape[:2]
        # comment out this print if it's too chatty
        # print(f"[frame] {w}x{h}  aspect={w/float(h):.3f}")

        cv2.putText(img, f"FPS~{fps:.1f} stride={args.stride}", (8, 24),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2, cv2.LINE_AA)
        cv2.imshow("Glass Camera + MediaPipe Hands", img)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    hands.close()
    if csv_file: csv_file.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
