import ffmpeg, os
from modules.time_util import ftime

def generate_subtitle():
    print(f"{ftime()}: Starting subtitle creation...")
    
    base_folder = os.environ.get('VIDEOS_FOLDER')
    translated_url = f'{base_folder}/translated.mp4'
    translation_url = f'{base_folder}/translation.srt'
    video_url = f'{base_folder}/original.mp4'
    
    in_video = ffmpeg.input(video_url)
    ffmpeg.filter(in_video, "subtitles", translation_url).output(in_video.audio, translated_url).run()
    print(f"{ftime()}: Subtitle creation done!")
    pass
