import ffmpeg

def stream_to_video(stream_url):
    original_vid_url = 'videos/original.mp4'
    original_aud_url = 'videos/original.mp3'
    in_video = ffmpeg.input(stream_url, protocol_whitelist="file,http,https,tcp,tls,crypto")
    out_audio = ffmpeg.output(in_video, original_aud_url, acodec="libmp3lame")
    out_audio.run()
    out_video = ffmpeg.output(in_video, original_vid_url, vcodec="copy", acodec="copy")
    out_video.run()
    return [
        f'http://127.0.0.1:8000/{original_vid_url}', 
        f'http://127.0.0.1:8000/{original_aud_url}'
    ]