import cv2
import mediapipe as mp
import numpy as np
import imageio
import os
import math
import collections
from typing import Dict, List, Optional, Tuple

class HandEffectTracker:
    def __init__(self, effects_folder: str = "effects"):
        # Initialize MediaPipe with optimized settings
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,  # Lower tracking confidence for better performance
            model_complexity=1  # Use simpler model for better FPS
        )
        
        # Load effects once at initialization
        self.effects = self._load_effects(effects_folder)
        self.hand_states = {}
        self.frame_count = 0
        
        # Optimized configuration
        self.config = {
            'alpha': 0.8,                # Increased smoothing
            'base_effect_size': 180,     # Base size for reference
            'max_effect_size': 400,
            'min_effect_size': 60,
            'effect_y_offset': -120,
            'size_smoothing': 0.3,       # Smoothing for size changes
            'hand_size_scale': 1.5,      # Multiplier for hand size to effect size
            'reference_hand_size': 120,  # Reference hand size for scaling
            'fist_threshold': 0.08,      # More reliable fist detection
            'stability_threshold': 15,   # Minimum movement to update position
            'finger_effect_size': 80,    # Size for single finger effects
            'finger_size_scale': 0.8,    # Scale factor for finger effects
        }
        
        # Cache frequently used values
        self.palm_landmarks = [0, 5, 9, 13, 17]  # More stable landmarks
        
    def _load_effects(self, folder_path: str, flip_horizontal: bool = True) -> Dict:
        """Load GIF effects with error handling and optimization"""
        effects = {}
        
        if not os.path.exists(folder_path):
            print(f"Warning: Effects directory not found: {folder_path}")
            return effects
        
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith('.gif'):
                continue
                
            name = os.path.splitext(filename)[0]
            full_path = os.path.join(folder_path, filename)
            
            try:
                gif_frames = imageio.mimread(full_path)
                if flip_horizontal:
                    frames = [cv2.flip(np.array(f), 1) for f in gif_frames]
                else:
                    frames = [np.array(f) for f in gif_frames]
                
                effects[name] = {
                    "type": "gif", 
                    "frames": frames,
                    "frame_count": len(frames)
                }
                print(f"Loaded effect '{name}' with {len(frames)} frames")
                
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        
        return effects
    
    def _detect_gesture(self, landmarks) -> Tuple[str, Optional[Tuple[float, float]]]:
        """Detect hand gesture and return gesture type with position"""
        try:
            # Define finger landmarks: [tip, pip, mcp] for each finger
            fingers = {
                'thumb': [4, 3, 2],
                'index': [8, 6, 5],
                'middle': [12, 10, 9],
                'ring': [16, 14, 13],
                'pinky': [20, 18, 17]
            }
            
            extended_fingers = []
            finger_positions = {}
            
            # Check each finger
            for finger_name, (tip, pip, mcp) in fingers.items():
                if finger_name == 'thumb':
                    # Thumb: check horizontal distance (special case)
                    is_extended = abs(landmarks[tip].x - landmarks[mcp].x) > 0.04
                else:
                    # Other fingers: tip should be above pip and mcp
                    is_extended = (landmarks[tip].y < landmarks[pip].y and 
                                 landmarks[tip].y < landmarks[mcp].y)
                
                if is_extended:
                    extended_fingers.append(finger_name)
                    finger_positions[finger_name] = (landmarks[tip].x, landmarks[tip].y)
            
            # Determine gesture
            if len(extended_fingers) == 0:
                return "fist", None
            elif len(extended_fingers) == 1:
                finger_name = extended_fingers[0]
                return f"single_{finger_name}", finger_positions[finger_name]
            else:
                return "open_hand", None
                
        except Exception as e:
            print(f"Gesture detection error: {e}")
            return "unknown", None
    
    def _calculate_palm_center(self, landmarks) -> Tuple[float, float, float]:
        """Calculate stable palm center position"""
        x_coords = [landmarks[i].x for i in self.palm_landmarks]
        y_coords = [landmarks[i].y for i in self.palm_landmarks]
        z_coords = [landmarks[i].z for i in self.palm_landmarks if landmarks[i].z is not None]
        
        cx = np.mean(x_coords)
        cy = np.mean(y_coords)
        cz = np.mean(z_coords) if z_coords else None
        
        return cx, cy, cz
    
    def _calculate_hand_size(self, landmarks, frame_dims: Tuple[int, int]) -> float:
        """Calculate hand size based on key landmark distances"""
        min_dim = min(frame_dims)
        
        # Method 1: Distance from wrist to middle finger tip
        wrist = landmarks[0]
        middle_tip = landmarks[12]
        hand_length = math.sqrt(
            (middle_tip.x - wrist.x)**2 + (middle_tip.y - wrist.y)**2
        ) * min_dim
        
        # Method 2: Palm width (distance between pinky and index MCP)
        index_mcp = landmarks[5]
        pinky_mcp = landmarks[17]
        palm_width = math.sqrt(
            (pinky_mcp.x - index_mcp.x)**2 + (pinky_mcp.y - index_mcp.y)**2
        ) * min_dim
        
        # Method 3: Thumb span (wrist to thumb tip)
        thumb_tip = landmarks[4]
        thumb_span = math.sqrt(
            (thumb_tip.x - wrist.x)**2 + (thumb_tip.y - wrist.y)**2
        ) * min_dim
        
        # Combine measurements for more stable size estimation
        # Use weighted average: hand_length is most reliable
        hand_size = (hand_length * 0.6 + palm_width * 1.8 + thumb_span * 0.4)
        
        return hand_size
    
    def _overlay_effect_optimized(self, base_frame: np.ndarray, effect_frame: np.ndarray, 
                                x: int, y: int, size: int) -> None:
        """Optimized overlay with bounds checking and performance improvements"""
        h, w = base_frame.shape[:2]
        
        # Early bounds checking
        half_size = size // 2
        x1, y1 = max(0, x - half_size), max(0, y - half_size)
        x2, y2 = min(w, x + half_size), min(h, y + half_size)
        
        # Skip if completely out of bounds
        if x1 >= x2 or y1 >= y2:
            return
        
        # Calculate effect region
        effect_x1 = half_size - (x - x1)
        effect_y1 = half_size - (y - y1)
        effect_x2 = effect_x1 + (x2 - x1)
        effect_y2 = effect_y1 + (y2 - y1)
        
        # Resize effect frame only once
        try:
            effect_resized = cv2.resize(effect_frame, (size, size), 
                                      interpolation=cv2.INTER_LINEAR)
            
            # Extract the region we need
            effect_region = effect_resized[effect_y1:effect_y2, effect_x1:effect_x2]
            
            if effect_region.shape[2] == 4:  # RGBA
                effect_rgb = effect_region[:, :, :3]
                alpha = effect_region[:, :, 3:4] / 255.0
                
                # Vectorized blending
                roi = base_frame[y1:y2, x1:x2]
                blended = (alpha * effect_rgb + (1 - alpha) * roi).astype(np.uint8)
                base_frame[y1:y2, x1:x2] = blended
            else:  # RGB
                base_frame[y1:y2, x1:x2] = effect_region
                
        except Exception as e:
            print(f"Overlay error: {e}")
    
    def _update_hand_state(self, hand_idx: int, landmarks, frame_dims: Tuple[int, int]) -> None:
        """Update hand state with improved smoothing and stability"""
        min_dim = min(frame_dims)
        
        # Initialize hand state if needed
        if hand_idx not in self.hand_states:
            self.hand_states[hand_idx] = {
                'smooth_x': None, 'smooth_y': None,
                'smooth_size': None, 'frame_index': 0,
                'position_history': collections.deque(maxlen=5),
                'is_stable': False,
                'current_gesture': 'unknown',
                'finger_position': None
            }
        
        state = self.hand_states[hand_idx]
        
        # Detect current gesture
        gesture, finger_pos = self._detect_gesture(landmarks)
        state['current_gesture'] = gesture
        
        # Reset if fist detected
        if gesture == "fist":
            state.update({
                'smooth_x': None, 'smooth_y': None, 'smooth_size': None,
                'position_history': collections.deque(maxlen=5),
                'is_stable': False, 'finger_position': None
            })
            return
        
        # Calculate positions based on gesture
        if gesture.startswith("single_"):
            # Single finger gesture - use fingertip position
            if finger_pos:
                cx, cy = finger_pos
                cx_px, cy_px = int(cx * min_dim), int(cy * min_dim)
                state['finger_position'] = (cx_px, cy_px)
                
                # Use smaller effect size for single finger
                current_hand_size = self._calculate_hand_size(landmarks, frame_dims)
                size_ratio = current_hand_size / self.config['reference_hand_size']
                target_effect_size = int(self.config['finger_effect_size'] * size_ratio * self.config['finger_size_scale'])
                target_effect_size = max(40, min(150, target_effect_size))
            else:
                return
        else:
            # Open hand gesture - use palm center
            cx, cy, cz = self._calculate_palm_center(landmarks)
            cx_px, cy_px = int(cx * min_dim), int(cy * min_dim)
            state['finger_position'] = None
            
            # Use normal effect size for open hand
            current_hand_size = self._calculate_hand_size(landmarks, frame_dims)
            size_ratio = current_hand_size / self.config['reference_hand_size']
            target_effect_size = int(self.config['base_effect_size'] * size_ratio * self.config['hand_size_scale'])
            target_effect_size = max(self.config['min_effect_size'],
                                   min(self.config['max_effect_size'], target_effect_size))
        
        # Smooth the effect size
        if state['smooth_size'] is None:
            state['smooth_size'] = target_effect_size
        else:
            size_alpha = self.config['size_smoothing']
            state['smooth_size'] = int(size_alpha * target_effect_size + 
                                     (1 - size_alpha) * state['smooth_size'])
        
        # Smooth position updates
        if state['smooth_x'] is None:
            state['smooth_x'], state['smooth_y'] = cx_px, cy_px
            state['is_stable'] = True
        else:
            # Check for significant movement
            distance = math.sqrt((cx_px - state['smooth_x'])**2 + (cy_px - state['smooth_y'])**2)
            
            if distance > self.config['stability_threshold']:
                alpha = self.config['alpha']
                state['smooth_x'] = int(alpha * cx_px + (1 - alpha) * state['smooth_x'])
                state['smooth_y'] = int(alpha * cy_px + (1 - alpha) * state['smooth_y'])
                state['is_stable'] = True
        
        # Update position history
        if state['is_stable']:
            state['position_history'].append((state['smooth_x'], state['smooth_y']))
    
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a single frame with hand tracking and effects"""
        self.frame_count += 1
        
        # Prepare frame
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (960, 720))
        h, w = frame.shape[:2]
        min_dim = min(h, w)
        
        # Crop to square
        x_start, y_start = (w - min_dim) // 2, (h - min_dim) // 2
        frame_square = frame[y_start:y_start + min_dim, x_start:x_start + min_dim]
        
        # Process hands
        rgb = cv2.cvtColor(frame_square, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        
        if results.multi_hand_landmarks:
            # Clean up states for undetected hands
            detected_indices = set(range(len(results.multi_hand_landmarks)))
            for idx in list(self.hand_states.keys()):
                if idx not in detected_indices:
                    del self.hand_states[idx]
            
            # Process each detected hand
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                self._update_hand_state(hand_idx, hand_landmarks.landmark, (h, w))
                
                # Render effect if hand is stable
                state = self.hand_states[hand_idx]
                if (state['is_stable'] and state['smooth_x'] is not None and 
                    state['smooth_size'] is not None and "efek-api-unscreen" in self.effects):
                    
                    # Use the calculated hand size for effect size
                    effect_size = state['smooth_size']
                    
                    # Determine effect position based on gesture
                    if state['current_gesture'].startswith("single_") and state['finger_position']:
                        # Single finger - effect at fingertip
                        effect_x, effect_y = state['finger_position']
                        effect_y += -30  # Small offset above fingertip
                    else:
                        # Open hand - effect at palm center
                        effect_x = state['smooth_x']
                        effect_y = state['smooth_y'] + self.config['effect_y_offset']
                    
                    # Render effect
                    effect_frames = self.effects["efek-api-unscreen"]["frames"]
                    
                    self._overlay_effect_optimized(
                        frame_square,
                        effect_frames[state['frame_index']],
                        effect_x,
                        effect_y,
                        effect_size
                    )
                    
                    # Update animation frame
                    state['frame_index'] = (state['frame_index'] + 1) % len(effect_frames)
                    
                    # Debug visualization
                    if state['current_gesture'].startswith("single_") and state['finger_position']:
                        # Show fingertip position
                        cv2.circle(frame_square, state['finger_position'], 
                                 5, (255, 0, 255), -1)  # Magenta for fingertip
                    else:
                        # Show palm center
                        cv2.circle(frame_square, (state['smooth_x'], state['smooth_y']), 
                                 8, (0, 255, 255), -1)  # Cyan for palm
                    
                    # Debug text showing gesture and size
                    gesture_name = state['current_gesture'].replace('single_', '').title() if state['current_gesture'].startswith('single_') else 'Open Hand'
                    debug_text = f"Hand {hand_idx + 1}: {gesture_name} | Size={effect_size}"
                    cv2.putText(frame_square, debug_text, (10, 40 + 30 * hand_idx),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame_square
    
    def run(self):
        """Main execution loop"""
        cap = cv2.VideoCapture(0)
        
        # Optimize camera settings
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                processed_frame = self.process_frame(frame)
                cv2.imshow("Optimized Hand Effects", processed_frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == ord('q'):  # ESC or 'q' to quit
                    break
                    
        finally:
            cap.release()
            cv2.destroyAllWindows()

def main():
    """Main function to run the hand effect tracker"""
    tracker = HandEffectTracker()
    
    if not tracker.effects:
        print("No effects loaded. Please ensure 'effects' folder exists with GIF files.")
        return
    
    print("Starting hand effect tracker...")
    print("Press ESC or 'q' to quit")
    print("Gestures:")
    print("- Make a fist to reset hand tracking")
    print("- Show single finger for fingertip fire effect")
    print("- Open hand for palm fire effect")
    
    tracker.run()

if __name__ == "__main__":
    main()
