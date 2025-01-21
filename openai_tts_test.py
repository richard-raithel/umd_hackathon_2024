from openai import OpenAI
from pathlib import Path

# Initialize OpenAI client
# client = OpenAI(api_key="")

def generate_tts_audio(text, voice='onyx'):
    # Define the path to save the audio file temporarily
    audio_file_path = Path("speech.mp3")  # Save in the current directory or update the path as necessary

    try:
        # Generate speech from text using OpenAI TTS API
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        # Save the response as an MP3 file
        response.stream_to_file(audio_file_path)
        print(f"Audio saved successfully at: {audio_file_path}")

    except Exception as e:
        # Handle errors and print the exception
        print(f"Error generating audio: {str(e)}")

# Test the function
generate_tts_audio('Zip it Gigi')
