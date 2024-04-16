import os, json, time, sys

import trio
from flask import Flask, request, send_from_directory
from dotenv import load_dotenv
load_dotenv()

from modules.stream_to_video import stream_to_video
from modules.audio_to_text import audio_to_text
# from server.modules.text_translation_gtranslate import text_translation
from modules.generate_subtitle import generate_subtitle
from modules.text_translation_openai import text_translation
from modules.scrape_video_url import scrape_video_url
from modules.time_util import ftime

# print(os.environ.get('VIDEOS_FOLDER'))

app = Flask(__name__)

# main route to perform video full process
@app.route('/')
def process_video(stream_url = None, lang = None):
    duration = {'start': ftime()}
    
    # Step0: cleanup the videos folder
    os.system('rm -rf ./videos/*')

    # Step1: get video from stream url
    if (stream_url is None):
        stream_url = request.args.get("url")
    stream_to_video(stream_url)
    duration['stream_to_video'] = ftime()
    
    # Test data
    # stream_url = "https://manifest.arte.tv/api/manifest/v1/Generate/240117202245/fr/XQ/117014-013-A.m3u8"
    
    # Step2: get video transcript
    audio_to_text()
    duration['audio_to_text'] = ftime()
    
    # Step3: translate transcript
    if(lang is None):
        lang = request.args.get("lang")
    text_translation(lang)
    duration['text_translation'] = ftime()
    
    # Step4: generate video subtitles
    generate_subtitle()
    duration['generate_subtitle'] = ftime()
    base_folder = os.environ.get('VIDEOS_FOLDER')
    output = {
        'original_vid_url': f"{base_folder}/original.mp4",
        'stream_url': stream_url,
        'transcript': f"{base_folder}/transcript.json",
        'translation': f"{base_folder}/translation.srt",
        'final_video': f"{base_folder}/translated.mp4",
        'duration': duration
    }
    return json.dumps(output)

# route exposing created videos
@app.route('/videos/<path:path>')
def send_report(path):
    return send_from_directory('videos', path)

async def sub_via_scraping(lang):
    print(f"{ftime()}: Start Arte Journal scraping...")
    url = await scrape_video_url()
    print(f"{ftime()}: Scraping done! URL and lang: ", url, lang)
    process_video(stream_url=url, lang=lang)

if __name__ == '__main__':
    # args mode
    if (len(sys.argv) == 2):
        trio.run(sub_via_scraping, sys.argv[1])
        sys.exit(0)
    elif (len(sys.argv) == 3):
        process_video(lang=sys.argv[2], stream_url=sys.argv[1])
    else:
        user_choice = input("Welcome to the Arte Journal video subber! What do you want to do?\n1 - Sub video via Chrome extension\n2 - Sub video via Scraping\n>")
        if(user_choice == "1"):
            app.run()
        elif(user_choice == "2"):
            lang = input("What lang should we translate to? en|pt|fr\n>")
            trio.run(sub_via_scraping, lang)
        else:
            print("Byeee!")
            sys.exit(0)