import ffmpeg
from modules.time_util import ftime

def generate_subtitle(translation_url, video_url):
    print(f"{ftime()}: Starting subtitle creation...")
    translated_url = './videos/translated.mp4'

    in_video = ffmpeg.input(video_url)
    ffmpeg.filter(in_video, "subtitles", translation_url).output(in_video.audio, translated_url).run()
    print(f"{ftime()}: Subtitle creation done!")
    return translated_url
