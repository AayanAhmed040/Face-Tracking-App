# Face-Tracking-App

An application which tracks faces using the device camera and displays emotes based on facial expressions or hand gestures.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Numpy](https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white)

## About this project
This project uses computer vision techniques to detect facial landmarks and hand gestures in real-time using the device camera. Based on the detected expressions or gestures, it displays preselected corresponding emotes on the screen.

The app is built using python and leverages libraries such as OpenCV for computer vision tasks and MediaPipe for facial and hand landmark detection.

## Features
- Real-time movement and face tracking using device camera.
- Detection of facial expressions for smiling, sticking out tongue, and blank expression.
- Detection of hand gestures, for the 'six seven' meme gesture, and waving.


## Attribution
### Credits & Inspiration
- This project was inspired by emoji-reactor created by [Aaronhubhachen](https://github.com/aaronhubhachen/emoji-reactor)

- Core logic for landmark detection for facial expressions adapted from his implementation.

- Refactored by Aayan Ahmed to improve code structure and add hand gesture recognition for the popular meme 'six seven'.

## Setup & Installation

### 1. Prerequisites
- Python 3.9 to 3.12.2 installed on your system.
   - *Note:* Some libraries may not be compatible with Python versions above 3.12.2.
- pip (Python package installer)
- A device with a functional camera

### 2. Clone the Repository
1. Clone this repository:
   ```bash
   git clone https://github.com/AayanAhmed040/Face-Tracking-App.git

   cd Face-Tracking-App
   ```

2. Intall the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

    Windows:
    ```bash
    python main.py
    ```
    MacOS or Linux:
    ```bash
    python3 main.py
    ```

## How to use
1. Ensure your device has a functional camera. 
   * Grant camera access permissions if prompted.
2. Once the two windows open, position your face and hands within the camera frame.
3. Make a smiling expression to see the smile emote.
4. Stick out your tongue to see the tongue out emote.
5. Make a blank expression to see the blank emote.
6. Move your hands up and down alternatively to perform the 'six seven' gesture and see the 6-7 emote.
7. Wave your hand to see the wave emote.
8. Press 'q' to exit the application.

## History
- **v1.0.0** - Initial release with facial expression detection for smiling, blank expression, and six-seven hand gesture. (2025-11-17)
- **v1.1.0** - Added tongue out facial expression detection and corresponding emote. (2025-11-24)

## Future Improvements
- Add more facial expressions and corresponding emotes.
- Improve gesture recognition accuracy.
- Create better logic for toungue out detection.
- Clean up code and add more comments/ documentation.