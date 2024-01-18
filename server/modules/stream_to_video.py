import ffmpeg

def stream_to_video(stream_url):
    original_vid_url = 'videos/original.mp4'
    in_video = ffmpeg.input(stream_url, protocol_whitelist="file,http,https,tcp,tls,crypto")
    out_video = ffmpeg.output(in_video, original_vid_url, vcodec="copy", acodec="copy")
    out_video.run()
    return original_vid_url