import os, json, time

from flask import Flask, request, send_from_directory
# from dotenv import load_dotenv

from modules.stream_to_video import stream_to_video
from modules.audio_to_text import audio_to_text
from modules.text_translation import text_translation
from modules.generate_subtitle import generate_subtitle


# load_dotenv()
# print(os.environ.get('PROJECTID'))

app = Flask(__name__)

# main route to perform video full process
@app.route('/')
def process_video():
    duration = {'start': time.time()}
    
    # Step0: cleanup the videos folder
    os.system('rm -rf ./videos/*')

    # Step1: get video from stream url
    stream_url = request.args.get("url")
    original_urls = stream_to_video(stream_url)
    duration['stream_to_video'] = time.time()
    
    # original_urls = [
    #     "http://127.0.0.1:8000/videos/original.mp4",
    #     "http://127.0.0.1:8000/videos/original.mp3"
    # ]
    # stream_url = "https://manifest.arte.tv/api/manifest/v1/Generate/240117202245/fr/XQ/117014-013-A.m3u8"
    
    # Step2: get video transcript
    transcript = audio_to_text(original_urls[1])
    duration['audio_to_text'] = time.time()
    # transcript = "videos/transcript.json"
    
    # Step3: translate transcript
    lang = request.args.get("lang")
    translations = text_translation(f'http://127.0.0.1:8000/{transcript}', lang)
    duration['text_translation'] = time.time()
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

if __name__ == '__main__':

    app.run()
