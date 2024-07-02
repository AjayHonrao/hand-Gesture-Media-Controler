from flask import Flask, render_template_string, redirect, url_for
import threading
import pyautogui
import cv2
import numpy as np
import keyboard
import mediapipe as mp
import time
from tensorflow.keras.models import load_model

# Initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model(r"trained_model.h5")

# Load class names
classNames = {
    0: "up",
    1: "right",
    2: "down",
    3: "left",
    4: "stop"
}

# Initialize the webcam
cap = cv2.VideoCapture(0)


app = Flask(__name__)

def background_process():
    while True:
        if keyboard.is_pressed('q'):
            break
        # Read each frame from the webcam
        _, frame = cap.read()

        x, y, _ = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)

        className = ''

        # Post-process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                flattened_input = np.array(landmarks).flatten()
                reshaped_input = flattened_input.reshape(1, -1)
                prediction = model.predict(reshaped_input)
                classID = np.argmax(prediction)
                confidence = prediction[0][classID]

                # Check confidence threshold
                if confidence > 0.9:
                    className = classNames[classID]
                    if className == "stop":
                        pyautogui.press('space')
                        time.sleep(3)
                    elif className == "up":
                        pyautogui.press('up')
                        time.sleep(0.5)
                    elif className == "down":
                        pyautogui.press('down')
                        time.sleep(0.5)
                    elif className == "right":
                        pyautogui.press('right')
                        time.sleep(0.5)
                    elif className == "left":
                        pyautogui.press('left')
                        time.sleep(0.5)
                    else:
                        pass
    # Release the webcam and destroy all active windows
    cap.release()
    cv2.destroyAllWindows()

@app.route('/')
def index():
    html_code = '''

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube and Facebook Buttons</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(180deg, #000346 0%, #FF0000 100%), linear-gradient(58.72deg, #0029FF 0%, #AA0014 100%), radial-gradient(100% 164.72% at 100% 100%, #FF00A8 0%, #00FF47 100%), radial-gradient(100% 148.07% at 0% 0%, #FFF500 0%, #51D500 100%);
            background-blend-mode: overlay, overlay, difference, normal;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            position: relative; /* Ensure relative positioning for absolute footer */
        }

        .container {
            background: radial-gradient(111% 111% at 74.29% -11%, #A93300 0%, #005570 100%), linear-gradient(127.43deg, #00D5C8 0%, #2200AA 100%);
            background-blend-mode: difference, normal; /* Background color with opacity */
            backdrop-filter: blur(10px); /* Apply blur effect */
            border-radius: 50px; /* Rounded corners */
            padding: 20px; /* Padding inside the container */
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 70px; /* Gap between child elements */
            width: 60%;
            height: 80%;
        }

        .buttons-container {
            display: flex;
            gap: 20px;
        }

        .start-button {
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            background-color: green;
            color: #D7DBDD;
            border: 2px solid #D7DBDD;
            border-radius: 10px;
            cursor: pointer;
            transition: background-color 0.3s ease; /* Smooth transition for background color change */
        }

        .start-button.processing {
            background-color: orange; /* Change color to orange when processing */
        }

        .button {
            width: 200px;
            height: 300px;
            color: black;
            border: 2px solid #D7DBDD;
            border-radius: 50px;
            padding: 10px;
            text-align: center;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-size: cover;
            background-position: center;
            overflow: hidden;
        }

        .button img,
        .button video {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
            border-radius: 50px;
        }

        .youtube-button {
            transition: transform 0.3s ease;
        }

        .facebook-button {
            transition: transform 0.3s ease;
        }

        .youtube-button:hover,
        .facebook-button:hover {
            transform: scale(1.1);
        }

        /* Tooltip style */
        .tooltip {
            position: absolute;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            pointer-events: none; /* Ensure tooltip doesn't interfere with button hover */
            opacity: 0; /* Initially hidden */
            transition: opacity 0.2s ease;
            top: -30px; /* Adjust position to be above the button */
            left: 50%; /* Center horizontally relative to button */
            transform: translateX(-50%); /* Center horizontally relative to button */
        }

        .youtube-button:hover .tooltip,
        .facebook-button:hover .tooltip {
            opacity: 1; /* Show tooltip on button hover */
        }

        /* Footer style */
        .footer {
            position: absolute;
            font-family: Times;
            bottom: 20px;
            color: white;
            font-size: 16px;
            width: 100%;
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container">
    <form id="start-form" action="/start" method="post">
        <button id="start-button" type="submit" class="start-button" aria-label="Start">Start</button>
    </form>
    <div class="buttons-container">
        <a href="https://www.youtube.com/" target="_blank" style="text-decoration: none;" aria-label="YouTube Link">
            <div class="button youtube-button">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/YouTube_social_white_square_%282017%29.svg/600px-YouTube_social_white_square_%282017%29.svg.png?20220808215424" alt="YouTube Logo">
                <video muted autoplay loop>
                    <source src="https://cdn.pixabay.com/video/2022/01/10/103984-664525664_large.mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <span class="tooltip">You are using YouTube</span>
            </div>
        </a>
        <a href="https://www.facebook.com/" target="_blank" style="text-decoration: none;" aria-label="Facebook Link">
            <div class="button facebook-button">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIZ2sahgGo2tBLEr1w8vWCBGQJ_HohDqIteQ&s" alt="Facebook Logo">
                <video muted autoplay loop>
                    <source src="https://www.shutterstock.com/shutterstock/videos/1106305857/preview/stock-footage-kiev-ukraine-july-animation-of-appearing-and-disappearing-d-icon-facebook-for-social.webm" type="video/webm">
                    Your browser does not support the video tag.
                </video>
                <span class="tooltip">You are using Facebook</span>
            </div>
        </a>
    </div>
</div>

<footer class="footer">Press Q for stop..</footer>

<script>
    const startButton = document.getElementById('start-button');
    const startForm = document.getElementById('start-form');

    startForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission
        startButton.classList.add('processing'); // Add 'processing' class to start button
        startButton.textContent = 'Processing...'; // Change button text to indicate processing

        // Simulate processing time (e.g., 3 seconds)
        setTimeout(function() {
            startForm.submit(); // Actually submit the form after processing
        }, 3000);
    });
</script>
</body>
</html>


    '''
    return render_template_string(html_code)

@app.route('/start', methods=['POST'])
def start():
    # Start the background process in a new thread
    thread = threading.Thread(target=background_process)
    thread.start()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
