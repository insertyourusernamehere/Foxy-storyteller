from groq import Groq
import random
import speech_recognition as sr
from Input_Helper import get_speech_input, generate_story_metrics
from Validation import Api_init
# Initialize the client with the API key
client = Groq(api_key=Api_init())

# Initialize global variables
story_length = 0
init_flag = True
total_words = 0  # Track total word count
target_length = 0  # Target word count for the story
conversation_history = []  # List to hold conversation history
user_query = "Repeat"


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
    drive_length = 8  # Assuming this is the duration of the ride in mins
    tts_speed = 150  # Words per minute
    global target_length
    target_length = drive_length * tts_speed  # Take minutes and multiply by speed
    return target_length

def chat_with_model():
    global init_flag, total_words, target_length, conversation_history, user_query

    while True:
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
            user_query += set_emotions()

            user_query += f". Tailor the story to match the following preferences. The story should be at least {target_length} words. If the story exceeds 1024 tokens or characters, break it into multiple parts. When I say 'Continue the story', provide the next part. Do not include any explanation, questions, or prompts asking if I want to continue. Simply provide the story, and nothing else, until I explicitly say 'Continue the story'. Avoid using phrases like 'Part 1', 'Part 2', or any other part indicators, as I am feeding the story to a text-to-speech agent and need the story alone."

            init_flag = False  # After the initial query, set flag to False

        else:
            user_query = "Continue the story."  # Trigger continuation
        
        # Add user query to the conversation history
        conversation_history.append({"role": "user", "content": user_query})

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
        print(story_text)

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

# Start the chat
chat_with_model()
