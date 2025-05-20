import cv2
import mediapipe as mp
import numpy as np
import imageio
import os

# Inisialisasi MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=2)

# Load semua efek dari folder
def load_effects(folder_path, flip_horizontal=True):
    effects = {}
    for filename in os.listdir(folder_path):
        name, ext = os.path.splitext(filename)
        full_path = os.path.join(folder_path, filename)

        if ext == ".gif":
            gif = imageio.mimread(full_path)
            frames = []
            for f in gif:
                bgr = cv2.cvtColor(np.array(f), cv2.COLOR_RGBA2BGR)
                if flip_horizontal:
                    bgr = cv2.flip(bgr, 1)
                frames.append(bgr)
            effects[name] = {
                "type": "gif",
                "frames": frames
            }

        elif ext == ".mp4":
            cap = cv2.VideoCapture(full_path)
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if flip_horizontal:
                    frame = cv2.flip(frame, 1)
                frames.append(frame)
            cap.release()
            effects[name] = {
                "type": "mp4",
                "frames": frames
            }
    return effects

# Fungsi overlay
def overlay_effect(base_frame, effect_frame, x, y, size=200):
    h, w = base_frame.shape[:2]
    effect_resized = cv2.resize(effect_frame, (size, size))

    x1 = x - size // 2
    y1 = y - size // 2
    x2 = x1 + size
    y2 = y1 + size

    if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
        return

    roi = base_frame[y1:y2, x1:x2]
    blended = cv2.addWeighted(roi, 0.5, effect_resized, 0.5, 0)
    base_frame[y1:y2, x1:x2] = blended

# Load efek
# Dapatkan path direktori kerja saat ini
cwd = os.getcwd()
effect_folder = os.path.join(cwd, "Tugas_besar_MultiMedia", "effects")
all_effects = load_effects(effect_folder)

# Pilih efek
current_effect_name = "sembur-efek"
effect_index = 0
effect_data = all_effects.get(current_effect_name, {})
current_effect_frames = effect_data.get("frames", [])
effect_type = effect_data.get("type", "gif")

# Buka kamera
cap = cv2.VideoCapture(0)
prev_positions = [None, None]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (960, 720))
    # Crop ke square biar hilang warning MediaPipe
    h, w = frame.shape[:2]
    min_dim = min(h, w)
    x_start = (w - min_dim) // 2
    y_start = (h - min_dim) // 2
    frame_square = frame[y_start:y_start + min_dim, x_start:x_start + min_dim]

    rgb = cv2.cvtColor(frame_square, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            landmark = hand_landmarks.landmark[9]
            cx = int(landmark.x * min_dim)
            cy = int(landmark.y * min_dim)

            if i >= len(prev_positions):
                prev_positions.append(None)

            if prev_positions[i] is None:
                prev_positions[i] = (cx, cy)

            px, py = prev_positions[i]
            alpha = 0.3
            x = int(px * (1 - alpha) + cx * alpha)
            y = int(py * (1 - alpha) + cy * alpha)
            prev_positions[i] = (x, y)

            if current_effect_frames:
                current_frame = current_effect_frames[effect_index % len(current_effect_frames)]
                overlay_effect(frame_square, current_frame, x, y, size=200)

        effect_index += 1

    cv2.imshow("Hand Effect", frame_square)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
