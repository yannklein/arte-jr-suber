import os, json
import whisper

from modules.time_util import ftime


def audio_to_text():
    print(f"{ftime()}: Starting transcript creation...")
    # Specify the directories
    transcript_file = f"{os.environ.get('VIDEOS_FOLDER')}/transcript.json"

    # Load the whisper model
    model = whisper.load_model("medium")
    
    # Transcribe the audio file
    input_audio = f"{os.environ.get('VIDEOS_FOLDER')}/original.mp3"
    result = model.transcribe(input_audio)
    
    json_object = json.dumps(result, indent=4)

    # Write the transcription to the output file
    with open(transcript_file, 'w') as f:
        f.write(json_object)
    
    print(f"{ftime()}: Transcript creation done!")
    pass