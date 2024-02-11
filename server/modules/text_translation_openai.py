import datetime
import requests
import json
import os
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

def text_translation(transcript_url, target_lang):
    
    langs = {
        'fr': 'french',
        'en': 'english',
        'pt': 'portugues'
    }
    
    url = os.getenv('LIBRETRANSLATE_DEV_URL')
    translation_json_file = "./videos/translation.json"
    translation_srt_file = "./videos/translation.srt" 
    
    # Opening JSON file
    json_object = {}
    with open(transcript_url) as file:
        # Reading from json file
        json_object = json.load(file)
        
    segmented_dict = generate_segmented_dict(json_object)
    # print(segmented_dict)
    
    client = OpenAI()
    
    # cut the transcript in two pieces to fit openai prompt limit
    seg1 = dict(list(segmented_dict.items())[int(len(segmented_dict)/2):])
    seg2 = dict(list(segmented_dict.items())[:int(len(segmented_dict)/2)])

    # translate each half
    trans_seg1 = json.loads(openai_translate(client, langs[target_lang], seg1))
    trans_seg2 = json.loads(openai_translate(client, langs[target_lang], seg2))

    # reconnect them
    full_trans_seg = dict(trans_seg1)
    full_trans_seg.update(dict(trans_seg2))
    
    # Write the transcription to the output SRT file
    print(full_trans_seg)
    segmented_dict_to_srt(translation_srt_file, full_trans_seg)
    
    return [translation_json_file, translation_srt_file]    

def generate_segmented_dict(json_file):
    segmented_dict = {}
    for segment in json_file["segments"]:
        segmented_dict[f'{segment["start"]}-{segment["end"]}'] = segment["text"]
    return segmented_dict

def segmented_dict_to_srt(translation_file, segmented_dict):
    index = 1
    with open(translation_file, 'w') as f:
        for timestamp, transcript in segmented_dict.items():
            if timestamp == '' or transcript == '':
                continue
            start, end = timestamp.split('-')
            f.write(f'{index}\n')
            f.write(f'{format_date(start)} --> {format_date(end)}\n')
            f.write(f'{transcript}\n')
            index += 1
            
def format_date(time):
    seconds = round(float(time)) 
    return str(datetime.timedelta(seconds=seconds)) + ',000'

def openai_translate(client, lang, seg):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
        {"role": "system", "content": "You are a meticulous video transcript translator for a TV news."},
        {
            "role": "user", 
            "content": 
                f"""
                The following data is a JSON file containing the segmented transcript of a TV news video.
                Each transcript segment is represented by a key/value pair of the JSON file.
                Each key represents the time frame of the segment and should be ignored.
                Each value represent the transcript for this segment.
                Translate each value of each segment in {lang}. 
                The segment translation should match the context of the whole transcript.
                Your output should be a copy of the original JSON file with each value replaced by their corresponding translation.
                Your output should only contain the JSON file.
                Here is the data: {seg}
                """}
    ]
    )
    return response.choices[0].message.content