import cv2
import mediapipe as mp
import numpy as np
from gestures import check_sixseven_gesture, check_smile, check_tongue_out

mp_pose = mp.solutions.pose
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Configuration for windows
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 450
EMOJI_WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Load gif for six-seven gesture
cap2 = cv2.VideoCapture("sixseven.gif")
if not cap2.isOpened():
    print("Error: Could not open sixseven.gif.")
    exit()

# Load emoji images
try:
    smiling_emoji = cv2.imread("smile.jpg")
    straight_face_emoji = cv2.imread("plain.png")
    tongue_out_emoji = cv2.imread("tongue_out.jpeg")

    if smiling_emoji is None:
        raise FileNotFoundError("smile.jpg not found")
    if straight_face_emoji is None:
        raise FileNotFoundError("plain.png not found")
    if tongue_out_emoji is None:
        raise FileNotFoundError("tongue_out.jpeg not found")

    # Resize emojis
    smiling_emoji = cv2.resize(smiling_emoji, EMOJI_WINDOW_SIZE)
    straight_face_emoji = cv2.resize(straight_face_emoji, EMOJI_WINDOW_SIZE)
    tongue_out_emoji = cv2.resize(tongue_out_emoji, EMOJI_WINDOW_SIZE)

except Exception as e:
    print("Error loading emoji images!")
    print(f"Details: {e}")
    exit()

blank_emoji = np.zeros((EMOJI_WINDOW_SIZE[0], EMOJI_WINDOW_SIZE[1], 3), dtype=np.uint8)

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cv2.namedWindow('Emoji Output', cv2.WINDOW_NORMAL)
cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Camera Feed', WINDOW_WIDTH, WINDOW_HEIGHT)
cv2.resizeWindow('Emoji Output', WINDOW_WIDTH, WINDOW_HEIGHT)
cv2.moveWindow('Camera Feed', 250, 250)
cv2.moveWindow('Emoji Output', WINDOW_WIDTH + 150, 100)

print("Controls:")
print("  Press 'q' to quit")
print("  Smile for smiling emoji")
print("  Straight face for neutral emoji")
print("  Move hands up and down for six-seven gesture")
print("  Stick out your tongue for tongue out emoji")


with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
     mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh, \
     mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False

        current_state = "STRAIGHT_FACE"

        results_pose = pose.process(image_rgb)
        results_face = face_mesh.process(image_rgb)
        results_hands = hands.process(image_rgb)

        # Check six-seven gesture first
        if results_pose.pose_landmarks:
            if check_sixseven_gesture(results_pose.pose_landmarks.landmark):
                current_state = "SIX_SEVEN"
                print("Six-Seven gesture detected test 1")

        # Other wise check for facial expressions
        if current_state != "SIX_SEVEN":
            if results_face.multi_face_landmarks:

                if check_tongue_out(results_face):
                    current_state = "TONGUE_OUT"
                elif check_smile(results_face):
                    current_state = "SMILING"
                else:
                    current_state = "STRAIGHT_FACE"
        

        # Display appropriate emoji/gif
        if current_state == "SIX_SEVEN":
            print("Six Seven Gesture Detected test2!")
            ret, frame2 = cap2.read()
            if not ret:
                cap2.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame2 = cap2.read()
            emoji_to_display = cv2.resize(frame2, EMOJI_WINDOW_SIZE)
            emoji_name = "😏"

        elif current_state == "TONGUE_OUT":
            emoji_to_display = tongue_out_emoji
            emoji_name = "😛"

        elif current_state == "SMILING":
            emoji_to_display = smiling_emoji
            emoji_name = "😊"

        elif current_state == "STRAIGHT_FACE":
            emoji_to_display = straight_face_emoji
            emoji_name = "😐"


        else:
            emoji_to_display = blank_emoji
            emoji_name = "❓"

        camera_frame_resized = cv2.resize(frame, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        cv2.putText(camera_frame_resized, f'STATE: {current_state} {emoji_name}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(camera_frame_resized, 'Press "q" to quit', (10, WINDOW_HEIGHT - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
    
        cv2.imshow('Camera Feed', camera_frame_resized)
        cv2.imshow('Emoji Output', emoji_to_display)

        # Exit on 'q' key
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()