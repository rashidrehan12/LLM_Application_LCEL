import requests
import streamlit as st
from gtts import gTTS
from io import BytesIO

def get_groq_response(input_text, language):
    """
    Make a POST request to the API and get the response in the specified language.

    Args:
        input_text (str): The text to be sent to the API.
        language (str): The language to convert the text to ('French', 'Hindi', etc.).

    Returns:
        str: The output text from the API.
    """
    # Create the JSON payload with the input text and specified language
    json_body = {
        "input": {
            "language": language,
            "text": input_text  # Use the provided input_text
        },
        "config": {},
        "kwargs": {}
    }

    try:
        # Make the POST request with the proper JSON payload
        response = requests.post("http://127.0.0.1:8000/chain/invoke", json=json_body)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        response_json = response.json()
        
        # Extract the output text from the response
        output = response_json.get("output", "no output found")

        return output
    except requests.exceptions.RequestException as e:
        # Handle exceptions
        st.error(f"An error occurred: {e}")
        return "Error occurred while fetching response."

def text_to_speech(text, language):
    """
    Convert text to speech using gTTS and return an audio file.

    Args:
        text (str): The text to be converted to speech.
        language (str): The language code for gTTS (e.g., 'hi' for Hindi, 'fr' for French).

    Returns:
        BytesIO: In-memory audio file in MP3 format.
    """
    # Convert the text to speech using gTTS
    tts = gTTS(text, lang=language)  # Set the language for TTS
    audio_file = BytesIO()  # Create an in-memory file-like object
    tts.write_to_fp(audio_file)  # Write the speech data to the BytesIO object
    audio_file.seek(0)  # Reset the file pointer to the beginning of the file
    return audio_file

## Streamlit app
st.title("Translate Text to Different Language")

# Dropdown menu for language selection
language = st.selectbox(
    "Select the language to convert your text to",
    ["French", "Hindi", "Spanish", "German", "Italian", "Portuguese", "Dutch", "Russian", "Arabic", "Urdu"]  # Add more languages if needed
)

# Map language names to language codes for gTTS
language_codes = {
   "French": "fr",
    "Hindi": "hi",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Dutch": "nl",
    "Russian": "ru",
    "Arabic": "ar",
    "Urdu": "ur"
}

# Input text
input_text = st.text_input("Enter the text you want to convert")

if input_text:
    # Get the response from the API in the selected language
    response = get_groq_response(input_text, language=language)
    
    st.subheader("Output")
    st.write(response)  # Display the output text

    # Convert the output to speech and play it
    if response and response != "no output found" and response != "Error occurred while fetching response.":
        lang_code = language_codes.get(language, 'en')  # Default to English if not found
        audio_file = text_to_speech(response, language=lang_code)  # Convert the text output to speech
        st.audio(audio_file, format='audio/mp3')  # Play the audio in Streamlit