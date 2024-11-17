import speech_recognition as sr
import random
recognizer = sr.Recognizer()

def get_speech_input():
    with sr.Microphone() as source:
        print("Listening... (say 'Hey Foxy' to begin)")

        try:
            # Listen for user input with a timeout for silence
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=20)

            # Convert audio to text
            user_query = recognizer.recognize_google(audio)
            print("You said:", user_query)

            # Check if input starts with "Hey Wizard"
            if "hey foxy" in user_query.lower():
                parsed_query=user_query[user_query.lower().find("hey foxy")+9::]
                # Extract valid input after "Hey Wizard"
        
                if parsed_query:  # Ensure there's something meaningful after "Hey Wizard"
                    return parsed_query
                else:
                    return "Silence"  # Return "Silence" if there's nothing after "Hey Wizard"
            else:
                return "Silence"  # Return "Silence" for irrelevant input
        except sr.WaitTimeoutError:
            # No speech detected within the timeout period
            return "Silence"
        except sr.UnknownValueError:
            # Speech was detected but not understood
            return "Silence"
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return "Error 404"


def generate_story_metrics():
    metrics = [
        "Craziness",
        "Intensity",
        "Emotional Depth",
        "Character Development",
        "Worldbuilding",
        "Mystery",
        "Romantic Element",
        "Humor",
        "Violence",
        "Plot Complexity"
    ]

    prompt = {metric: random.randint(0, 100) for metric in metrics}
    metrics_str = "The following story metrics should guide the narrative: "
    for metric, value in prompt.items():
        metrics_str += f"{metric} at {value}%, "

    return metrics_str.strip(", ") + "."

def get_location():
    with sr.Microphone() as source:
        print("Hello Where are we off to Today? ")

        audio = recognizer.listen(source, timeout=20, phrase_time_limit=20)

        try:
            user_query = recognizer.recognize_google(audio)
            print("You said:", user_query)

            return(user_query)
        
        except sr.UnknownValueError:
            # Speech was detected but not understood
            return "Silence"
        


