import os, json
import whisper

from modules.time_util import ftime
from openai import OpenAI


def audio_to_text_via_api():
    print(f"{ftime()}: Starting transcript creation...")
    # Specify the directories
    transcript_file = f"{os.environ.get('VIDEOS_FOLDER')}/transcript.json"

    # Load the whisper client
    client = OpenAI()
    
    # Transcribe the audio file
    input_audio = f"{os.environ.get('VIDEOS_FOLDER')}/original.mp3"
    
    try:
        audio_file= open(input_audio, "rb")
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
        result = dict(transcription)
    except Exception as e:  
        print(f"{ftime()}: Can't do transcription... {e}")
    print(f"{ftime()}: Got transcription...")
    
    json_object = json.dumps(result, indent=4)
    print(f"{ftime()}: Ready to write in file...")

    # Write the transcription to the output file
    with open(transcript_file, 'w') as f:
        f.write(json_object)
    
    print(f"{ftime()}: Transcript creation done! Check it out: {transcript_file}")
    pass