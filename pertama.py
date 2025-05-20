import cv2
import mediapipe as mp
import numpy as np
import math
import os

# Inisialisasi kamera dan efek
cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

# Define filter buttons
filter_buttons = [
    {"name": "Api", "x1": 10, "y1": 10, "x2": 90, "y2": 90, "video": "fire.mp4", "color": (0, 0, 255)},
    {"name": "Hijau", "x1": 100, "y1": 10, "x2": 180, "y2": 90, "video": "hijau.mp4", "color": (0, 255, 0)},
    {"name": "Merah", "x1": 190, "y1": 10, "x2": 270, "y2": 90, "video": "merah.mp4", "color": (0, 0, 255)},
    {"name": "Kuning", "x1": 280, "y1": 10, "x2": 360, "y2": 90, "video": "kuning.mp4", "color": (0, 255, 255)},
    {"name": "Oranye", "x1": 370, "y1": 10, "x2": 450, "y2": 90, "video": "oranye.mp4", "color": (0, 165, 255)},
]

# Initialize filter videos dictionary
filter_videos = {}

def load_video(video_path):
    if not os.path.exists(video_path):
        # Create a colored frame if video doesn't exist (for development/testing)
        dummy_video = np.ones((200, 200, 3), dtype=np.uint8)
        for btn in filter_buttons:
            if btn["video"] == os.path.basename(video_path):
                dummy_video[:] = btn["color"]
                break
        return dummy_video
    else:
        return cv2.VideoCapture(video_path)

# Load all videos or create dummy frames
for btn in filter_buttons:
    video_path = btn["video"]
    filter_videos[video_path] = load_video(video_path)

# Set default filter
current_filter = filter_buttons[0]["video"]
active_button_index = 0

def calc_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def is_finger_up(lm, tip_id, pip_id):
    return lm[tip_id].y < lm[pip_id].y

def get_fire_frame(video_source):
    if isinstance(video_source, np.ndarray):  # It's a dummy frame
        return video_source.copy()
    else:  # It's a video capture
        ret, frame = video_source.read()
        if not ret:
            video_source.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video_source.read()
        return frame

def overlay_fire_effect(frame, fire_src, x, y, size):
    # If fire_src is a numpy array (dummy frame), resize it
    if isinstance(fire_src, np.ndarray):
        fire_resized = cv2.resize(fire_src, (size, size))
    else:
        fire_frame = get_fire_frame(fire_src)
        fire_resized = cv2.resize(fire_frame, (size, size))
    
    hsv = cv2.cvtColor(fire_resized, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 50))
    mask_inv = cv2.bitwise_not(mask)
    
    # Add some randomness to the fire effect
    angle = np.random.randint(-15, 15)
    rot_matrix = cv2.getRotationMatrix2D((size // 2, size // 2), angle, 1)
    fire_rotated = cv2.warpAffine(fire_resized, rot_matrix, (size, size))
    
    h, w = frame.shape[:2]
    x1, y1 = x - size // 2, y - size // 2
    x2, y2 = x1 + size, y1 + size
    
    # Ensure the coordinates are within the frame bounds
    if 0 <= x1 < w and 0 <= y1 < h and x2 <= w and y2 <= h:
        roi = frame[y1:y2, x1:x2]
        
        # Ensure ROI and masks have the same dimensions
        if roi.shape[:2] == mask.shape[:2]:
            bg = cv2.bitwise_and(roi, roi, mask=mask)
            fg = cv2.bitwise_and(fire_rotated, fire_rotated, mask=mask_inv)
            combined = cv2.add(bg, fg)
            frame[y1:y2, x1:x2] = combined

def draw_buttons(frame):
    for i, btn in enumerate(filter_buttons):
        # Draw button background
        cv2.rectangle(frame, (btn["x1"], btn["y1"]), (btn["x2"], btn["y2"]), btn["color"], -1)
        
        # Highlight active button with blue border
        border_color = (255, 0, 0) if i == active_button_index else (200, 200, 200)
        border_thickness = 3 if i == active_button_index else 1
        cv2.rectangle(frame, (btn["x1"], btn["y1"]), (btn["x2"], btn["y2"]), border_color, border_thickness)
        
        # Add button label
        label = btn["name"]
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        text_x = btn["x1"] + (btn["x2"] - btn["x1"] - text_size[0]) // 2
        text_y = btn["y2"] + 15
        cv2.putText(frame, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Display current filter name in top left corner
    current_name = filter_buttons[active_button_index]["name"]
    cv2.putText(frame, f"Filter: {current_name}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# Main loop
cooldown_timer = 0
COOLDOWN_DURATION = 15  # frames before allowing another button press

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)  # Mirror the frame
    h, w, _ = frame.shape
    
    # Draw the filter buttons
    draw_buttons(frame)
    
    # Convert to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    if cooldown_timer > 0:
        cooldown_timer -= 1
    
    if results.multi_hand_landmarks:
        for idx, hand in enumerate(results.multi_hand_landmarks):
            hand_label = results.multi_handedness[idx].classification[0].label  # 'Left' or 'Right'
            lm = hand.landmark
            
            # Get important landmarks
            x_center = int(lm[9].x * w)  # Palm center
            y_center = int(lm[9].y * h)
            
            x_index_tip = int(lm[8].x * w)  # Index finger tip
            y_index_tip = int(lm[8].y * h)
            
            x_thumb = int(lm[4].x * w)
            y_thumb = int(lm[4].y * h)
            
            x_pinky = int(lm[20].x * w)
            y_pinky = int(lm[20].y * h)
            
            # Calculate hand width for effect sizing
            hand_width = int(calc_distance((x_thumb, y_thumb), (x_pinky, y_pinky)))
            hand_width = max(50, min(int(hand_width * 1.5), 300))
            
            # Check if index finger is touching any button
            if cooldown_timer == 0:
                for i, btn in enumerate(filter_buttons):
                    if btn["x1"] <= x_index_tip <= btn["x2"] and btn["y1"] <= y_index_tip <= btn["y2"]:
                        current_filter = btn["video"]
                        active_button_index = i
                        cooldown_timer = COOLDOWN_DURATION
                        break
            
            # Get current filter video source
            current_video_source = filter_videos[current_filter]
            
            # Detect raised fingers
            fingers_up = []
            for tip_id, pip_id in [(8, 6), (12, 10), (16, 14), (20, 18)]:  # Index, Middle, Ring, Pinky
                if is_finger_up(lm, tip_id, pip_id):
                    fingers_up.append(tip_id)
            
            # Show fire effect on fingertips
            for tip_id in fingers_up:
                x_finger = int(lm[tip_id].x * w)
                y_finger = int(lm[tip_id].y * h)
                overlay_fire_effect(frame, current_video_source, x_finger, y_finger, hand_width // 2)
            
            # Show fire effect on palm center
            overlay_fire_effect(frame, current_video_source, x_center, y_center, hand_width)
            
            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            
            # Draw a circle at the index fingertip
            cv2.circle(frame, (x_index_tip, y_index_tip), 10, (0, 255, 255), -1)
    
    # Show the output
    cv2.imshow("Interactive Fire Hands", frame)
    
    # Press Esc to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Clean up
cap.release()
for video in filter_videos.values():
    if not isinstance(video, np.ndarray):
        video.release()
cv2.destroyAllWindows()