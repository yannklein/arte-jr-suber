import ffmpeg

def generate_subtitle(translation_url, video_url):
    translated_url = 'videos/translated.mp4'

    in_video = ffmpeg.input(video_url).filter("subtitles", translation_url)
    out_video = ffmpeg.output(in_video, translated_url, vcodec="copy", acodec="copy")
    out_video.run()
    return translated_url