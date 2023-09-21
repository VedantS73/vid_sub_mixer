from moviepy.editor import VideoFileClip
import pysrt

video_clip = VideoFileClip("output.mp4")

subtitle = pysrt.open("output.srt")
print(subtitle)
def float_to_milliseconds(time):
    return int(time * 1000)

def add_subtitles(get_frame, t):
    frame = get_frame(t)
    subtitle_text = ""
    for s in subtitle:
        if s.start <= float_to_milliseconds(t) <= s.end:
            subtitle_text = s.text_without_tags
            break
    return frame

video_with_subtitles = video_clip.fl(add_subtitles)

output_filename = "output_video_with_subtitles.mp4"

video_with_subtitles.write_videofile(output_filename, codec="libx264", audio_codec="aac")

video_clip.close()

print("OUTPUT DONE ", output_filename)
