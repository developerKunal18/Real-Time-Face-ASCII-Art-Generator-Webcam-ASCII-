
import cv2
import os
import time

# Characters from dark -> light (you can reorder/change)
ASCII_CHARS = "@%#*+=-:. "
ASCII_CHARS = ASCII_CHARS[::-1]  # reverse if you prefer darker -> denser

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pixel_to_char(pixel_value):
    """Map 0-255 pixel to an index in ASCII_CHARS safely."""
    # scale pixel (0-255) to index range 0..len(ASCII_CHARS)-1
    n = len(ASCII_CHARS)
    idx = int(pixel_value / 255 * (n - 1))
    if idx < 0:
        idx = 0
    elif idx >= n:
        idx = n - 1
    return ASCII_CHARS[idx]

def frame_to_ascii(frame_gray, width=120):
    """
    Convert a grayscale frame (numpy 2D array, 0-255) to ASCII art string.
    width = number of characters per line (columns).
    """
    h, w = frame_gray.shape
    aspect_ratio = h / float(w)
    # Factor 0.45 compensates for terminal character aspect ratio (height > width)
    new_height = max(1, int(width * aspect_ratio * 0.45))
    # Use INTER_AREA for downscaling for better result and speed
    resized = cv2.resize(frame_gray, (width, new_height), interpolation=cv2.INTER_AREA)

    lines = []
    n = len(ASCII_CHARS)
    # Build ASCII line by line
    for row in resized:
        line_chars = [pixel_to_char(int(pixel)) for pixel in row]
        lines.append("".join(line_chars))
    return "\n".join(lines)

def main():
    cap = cv2.VideoCapture(0)  # 0 = default camera

    if not cap.isOpened():
        print("❌ Cannot access webcam. Make sure it's plugged in and not used by another app.")
        return

    print("🎥 Starting ASCII webcam (press 'q' to quit)...")
    # small delay to allow camera warm-up
    time.sleep(0.5)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to grab frame.")
                break

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Convert frame to ascii (reduce width if too slow)
            ascii_art = frame_to_ascii(gray, width=100)

            # Clear terminal and print
            clear()
            print(ascii_art)

            # Check for 'q' key: use small wait time and read keyboard state via OpenCV
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\n👋 Interrupted by user.")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("👋 Exiting...")

if __name__ == "__main__":
    main()
