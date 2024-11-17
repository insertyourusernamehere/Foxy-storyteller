
# Foxy: Personalized Storytelling Agent

**Foxy** is an intelligent, personalized storytelling agent designed to provide engaging, immersive narratives tailored to the user's emotional state, journey duration, and other unique preferences. By leveraging state-of-the-art AI technologies, Foxy provides a dynamic storytelling experience and seamless voice-based interaction.

## Features

1. **Dynamic Storytelling**:
   - Generates personalized stories using an 11-billion parameter language model.
   - Dynamically calculates the length of your journey using the Google Maps API and creates a story perfectly matched to that duration.

2. **Emotion Detection**:
   - Utilizes DeepFace and RetinaFace to analyze emotions such as happiness, sadness, anger, and anxiety.
   - Adapts story content to improve the user’s mood and match emotional preferences.

3. **Interactive Voice Interface**:
   - Recognizes speech commands using Google Speech Recognition.
   - Narrates stories using Google Text-to-Speech (TTS) for a natural, engaging experience.

4. **Pause, Resume, and Stop Functionality**:
   - Responds to commands like "Hey Foxy Stop", "Hey Foxy Continue", and "Hey Foxy End" for complete control over narration.

5. **Time-Based Custom Voice Lines**:
   - Plays specific audio tracks based on the time of day (morning, evening, or night) to set the perfect mood for storytelling.

6. **Real-Time Interaction**:
   - Captures live user input and adapts story progression dynamically, ensuring a unique experience every time.

## Setup Guide

### Requirements
- **Python Version**: Foxy runs on Python 3.10.11. Using other versions may cause errors due to dependencies.
- **Dependencies**: Foxy relies on a variety of modules, which are listed in the `requirements.txt` file.

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/insertyourusernamehere/Foxy-storyteller
   cd foxy
   ```

2. **Install Dependencies**:
   Install all necessary Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file in the project root directory.
   - Add your API credentials as shown below:
     ```env
     GROQ_API_KEY=your_groq_api_key
     GMAP_KEY=your_google_maps_api_key
     ```

4. **Configure Google Cloud**:
   - Place the Google Cloud service account file (`demo_service_acc.json`) in the project directory.
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="demo_service_acc.json"
     ```

5. **Run the Program**:
   Launch the storytelling agent:
   ```bash
   python Advanced_Agent.py
   ```

### First-Time Setup
- During the first run, Foxy may need to download several AI models required for its features. This process may take some time, so please be patient.

## Usage

### Interacting with Foxy
- **Start Interaction**:
  Say "Hey Foxy" followed by your input to begin the conversation.
- **Voice Commands**:
  - "Hey Foxy Stop" - Pause the narration.
  - "Hey Foxy Continue" - Resume the narration.
  - "Hey Foxy End" - End the session.

### How It Works
- **Journey-Based Stories**:
  Foxy uses the Google Maps API to calculate your journey duration and generates a story tailored to that time frame.
- **Emotion-Aware Narratives**:
  By analyzing user emotions in real-time, Foxy adapts the story to enhance engagement and improve the user’s mood.

## Notes

1. **Performance**:
   - Input processing may be slower on lower-end systems due to the computational demands of running multiple AI models in the background.

2. **Audio Files**:
   - Ensure all required audio files (e.g., `Morning.mp3`, `Eve.mp3`, `Night.mp3`) are correctly placed in the `Audio/` folder.

3. **Webcam Access**:
   - Emotion detection requires an active webcam. Ensure your webcam is properly configured and accessible.

## Features Overview

| Feature                 | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| **Dynamic Storytelling** | Creates engaging stories customized for your journey and emotions.         |
| **Emotion Detection**    | Adapts storytelling based on emotional analysis using DeepFace and RetinaFace. |
| **Voice Control**        | Interactive voice commands for pausing, resuming, and stopping the narration. |
| **Journey Awareness**    | Calculates trip duration dynamically with Google Maps API.                 |
| **Time-Based Audio**     | Plays customized tracks for morning, evening, and night.                   |

## Contribution

We welcome contributions to improve Foxy! Feel free to submit issues or pull requests to enhance the project.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
