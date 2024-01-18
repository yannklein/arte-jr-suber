import json, urllib.request
from google.cloud import translate_v2 as translate
 

def text_translation(transcript_url, target_lang):
    
    translation_file = "videos/translation.json"
    
    # Opening JSON file
    json_object = {}
    with urllib.request.urlopen(transcript_url) as url:
        # Reading from json file
        json_object = json.load(url)
        
    text = generate_segmented_text(json_object)
    print(text)
    translate_client = translate.Client()
    # Detect the source language
    translate_client.detect_language(text)
    
    # Translate the text
    translation_text = translate_client.translate(text, target_language=target_lang)
    # Generate a response in the target language
    
    translation_dict = unpack_segmented_text(translation_text['translatedText'])
    
    json_object = json.dumps(translation_dict, indent=4)

    # Write the transcription to the output file
    with open(translation_file, 'w') as f:
        f.write(json_object)
    
    return translation_file


def generate_segmented_text(json_file):
    segmented_text = ""
    for segment in json_file["segments"]:
        segmented_text += f'[[{segment["start"]}][{segment["end"]}]]{segment["text"]}'
    return segmented_text

def unpack_segmented_text(segmented_text):
    print(segmented_text)
    translation = []
    for seg in segmented_text.split('[['):
        if seg == '':
            continue
        time, text = seg.split(']]')
        start, end = time.split('][')
        translation.append({
            'start': start,
            'end': end,
            'text': text
        })
    return translation