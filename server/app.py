import os
import json
from flask import Flask, request, send_from_directory

from modules.stream_to_video import stream_to_video


app = Flask(__name__)

# main route to perform video full process
@app.route('/')
def process_video():
    
    # Step0: cleanup the videos folder
    os.system('rm -rf ./videos/*')

    # Step1: get video from stream url
    stream_url = request.args.get("url")
    original_urls = stream_to_video(stream_url)
    
    # Step2: get video transcript
    outupt = {
        'original_vid_url': original_urls,
        'stream_url': stream_url
    }
    return json.dumps(outupt)

# route exposing created videos
@app.route('/videos/<path:path>')
def send_report(path):
    return send_from_directory('videos', path)

if __name__ == '__main__':

    app.run()
