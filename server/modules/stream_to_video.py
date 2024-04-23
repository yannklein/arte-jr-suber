import ffmpeg, os
from modules.time_util import ftime

def stream_to_video(stream_url):
    print(f"{ftime()}: Start downloading video stream...")
    base_folder = os.environ.get('VIDEOS_FOLDER')
    original_vid_url = f'{base_folder}/original.mp4'
    original_aud_url = f'{base_folder}/original.mp3'
    
    in_video = ffmpeg.input(stream_url, protocol_whitelist="file,http,https,tcp,tls,crypto")
    out_audio = ffmpeg.output(in_video, original_aud_url, acodec="libmp3lame", loglevel="quiet")
    out_audio.run()
    print(f"{ftime()}: Audio downloaded! Check it out: {original_aud_url}")
    out_video = ffmpeg.output(in_video, original_vid_url, vcodec="copy", acodec="copy", loglevel="quiet")
    out_video.run()
    print(f"{ftime()}: Video downloaded! Check it out: {original_vid_url}")
    
    pass