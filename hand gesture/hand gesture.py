# hand_gesture.py
# Simple real-time hand gesture detector using MediaPipe + OpenCV
# Run: python hand_gesture.py
# Press 'q' to quit.

import cv2
import mediapipe as mp
import time

# ---- Setup ----
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Hands model: tuned for webcam realtime
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# helper: finger tip and pip landmark indices
TIP_IDS = [4, 8, 12, 16, 20]     # thumb, index, middle, ring, pinky
PIP_IDS = [3, 6, 10, 14, 18]     # approximate "lower joint" for thumb and fingers

prev_time = 0

def detect_gesture(landmarks, handedness_label):
    """
    landmarks: list of mediapipe landmark objects (normalized)
    handedness_label: 'Left' or 'Right' from MediaPipe (useful for thumb logic)
    Returns: string gesture name and finger_status list
    """
    finger_status = []  # 1 = up/extended, 0 = down
    # For index, middle, ring, pinky: check if tip.y < pip.y (smaller y -> higher on image => extended)
    for tip_id, pip_id in zip(TIP_IDS[1:], PIP_IDS[1:]):  # skip thumb for this loop
        if landmarks[tip_id].y < landmarks[pip_id].y:
            finger_status.append(1)
        else:
            finger_status.append(0)

    # Simple thumb check:
    # We'll check if thumb tip is to the left/right of its lower joint depending on handedness,
    # and also allow vertical check (tip.y < pip.y) as a "thumb up" indicator.
    thumb_is_open = False
    # Horizontal test (works for many typical camera setups)
    if handedness_label == "Right":
        if landmarks[TIP_IDS[0]].x > landmarks[PIP_IDS[0]].x:
            thumb_is_open = True
    else:  # Left hand
        if landmarks[TIP_IDS[0]].x < landmarks[PIP_IDS[0]].x:
            thumb_is_open = True
    # Vertical thumb-up test (for thumbs-up gesture)
    thumb_up_vertical = landmarks[TIP_IDS[0]].y < landmarks[PIP_IDS[0]].y

    # Combine info
    total_fingers = sum(finger_status) + (1 if thumb_is_open else 0)

    # Gesture rules (simple & explainable)
    # - Fist: no fingers extended
    # - Thumbs Up: only thumb up (others down), or thumb up vertical + others down
    # - Pointing: only index up
    # - Peace: index + middle up
    # - Palm: all 4 fingers up + thumb open-ish
    gesture = "Unknown"
    if sum(finger_status) == 0 and not thumb_is_open:
        gesture = "Fist"
    elif sum(finger_status) == 0 and (thumb_up_vertical or thumb_is_open):
        gesture = "Thumbs Up"
    elif finger_status == [1, 0, 0, 0]:  # index only
        gesture = "Pointing (1)"
    elif finger_status[:2] == [1, 1] and finger_status[2:] == [0, 0]:
        gesture = "Peace (2)"
    elif sum(finger_status) == 4 and thumb_is_open:
        gesture = "Palm (5)"
    else:
        gesture = f"{total_fingers} fingers"

    return gesture, [ (TIP_IDS[i+1], state) for i,state in enumerate(finger_status) ], thumb_is_open

# ---- Main loop ----
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Flip for mirror view (so it feels like a mirror)
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    h, w, _ = frame.shape
    gesture_text = "No hand"

    if results.multi_hand_landmarks:
        # Use first detected hand
        hand_landmarks = results.multi_hand_landmarks[0]
        # Get handedness label (Left/Right)
        handedness = "Unknown"
        if results.multi_handedness:
            handedness = results.multi_handedness[0].classification[0].label

        # Draw landmarks
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Detect gesture
        gesture_text, finger_details, thumb_open = detect_gesture(hand_landmarks.landmark, handedness)

        # Optionally show finger tip coordinates (for debugging)
        for i, lm in enumerate(hand_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            # draw small circle on tip points for visibility
            if i in TIP_IDS:
                cv2.circle(frame, (cx, cy), 6, (255, 0, 0), cv2.FILLED)

    # FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time

    # Overlay text
    cv2.putText(frame, f"Gesture: {gesture_text}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Hand Gesture Detection", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
