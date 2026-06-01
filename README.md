A simple real-time *Hand Gesture Detection System* built using *Python, OpenCV, and MediaPipe*.

This project detects hand landmarks through a webcam and recognizes basic gestures like:

- ✊ Fist
- 👍 Thumbs Up
- ☝️ Pointing
- ✌️ Peace Sign
- 🖐️ Palm/Open Hand
- Finger Counting

The system also displays real-time FPS for smooth performance monitoring.

---

## 🚀 Features

- Real-time hand tracking using webcam
- Gesture recognition using hand landmarks
- Finger counting functionality
- FPS (Frames Per Second) display
- Simple and beginner-friendly implementation
- Uses MediaPipe for accurate hand detection

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe

✨ Detected Gestures
Gesture	Description
✊ Fist	No fingers detected
👍 Thumbs Up	Only thumb detected
☝️ Pointing	Only index finger up
✌️ Peace	Index + middle finger
🖐️ Palm	All fingers open
🔢 Finger Count	Shows total fingers

📸 How It Works
Captures video from webcam
MediaPipe detects hand landmarks
Finger positions are analyzed
Gesture rules determine the hand sign
Result is displayed live on screen

🧠 Future Improvements
Add custom gesture training
Support multiple hands
Gesture-based system controls
Add GUI interface
Improve gesture accuracy

🙌 Acknowledgements
OpenCV
Google MediaPipe
