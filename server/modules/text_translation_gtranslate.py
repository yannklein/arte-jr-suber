import json, urllib.request, datetime, os
from google.cloud import translate_v2 as translate
from modules.time_util import ftime

def text_translation(target_lang):
    print(f"{ftime()}: Starting text translation...")
    base_folder = os.environ.get('VIDEOS_FOLDER')
    translation_json_file = f"{base_folder}translation.json"
    translation_srt_file = f"{base_folder}translation.srt" 
    
    # Opening JSON file
    json_object = {}
    transcript_url = f"{base_folder}/transcript.json"
    with open(transcript_url) as file:
        # Reading from json file
        json_object = json.load(file)
        
    text = generate_segmented_text(json_object)
    translate_client = translate.Client()
    # Detect the source language
    translate_client.detect_language(text)
    
    # Translate the text
    translation_text = translate_client.translate(text, target_language=target_lang)
    # Generate a response in the target language
    
    # Write the transcription to the output JSON file
    segmented_text_to_json(translation_json_file, translation_text['translatedText'])
    
    # Write the transcription to the output SRT file
    segmented_text_to_srt(translation_srt_file, translation_text['translatedText'])
    print(f"{ftime()}: Text translation done!")
    
    pass


def generate_segmented_text(json_file):
    segmented_text = ""
    for segment in json_file["segments"]:
        segmented_text += f'<span translate="no">{segment["start"]}-{segment["end"]}</span>{segment["text"]}'
    return segmented_text

def segmented_text_to_json(translation_file, segmented_text):
    translation = []
    for seg in segmented_text.split('<span translate="no">'):
        if seg == '':
            continue
        time, text = seg.split('</span>')
        start, end = time.split('-')
        translation.append({
            'start': float(start),
            'end': float(end),
            'text': text
        })
    json_object = json.dumps(translation, indent=4)
    with open(translation_file, 'w') as f:
        f.write(json_object)
        
def segmented_text_to_srt(translation_file, segmented_text):
    with open(translation_file, 'w') as f:
        for index, seg in enumerate(segmented_text.split('<span translate="no">')):
            if seg == '':
                continue
            time, text = seg.split('</span>')
            start, end = time.split('-')
            f.write(f'{index}\n')
            f.write(f'{format_date(start)} --> {format_date(end)}\n')
            f.write(f'{text}\n')
            
def format_date(time):
    seconds = round(float(time)) 
    return str(datetime.timedelta(seconds=seconds)) + ',000'