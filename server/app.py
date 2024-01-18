from flask import Flask, request, send_from_directory
import json

from modules.stream_to_video import stream_to_video


app = Flask(__name__)

# main route to perform video full process
@app.route('/')
def process_video():
    # Step1: get video from stream url
    stream_url = request.args.get("url")
    original_vid_url = stream_to_video(stream_url)
    
    return json.dumps({
        'original_vid_url': f'http://127.0.0.1:5000/{original_vid_url}',
        'stream_url': stream_url
    })

# route exposing created videos
@app.route('/videos/<path:path>')
def send_report(path):
    return send_from_directory('videos', path)

if __name__ == '__main__':

    app.run()
