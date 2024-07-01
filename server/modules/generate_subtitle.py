import ffmpeg, os
from modules.time_util import ftime

def generate_subtitle():
    print(f"{ftime()}: Starting subtitle creation...")
    
    base_folder = os.environ.get('VIDEOS_FOLDER')
    translated_url = f'{base_folder}/translated.mp4'
    translation_url = f'{base_folder}/translation.srt'
    video_url = f'{base_folder}/original.mp4'
    
    try:
        in_video = ffmpeg.input(video_url)
        ffmpeg.filter(in_video, "subtitles", translation_url).output(in_video.audio, translated_url, loglevel="quiet").run(capture_stdout=True, capture_stderr=True)
        print(f"{ftime()}: Subtitle creation done! Check it out: {translated_url}")
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e
    pass
