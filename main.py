import cv2
import mediapipe as mp
import numpy as np
import imageio
import os
import math
import collections

# Inisialisasi modul hand tracking Mediapipe dengan threshold deteksi 0.7 dan maksimal 2 tangan
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1)

# Fungsi untuk load efek GIF dari folder, setiap frame bisa di-flip horizontal
def load_effects(folder_path, flip_horizontal=True):
    effects = {}
    for filename in os.listdir(folder_path):              # Loop tiap file di folder efek
        name, ext = os.path.splitext(filename)             # Pisah nama dan ekstensi file
        full_path = os.path.join(folder_path, filename)    # Path lengkap file
        if ext == ".gif":                                   # Kalau file GIF, proses
            gif = imageio.mimread(full_path)                # Baca semua frame GIF
            frames = [cv2.flip(np.array(f), 1) if flip_horizontal else np.array(f) for f in gif]  # Flip jika perlu
            effects[name] = {"type": "gif", "frames": frames}  # Simpan frames ke dictionary efek
    return effects

# Fungsi overlay efek (GIF) di frame kamera pada posisi (x,y) dengan ukuran tertentu
def overlay_effect(base_frame, effect_frame, x, y, size=200):
    h, w = base_frame.shape[:2]                            # Ukuran frame utama
    effect_resized = cv2.resize(effect_frame, (size, size), interpolation=cv2.INTER_AREA)  # Resize efek
    if effect_resized.shape[2] == 4:                        # Kalau ada alpha channel (RGBA)
        effect_rgb = effect_resized[:, :, :3]              # Ambil RGB
        alpha_mask = effect_resized[:, :, 3] / 255.0       # Alpha sebagai mask transparansi
    else:
        effect_rgb = effect_resized                         # Kalau tanpa alpha, pakai RGB
        alpha_mask = np.ones((size, size))                  # Mask penuh (opaque)

    # Hitung area overlay, pusat di (x,y)
    x1, y1 = x - size // 2, y - size // 2
    x2, y2 = x1 + size, y1 + size

    # Cegah overlay keluar batas frame
    if x1 < 0 or y1 < 0 or x2 > w or y2 > h:
        return

    roi = base_frame[y1:y2, x1:x2]                         # Region of interest pada frame utama
    # Blend pixel antara efek dan background berdasarkan alpha mask
    for c in range(3):
        roi[:, :, c] = (alpha_mask * effect_rgb[:, :, c] + (1 - alpha_mask) * roi[:, :, c]).astype(np.uint8)
    base_frame[y1:y2, x1:x2] = roi                          # Update frame utama dengan overlay

# Fungsi cek apakah tangan dalam posisi fist (kepalan)
def is_fist(lm):
    x12, y12 = lm[12].x, lm[12].y                          # Koordinat jari tengah (landmark 12)
    x9, y9 = lm[9].x, lm[9].y                              # Koordinat pergelangan tangan (landmark 9)
    dist = ((x12 - x9)**2 + (y12 - y9)**2)**0.5            # Hitung jarak Euclidean
    return dist < 5                                        # Kalau jarak kecil, dianggap kepalan

cwd = os.getcwd()                                         # Dapatkan current working directory
effect_folder = os.path.join(cwd, "Tugas_besar_MultiMedia", "effects")  # Path folder efek GIF
all_effects = load_effects(effect_folder)                 # Load semua efek GIF

effect_frames = all_effects["efek-api-unscreen"]["frames"]  # Ambil frames GIF efek tertentu
effect_index = 0                                          # Index frame awal

cap = cv2.VideoCapture(0)                                 # Buka webcam

alpha = 0.3                                              # Faktor smoothing posisi tangan
smooth_x, smooth_y = None, None                           # Variabel posisi tangan ter-smoothing

position_history = collections.deque(maxlen=10)          # Riwayat posisi tangan untuk efek bounce
bounce_amplitude = 20                                    # Amplitudo gerak bounce efek
bounce_speed = 0.5                                       # Kecepatan osilasi bounce
frame_count = 0                                          # Counter frame untuk hitung bounce

while True:
    ret, frame = cap.read()                              # Baca frame dari webcam
    if not ret:
        break                                           # Stop kalau gagal baca frame

    frame = cv2.flip(frame, 1)                           # Flip frame horizontal (mirror)
    frame = cv2.resize(frame, (960, 720))                # Resize frame ke resolusi tetap
    frame_count += 1

    h, w = frame.shape[:2]                               # Ambil ukuran frame
    min_dim = min(h, w)                                  # Cari dimensi terkecil untuk crop square
    x_start, y_start = (w - min_dim) // 2, (h - min_dim) // 2  # Koordinat crop tengah
    frame_square = frame[y_start:y_start + min_dim, x_start:x_start + min_dim]  # Crop jadi square

    rgb = cv2.cvtColor(frame_square, cv2.COLOR_BGR2RGB)  # Convert ke RGB untuk Mediapipe
    results = hands.process(rgb)                          # Proses deteksi tangan dengan Mediapipe
    
    if results.multi_hand_landmarks:                      # Kalau ada tangan terdeteksi
        lm = results.multi_hand_landmarks[0].landmark     # Ambil landmark tangan pertama
        palm_landmarks = [1, 5, 9, 13, 17]                 # Landmark yang dianggap pusat telapak tangan

        if is_fist(lm):                                   # Kalau tangan kepalan
            smooth_x, smooth_y = None, None                # Reset smoothing posisi tangan
            position_history.clear()                        # Bersihkan riwayat posisi

        # Hitung rata-rata koordinat landmark telapak tangan (x,y)
        cx = int(np.mean([lm[i].x for i in palm_landmarks]) * min_dim)
        cy = int(np.mean([lm[i].y for i in palm_landmarks]) * min_dim)

        palm_z_avg = np.mean([lm[i].z for i in palm_landmarks])  # Rata-rata kedalaman landmark telapak tangan

        if palm_z_avg:                                      # Kalau ada nilai kedalaman
            if smooth_x is None:                            # Jika smoothing belum ada
                smooth_x, smooth_y = cx, cy                 # Set smoothing awal ke posisi tangan sekarang
            else:
                # Smooth posisi tangan untuk gerakan lebih halus dengan faktor alpha
                smooth_x = int(alpha * cx + (1 - alpha) * smooth_x)
                smooth_y = int(alpha * cy + (1 - alpha) * smooth_y)

            position_history.append((smooth_x, smooth_y))   # Simpan posisi tangan terbaru

            # Hitung offset bounce menggunakan fungsi sinusoidal untuk efek animasi naik-turun
            bounce_offset = int(bounce_amplitude * math.sin(bounce_speed * frame_count))
            dynamic_y = smooth_y - 150 + bounce_offset      # Offset vertikal untuk posisi overlay efek

            # Tampilkan efek GIF dengan posisi overlay yang sudah dihitung
            overlay_effect(frame_square, effect_frames[effect_index], smooth_x + 10, dynamic_y, size=350)
            effect_index = (effect_index + 1) % len(effect_frames)  # Frame GIF berganti tiap loop
        else:
            smooth_x, smooth_y = None, None                   # Reset smoothing kalau data z tidak valid
            position_history.clear()                          # Bersihkan riwayat posisi

    cv2.imshow("Hand Effect", frame_square)                  # Tampilkan frame dengan overlay efek
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):                          # Keluar jika tekan ESC atau 'q'
        break

cap.release()                                                # Lepas webcam
cv2.destroyAllWindows()                                      # Tutup semua jendela OpenCV
