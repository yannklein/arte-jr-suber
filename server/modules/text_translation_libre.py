import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()

def text_translation(transcript_url, target_lang):
    url = os.getenv('LIBRETRANSLATE_DEV_URL')
    translation_json_file = "./videos/translation.json"
    translation_srt_file = "./videos/translation.srt" 
    
    # Opening JSON file
    json_object = {}
    with open(transcript_url) as file:
        # Reading from json file
        json_object = json.load(file)
        
    text = generate_segmented_text(json_object)

    payload = json.dumps({
    "q": text,
    "source": "auto",
    "target": target_lang,
    "format": "text",
    "api_key": ""
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'session=536a75f0-6472-43eb-8044-abac3aae717c'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    
def generate_segmented_text(json_file):
    segmented_text = ""
    for segment in json_file["segments"]:
        segmented_text += f'[[{segment["start"]}-{segment["end"]}]]{segment["text"]}'
    return segmented_text

def segmented_text_to_srt(translation_file, segmented_text):
    translation = []
    with open(translation_file, 'w') as f:
        for index, seg in enumerate(segmented_text.split('[[')):
            if seg == '':
                continue
            time, text = seg.split(']]')
            start, end = time.split('-')
            f.write(f'{index}\n')
            f.write(f'{format_date(start)} --> {format_date(end)}\n')
            f.write(f'{text}\n')
            
def format_date(time):
    seconds = round(float(time)) 
    return str(datetime.timedelta(seconds=seconds)) + ',000'