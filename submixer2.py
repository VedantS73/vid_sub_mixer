from moviepy.editor import VideoFileClip, TextClip, concatenate_videoclips
import pysrt

# Load the video clip
video_clip = VideoFileClip("output.mp4")

# Load the subtitle file
subtitle = pysrt.open("output.srt")

# Function to convert SubRipTime to milliseconds
def subrip_to_milliseconds(subrip_time):
    return (subrip_time.hours * 3600 + subrip_time.minutes * 60 + subrip_time.seconds) * 1000 + subrip_time.milliseconds

# Create an empty list to store subtitle TextClips
subtitle_clips = []

# Iterate through the subtitles and create TextClips for each entry
for s in subtitle:
    start_time_ms = subrip_to_milliseconds(s.start)
    end_time_ms = subrip_to_milliseconds(s.end)
    subtitle_text = s.text_without_tags
    # Create a TextClip for each subtitle entry
    subtitle_clip = TextClip(subtitle_text, fontsize=24, color='white')
    # Set the duration of the subtitle_clip based on the start and end times
    subtitle_clip = subtitle_clip.set_start(start_time_ms / 1000).set_duration((end_time_ms - start_time_ms) / 1000)
    subtitle_clips.append(subtitle_clip)

# Concatenate all subtitle clips together
subtitles_clip = concatenate_videoclips(subtitle_clips)

# Overlay the subtitles_clip on top of the video_clip
video_with_subtitles = video_clip.set_audio(None).overlay(subtitles_clip.set_position(("center", "bottom")))

# Write the video with burned-in subtitles
output_filename = "output_video_with_subtitles.mp4"
video_with_subtitles.write_videofile(output_filename, codec="libx264", audio_codec="aac")

# Close the video_clip
video_clip.close()

print("OUTPUT DONE ", output_filename)
