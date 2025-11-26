import cv2
import mediapipe as mp
import numpy as np


mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# six-seven variables
hand_positions_history = []
MAX_HISTORY = 20 
alternating_count = 0
ALTERNATING_THRESHOLD = 2 
MIN_MOVEMENT = 0.02  

# Variables to track smiling
SMILE_THRESHOLD = 0.15

# Variables to track tongue out
TONGUE_OUT_THRESHOLD = 0.25

# Wave variables
wave_history_right = []
wave_history_left = []
WAVE_HISTORY_MAX = 15
WAVE_MIN_MOVEMENT = 2
WAVE_MOVE_THRESHOLD = 0.02

# global variables we need to modify or access
current_state = None  # Initialize with a default value

def check_sixseven_gesture(pose_landmarks):
    """
    Detects six-seven gesture by looking for alternating wrist heights.
    """
    global hand_positions_history, alternating_count  # Declare as global
        
    try:
        # Checking if wrists are visible 
        left_wrist = pose_landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pose_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_shoulder = pose_landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = pose_landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        if not (left_wrist.visibility > 0.3 and right_wrist.visibility > 0.3):
            hand_positions_history = []
            alternating_count = 0
            return False

        # Ensure hands are in correct position
        hands_in_front = (left_wrist.y < left_shoulder.y + 0.3 and 
                         right_wrist.y < right_shoulder.y + 0.3)
        
        if not hands_in_front:
            hand_positions_history = []
            alternating_count = 0
            return False
        
        # Calculate height difference
        height_diff = abs(left_wrist.y - right_wrist.y)
        if height_diff < MIN_MOVEMENT:
            # Only work if there is enough movement
            return len(hand_positions_history) >= 4 and alternating_count >= ALTERNATING_THRESHOLD
        
        # Determine which hand is higher
        left_higher = left_wrist.y < right_wrist.y - MIN_MOVEMENT
        hand_positions_history.append(left_higher)
        if len(hand_positions_history) > MAX_HISTORY:
            hand_positions_history.pop(0)

        if len(hand_positions_history) < 4:
            return False
        
        alternations = 0
        for i in range(1, len(hand_positions_history)):
            if hand_positions_history[i] != hand_positions_history[i-1]:
                alternations += 1
        
        alternating_count = alternations
        
        # Debug output
        # print(f"Hand Alternations: {alternations}/{ALTERNATING_THRESHOLD}, History: {len(hand_positions_history)}, Diff: {height_diff:.3f}")
        
        # Run if all conditions are met
        return alternations >= ALTERNATING_THRESHOLD
            
    except Exception as e:
        print(f"Error in gesture detection: {e}")
        hand_positions_history = []
        alternating_count = 0
        return False
    
# More logic so we can check for both left and right
def process_waving(wrist, history):
    """
    Process wrist movement for waving detection.
    """
    if wrist.visibility < 0.3:
        history.clear()
        return False
    history.append(wrist.x)

    if len(history) > WAVE_HISTORY_MAX:
        history.pop(0)

    if len(history) < 5:
        return False
    
    # Chedcking for movement in x
    # 1 for right, -1 for left
    moves = []
    for i in range(1, len(history)):
        difference = history[i] - history[i-1]
        if abs(difference) > WAVE_MOVE_THRESHOLD:
            if difference > 0:
                moves.append(1) 
            else:
                moves.append(-1)
            
    wiggle = 0
    for i in range(1, len(moves)):
        if moves[i] != moves[i-1]:
            wiggle += 1
    return wiggle >= WAVE_MIN_MOVEMENT


def check_waving(pose_landmarks):
    """
    Detects waving gesture by looking for hand movements.
    """
    global wave_history_left, wave_history_right
    try:
        left_wrist = pose_landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pose_landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

        left_wave = process_waving(left_wrist, wave_history_left)
        right_wave = process_waving(right_wrist, wave_history_right)
        return left_wave or right_wave
    
    except Exception as e:
        print(f"Error in waving {e}")
        wave_history_left.clear()
        wave_history_right.clear()
        return False

def get_mouth_dims(face_landmarks):
    """Helper to get mouth width and height."""
    left_corner = face_landmarks.landmark[61]
    right_corner = face_landmarks.landmark[291]
    upper_lip = face_landmarks.landmark[13]
    lower_lip = face_landmarks.landmark[14]

    width = ((right_corner.x - left_corner.x)**2 + (right_corner.y - left_corner.y)**2)**0.5
    height = ((lower_lip.x - upper_lip.x)**2 + (lower_lip.y - upper_lip.y)**2)**0.5
    return width, height, left_corner, right_corner, upper_lip, lower_lip

def check_tongue_out(results_face):
    """
    Detects if the mouth is open vertically significantly (proxy for tongue out).
    """
    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            width, height, _, _, _, _ = get_mouth_dims(face_landmarks)

            if width > 0:
                # Ratio: Height over Width. High value = mouth open vertically.
                aspect_ratio = height / width
                if aspect_ratio > TONGUE_OUT_THRESHOLD:
                    return True
    return False

def check_smile(results_face):  
    """
    Detects smiling by analyzing mouth aspect ratio.
    """
    global current_state  
    
    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            mouth_width, mouth_height, _, _, _, _ = get_mouth_dims(face_landmarks)

            if mouth_width > 0:
                mouth_aspect_ratio = mouth_height / mouth_width
                if mouth_aspect_ratio > SMILE_THRESHOLD and mouth_aspect_ratio < TONGUE_OUT_THRESHOLD:
                    # current_state = "SMILING"
                    return True
    return False