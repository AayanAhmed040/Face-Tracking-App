# Face-Tracking-App

An appplication which tracks faces using the device camera and displays emotes based on facial expressions or hand gestures.

## About this project
This project uses computer vision techniques to detect facial landmarks and hand gestures in real-time using the device camera. Based on the detected expressions or gestures, it displays preselected corresponding emotes on the screen.

The app is built using python and leverages libraries such as OpenCV for computer vision tasks and MediaPipe for facial and hand landmark detection.

## Features
- Real-time movement and face tracking using device camera.
- Detection of facial expressions for smiling or blank expression.
- Detection of hand gestures, for the 'six seven' meme gesture.


## Attribution
### Credits & Inspiration
- This project was inspired by emoji-reactor created by [Aaronhubhachen](https://github.com/aaronhubhachen/emoji-reactor)

- Core logic for landmark detection for facial expressions adapted from his implementation.

- Refactored Aayan Ahmed to improve code structure and add hand gesture recognition for the popular meme 'six seven'.

## Setup & Installation

### 1. Prerequisites
- Python 3.12.2 or lower

### 2. Clone the Repository
1. Clone this repository:
   ```bash
   git clone [https://github.com/AayanAhmed040/Face-Tracking-App.git](https://github.com/AayanAhmed040/Face-Tracking-App.git)

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
4. Make a blank expression to see the blank emote.
5. Move your hands up and down alternatively to perform the 'six seven' gesture and see the 6-7 emote.

## Future Improvements
- Add more facial expressions and corresponding emotes.
- Improve gesture recognition accuracy.
- Clean up code and add more comments/ documentation.