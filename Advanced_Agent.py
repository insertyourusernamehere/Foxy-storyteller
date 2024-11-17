import random
import sys
import speech_recognition as sr
import threading
import os
sys.stdout = open(os.devnull, 'w')
from pygame import mixer  # for playing the audio
sys.stdout = sys.__stdout__
from time import sleep
from Input_Helper import get_speech_input, generate_story_metrics, get_location
from Validation import Api_init, get_travel_time
from speak import TTS
from groq import Groq
from datetime import datetime
from Emo import detect_emotion
import warnings

# Suppress pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Initialize the client with the API key
client = Groq(api_key=Api_init())

# Initialize global variables
story_length = 0
init_flag = True
total_words = 0  # Track total word count
target_length = 0  # Target word count for the story
conversation_history = []  # List to hold conversation history
user_query = "Repeat"

# Initialize speech recognition
recognizer = sr.Recognizer()
mixer.init()

# Global flags for stop, pause, and resume
stop_flag = False
pause_flag = False

# Function to listen for the stop command or pause/resume commands in a separate thread
def listen_for_commands():
    global stop_flag, pause_flag
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for commands... ('Hey Foxy End', 'Hey Foxy Stop', 'Hey Foxy Continue')")

        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                
                if "hey foxy end" in command.lower():
                    print("End command detected!")
                    stop_flag = True  # Flag to stop the audio and program
                    break
                
                if "hey foxy stop" in command.lower():
                    print("Stop command detected!")
                    pause_flag = True  # Flag to pause the audio
                    continue

                if "hey foxy continue" in command.lower():
                    print("Continue command detected!")
                    pause_flag = False  # Flag to resume the audio
                    continue

            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Error with speech recognition service")
                break

def set_emotions():
    emotions = {
        "Happy": "90.1",
        "Sadness": "5.5",
        "Anxious": "4.2",
        "Anger": "0.3"
    }

    emotion_str = ". The user is experiencing the following emotions: "
    for emotion, intensity in emotions.items():
        emotion_str += f"{emotion} at {intensity}%, "
    
    return emotion_str.strip(", ")

def get_story_length():
    # Logic to calculate story length based on ride length and words per minute
    global drive_length  # Assuming this is the duration of the ride in mins
    tts_speed = 150  # Words per minute
    global target_length
    target_length = drive_length * tts_speed  # Take minutes and multiply by speed
    return target_length

def chat_with_model():
    global init_flag, total_words, target_length, conversation_history, user_query, stop_flag, pause_flag


    while True:
        stop_flag = False  # Variable to monitor stop command
        pause_flag = False  # Variable to monitor pause/resume state
        # Reset for a new story
        if init_flag:
            # Reset word count and conversation history for a new story
            total_words = 0
            conversation_history = []
            
            # Calculate the target story length
            target_length = get_story_length()  # Target word count for the story
            print(f"Target story length: {target_length} words")

            # Initialize conversation history with a system message (to provide context)
            conversation_history.append({"role": "system", "content": "You are a storyteller helping the user create a story. Respond in narrative form."})

            # Get initial user input
            user_query = "Repeat"
            while user_query in ["Repeat", "Silence"]:  
                user_query = get_speech_input()
            # Ensure the user exits gracefully
            if user_query.lower() in ["exit", "quit", "bye", "Error 404"]:
                print("Ending chat. Goodbye!")
                break
            elif user_query == "stop":
                print("Stopping the program.")
                break

            # Append story metrics and emotions to the user query
            user_query += generate_story_metrics()
            print("Analyzing Emotions...")
            temp = detect_emotion()
            print(temp)
            user_query+= temp
            user_query += f". Tailor the story to match the following preferences, so as to make the user feel better after hearing the story. The story should be at least {target_length} words. If the story exceeds 1024 tokens or characters, break it into multiple parts. When I say 'Continue the story', provide the next part. Do not include any explanation, questions, or prompts asking if I want to continue. Simply provide the story, and nothing else, until I explicitly say 'Continue the story'. Avoid using phrases like 'Part 1', 'Part 2', or any other part indicators, as I am feeding the story to a text-to-speech agent and need the story alone."

            init_flag = False  # After the initial query, set flag to False

        else:
            user_query = "Continue the story."  # Trigger continuation
        
        # Add user query to the conversation history
        conversation_history.append({"role": "user", "content": user_query})
        print("Generating Story....")
        # Create a chat completion with the user's query and conversation history
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=conversation_history,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        # Get the model's response
        story_text = completion.choices[0].message.content
        print("Voicing Story....")
        
        # Convert the story to audio
        TTS(story_text)

        # Start listening for stop/pause/continue commands in a separate thread
        stop_thread = threading.Thread(target=listen_for_commands)
        stop_thread.start()

        # Play the MP3 file
        mixer.music.load("output.mp3")
        mixer.music.play()

        while mixer.music.get_busy():  # While audio is playing
            sleep(1)

            if stop_flag:  # Check if stop command was received
                mixer.music.stop()  # Stop the audio
                print("Stopping the story and exiting.")
                stop_thread.join()  # Make sure the thread ends gracefully
                init_flag = True
                break

            if pause_flag:  # Check if pause command was received
                mixer.music.pause()  # Pause the audio
                print("Audio paused")
                print("Listening for commands... ('Hey Foxy End', 'Hey Foxy Stop', 'Hey Foxy Continue')")

                
                while pause_flag:  # Wait until continue command is given
                    sleep(1)

                mixer.music.unpause()  # Resume the audio
                print("Audio resumed.")
                print("Listening for commands... ('Hey Foxy End', 'Hey Foxy Stop', 'Hey Foxy Continue')")


        # Ensure the file is no longer being used before deleting it
        while mixer.music.get_busy():  # Wait for music to finish playing
            sleep(0.1)

        mixer.quit()
        mixer.init()
        try:
            os.remove("output.mp3")
        except PermissionError:
            print("Error: Unable to delete output.mp3. File is still in use.")
        
        # Update total words count by counting words in the generated content
        total_words += len(story_text.split())

        # Add the model's response to the conversation history
        conversation_history.append({"role": "assistant", "content": story_text})

        # Check if the story has reached or exceeded the target length
        if total_words >= target_length:
            print("Story complete! Exceeded target word count.")
            init_flag = True  # Reset to allow new story input
            user_query = "Repeat"  # Reset user query to re-prompt for new input
            continue  # Loop back to ask if the user wants a new story

    # Final message to close the program
    print("Thank you for the interaction!")



def InitialD():
    # Get the current time
    current_time = datetime.now()
    current_hour = current_time.hour
    # Determine the time of day and load the corresponding music
    if 5 <= current_hour < 12:
        # Morning (5 AM to 12 PM)
        music_file = r"Audio/Morning.mp3"
    elif 12 <= current_hour < 18:
        # Evening (6 PM to 10 PM)
        music_file = r"Audio/Eve.mp3"
    else:
        # Night (10 PM to 5 AM)
        music_file = r"Audio/Night.mp3"

    # Load and play the selected music file
    mixer.music.load(music_file)
    mixer.music.play()
    while mixer.music.get_busy():
        pass
    # Quit the mixer after the music finishes playing
    mixer.quit()
    mixer.init()



# Call the function to play music based on the time of day
InitialD()
drive_length = get_travel_time()
chat_with_model()
