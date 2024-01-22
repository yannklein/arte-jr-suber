import ffmpeg

def generate_subtitle(translation_url, video_url):
    translated_url = './videos/translated.mp4'

    in_video = ffmpeg.input(video_url)
    ffmpeg.filter(in_video, "subtitles", translation_url).output(in_video.audio, translated_url).run()
    return translated_url

# generate_subtitle('/Users/kleinyann/github/arte-jr-suber/server/videos/translation.srt','/Users/kleinyann/github/arte-jr-suber/server/videos/original.mp4')