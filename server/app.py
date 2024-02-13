import os, json, time, sys

import trio
from flask import Flask, request, send_from_directory
# from dotenv import load_dotenv

from modules.stream_to_video import stream_to_video
from modules.audio_to_text import audio_to_text
# from server.modules.text_translation_gtranslate import text_translation
from modules.generate_subtitle import generate_subtitle
from modules.text_translation_openai import text_translation
from modules.scrape_video_url import scrape_video_url

# load_dotenv()
# print(os.environ.get('PROJECTID'))

app = Flask(__name__)

# main route to perform video full process
@app.route('/')
def process_video(stream_url = None, lang = None):
    duration = {'start': time.time()}
    
    # Step0: cleanup the videos folder
    os.system('rm -rf ./videos/*')

    # Step1: get video from stream url
    if (stream_url is None):
        stream_url = request.args.get("url")
    original_urls = stream_to_video(stream_url)
    duration['stream_to_video'] = time.time()
    
    # Test data
    # original_urls = [
    #     "/videos/original.mp4",
    #     "/videos/original.mp3"
    # ]
    # stream_url = "https://manifest.arte.tv/api/manifest/v1/Generate/240117202245/fr/XQ/117014-013-A.m3u8"
    
    # Step2: get video transcript
    transcript = audio_to_text(original_urls[1])
    duration['audio_to_text'] = time.time()
    
    # Test data
    # transcript = "videos/transcript.json"
    
    # Step3: translate transcript
    if(lang is None):
        lang = request.args.get("lang")
    translations = text_translation(transcript, lang)
    duration['text_translation'] = time.time()
    
    # Test data
    # translations = ["videos/translation.json", "videos/translation.srt"]
    
    # Step4: generate video subtitles
    final_video = generate_subtitle(translations[1], original_urls[0])
    duration['generate_subtitle'] = time.time()
    print(duration)
    output = {
        'original_vid_url': original_urls,
        'stream_url': stream_url,
        'transcript': transcript,
        'translation': translations,
        'final_video': final_video,
        'duration': duration
    }
    return json.dumps(output)

# route exposing created videos
@app.route('/videos/<path:path>')
def send_report(path):
    return send_from_directory('videos', path)

async def sub_via_scraping(lang):
    print("sub_via_scraping")
    url = await scrape_video_url()
    print(url, lang)
    process_video(url, lang)

if __name__ == '__main__':
    print("Hi")
    while True:
        user_choice = input("Welcome to the Arte Journal video subber! What do you want to do?\n1 - Sub video via Chrome extension\n2 - Sub video via Scraping\n>")
        if(user_choice == "1"):
            app.run()
        elif(user_choice == "2"):
            lang = input("What lang should we translate to? en|pt|fr\n>")
            trio.run(sub_via_scraping, lang)
        else:
            print("Byeee!")
            sys.exit(0)