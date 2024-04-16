import datetime
import json
import os
from openai import OpenAI
from modules.time_util import ftime


def text_translation(target_lang):
    print(f"{ftime()}: Starting text translation...")
    langs = {
        'fr': 'french',
        'en': 'english',
        'ja': 'japanese',
        'pt': 'portugues'
    }
    
    url = os.getenv('LIBRETRANSLATE_DEV_URL')
    base_folder = os.environ.get('VIDEOS_FOLDER')
    translation_srt_file = f"{base_folder}/translation.srt" 
    transcript_url = f"{base_folder}/transcript.json"
    
    # Opening JSON file
    json_object = {}
    with open(transcript_url) as file:
        # Reading from json file
        json_object = json.load(file)
        
    segmented_dict = generate_segmented_dict(json_object)
    
    client = OpenAI()
    
    # cut the transcript in two pieces to fit openai prompt limit
    segments = {}
    char_count = 0 
    start_index = 0
    for index, (timestamp, text) in enumerate(segmented_dict.items()):
        char_count += len(f"\{{ '{timestamp}': '{text}', ")
        if (char_count >= 6000 or index >= len(segmented_dict) - 1):
            segment = dict(list(segmented_dict.items())[start_index:index])
            # print("char count: ", char_count)
            # print("segment: ", segment)
            openai_output = openai_translate(client, langs[target_lang], segment)
            # print("openai_output: ", openai_output)
            translated_segment = json.loads(openai_output)
            segments.update(translated_segment)
            start_index = index + 1
            char_count = 0
    
    # Write the transcription to the output SRT file
    segmented_dict_to_srt(translation_srt_file, segments)
    print(f"{ftime()}: Text translation done!")
    pass

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
    messages = [
        {"role": "system", "content": "You are a meticulous video transcript translator for a TV news."},
        {"role": "user", 
        "content": 
            f"""
            The following data is a JSON file containing the segmented transcript of a TV news video.
            Each transcript segment is represented by a key/value pair of the JSON file.
            Each key represents the time frame of the segment and should be ignored.
            Each value represent the transcript for this segment.
            Translate each value of each segment in {lang}. 
            The segment translation should match the context of the whole transcript.
            Your output should be a copy of the original JSON file with each value replaced by their corresponding translation.
            Your output should only contain the JSON file. You should make sure the JSON file structure is valid and you should correct it if it's not.
            Here is the data: {seg}
            """
        }
    ]
    )
    return response.choices[0].message.content