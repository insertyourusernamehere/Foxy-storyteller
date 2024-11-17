import cv2
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from deepface import DeepFace
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging

# Suppress TensorFlow logs
logging.getLogger('tensorflow').setLevel(logging.CRITICAL)
import tensorflow as tf
import time



def detect_emotion():
    # Suppress TensorFlow deprecation warnings
    tf.get_logger().setLevel('ERROR')
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Start capturing video from the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        exit()

    # Variables to track emotion percentages
    emotion_data = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
    frame_count = 0
    age_sum = 0  # Sum of detected ages for calculating the average
    detected_faces = 0  # Counter for valid face detections
    start_time = time.time()

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Check if the frame is read correctly
        if not ret or frame is None:
            print("Error: Failed to capture frame.")
            break

        # Ensure the frame is a valid numpy array
        if not isinstance(frame, (list, tuple)) and len(frame.shape) == 3:
            try:
                # Analyze the frame for emotions and age
                analysis = DeepFace.analyze(
                    frame,
                    actions=['emotion', 'age'],
                    enforce_detection=False,
                    detector_backend='retinaface',silent=True
                )
            except Exception as e:
                print(f"Error in DeepFace analysis: {e}")
                continue

            for face in analysis:
                # Extract emotion percentages
                emotion_percentages = face['emotion']

                # Update the emotion data
                for emotion, percentage in emotion_percentages.items():
                    emotion_data[emotion] += percentage

                # Extract age and add to the cumulative sum
                if 'age' in face:
                    age_sum += face['age']
                    detected_faces += 1

            # Increment the frame count
            frame_count += 1

        # Check if 8 seconds have passed
        if time.time() - start_time > 8:
            # Calculate the average emotion percentages
            avg_emotion_percentages = {emotion: (percentage / frame_count) for emotion, percentage in emotion_data.items()}

            # Calculate average age
            avg_age = age_sum / detected_faces if detected_faces > 0 else None

            # Construct the output string
            output_string = "The user's emotions are: "
            for emotion, avg_percentage in avg_emotion_percentages.items():
                output_string += f"{avg_percentage:.2f}% {emotion}, "

            # Include age information in the output string
            if avg_age is not None:
                output_string += f" and the estimated average age is {avg_age:.2f} years."
            else:
                output_string += " but the age could not be reliably estimated."

            # Print the output string
            return output_string

