import cv2, requests, numpy as np

URL = "http://<GLASS_IP>:8080/stream.mjpeg"  # <-- change to your Glass IP

BOUNDARY = b"--frame"

def frames():
    r = requests.get(URL, stream=True, timeout=10)
    r.raise_for_status()
    buf = b""
    for chunk in r.iter_content(chunk_size=4096):
        if not chunk:
            break
        buf += chunk
        # Find JPEG start (FF D8) and end (FF D9)
        a = buf.find(b'\xff\xd8')
        b = buf.find(b'\xff\xd9')
        if a != -1 and b != -1 and b > a:
            jpg = buf[a:b+2]
            buf = buf[b+2:]  # keep remainder in buffer
            yield jpg

def main():
    print("Connecting to", URL)
    for jpg in frames():
        img = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            continue
        cv2.imshow("Glass Camera Live", img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
