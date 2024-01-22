import os, json
import whisper

def audio_to_text(input_audio):

    # Specify the directories
    transcript_file = "./videos/transcript.json"

    print(transcript_file, input_audio)
    # Load the whisper model
    model = whisper.load_model("medium")
    
    # Transcribe the audio file
    result = model.transcribe(input_audio)
    # print(result)
    
    json_object = json.dumps(result, indent=4)

    # Write the transcription to the output file
    with open(transcript_file, 'w') as f:
        f.write(json_object)
    
    return transcript_file