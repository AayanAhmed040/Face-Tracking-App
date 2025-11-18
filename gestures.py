import cv2
import mediapipe as mp
import numpy as np


mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Variables to track gesture state for six-seven gesture
hand_positions_history = []
MAX_HISTORY = 20 
alternating_count = 0
ALTERNATING_THRESHOLD = 2 
MIN_MOVEMENT = 0.02  

# Variables to track smiling
SMILE_THRESHOLD = 0.15

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
    
def check_smile(results_face):  # Add results_face as parameter
    global current_state  # Declare as global
    
    if results_face.multi_face_landmarks:
        for face_landmarks in results_face.multi_face_landmarks:
            left_corner = face_landmarks.landmark[291]
            right_corner = face_landmarks.landmark[61]
            upper_lip = face_landmarks.landmark[13]
            lower_lip = face_landmarks.landmark[14]

            mouth_width = ((right_corner.x - left_corner.x)**2 + (right_corner.y - left_corner.y)**2)**0.5
            mouth_height = ((lower_lip.x - upper_lip.x)**2 + (lower_lip.y - upper_lip.y)**2)**0.5

            if mouth_width > 0:
                mouth_aspect_ratio = mouth_height / mouth_width
                if mouth_aspect_ratio > SMILE_THRESHOLD:
                    current_state = "SMILING"
                    return True
    return False