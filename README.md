# Hand-Gesture-Recognition-System

The Hand Gesture Recognition System project is designed to allow users to interact with their computer using hand gestures. The system utilizes a webcam to capture hand gestures and interprets them to control various functions, such as navigating through videos or controlling applications without touching the computer.

## Features
- Real-time hand gesture recognition using a webcam.
- Controls for five gestures: up, down, left, right, and stop.
- Webpage interface for easy demonstration and usage.

## Dataset Description
- **Classes**: Up, Down, Left, Right, Stop
- **Total Images**: 10,000
- **Format**: Images converted to arrays for training purposes.

## System Requirements
- Python 3.x
- Flask
- OpenCV
- MediaPipe
- TensorFlow
- PyAutoGUI
- Keyboard

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/hand-gesture-recognition-system.git
    cd hand-gesture-recognition-system
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Download the trained model and place it in the project directory.

## Usage
1. Start the Flask server:
    ```bash
    python app.py
    ```
2. Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).
3. Click the Start button to begin the hand gesture recognition system.

## Development/Deployment
- **Model Training**: The model was trained manually by converting all image data into arrays and using a neural network for classification. The custom dataset consists of 10,000 images representing five gesture classes.
- **Webpage**: A simple webpage is created for demonstration purposes, where users can choose to open YouTube or other supported services. Upon clicking the Start button, the hand gesture recognition system is activated.

## Expected Outcomes
- Touch-free interaction with computers.
- Increased accessibility for users with physical disabilities.
- Improved user experience with gesture-based controls.
- Real-time processing and high accuracy in gesture recognition.
- Practical applications in various domains such as entertainment and smart homes.

## Future Scope
- Expand the gesture set to include more commands.
- Optimize the system for better performance and accuracy.
- Develop mobile applications to extend the functionality to smartphones and tablets.
- Integrate with more web services and applications.

## Conclusion
The Hand Gesture Recognition System demonstrates the potential of using computer vision and machine learning to create innovative and user-friendly interaction methods. The system is a step towards more natural and intuitive ways to interact with technology, providing a foundation for future advancements in gesture-based controls.

## Limitations
- Continuous use of the webcam can lead to high battery consumption.
- Limited to predefined gestures and commands.
- Environmental factors such as lighting can affect accuracy.

## Contribution
- **Ajay Manohar Honrao** (ajayhonrao12@gmail.com) - Developer
- **Karan Gorakh Yeole** (karanyeole2712@gmail.com) - Developer

## License
This project is licensed under the MIT License.

## Contact
For any inquiries or suggestions, please contact **Karan Gorakh Yeole** at [karanyeole2712@gmail.com](mailto:karanyeole2712@gmail.com).
