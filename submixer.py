import cv2
import pysrt
import textwrap
import moviepy.editor as mp
import os

# Load the video file
video_file = "output.mp4"
cap = cv2.VideoCapture(video_file)

# Load the subtitle file
subtitle_file = "output.srt"
subtitle = pysrt.open(subtitle_file)

# Create an output video writer
output_filename = "output_video_with_subtitles_opencv.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for MP4
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height), True)  # Set isColor=True

# Function to convert SubRipTime to milliseconds
def subrip_to_milliseconds(subrip_time):
    return (subrip_time.hours * 3600 + subrip_time.minutes * 60 + subrip_time.seconds) * 1000 + subrip_time.milliseconds

# Iterate through the subtitles and add them to the video frames
current_subtitle = 0
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2
font_thickness = 5
text_color = (255, 255, 255)
line_height = 100  # Increase line height to prevent text overlap
y_position = "bottom"  # Available options - center, top, bottom

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Get the current time in milliseconds
    current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)

    # Check if there are subtitles for this time
    while current_subtitle < len(subtitle) and subrip_to_milliseconds(subtitle[current_subtitle].end) < current_time_ms:
        current_subtitle += 1

    # Add subtitle text to the frame
    if current_subtitle < len(subtitle):
        subtitle_text = subtitle[current_subtitle].text_without_tags
        wrapped_text = textwrap.fill(subtitle_text, width=30)  # Adjust the width as needed
        wrapped_lines = wrapped_text.split('\n')

        if y_position == "top":
            y = 50
        elif y_position == "center":
            y = height // 2 - (line_height * len(wrapped_lines)) // 2
        elif y_position == "bottom":
            y = height - (line_height * len(wrapped_lines)) - 50
        else:
            raise ValueError("Invalid Y position parameter")

        for line in wrapped_lines:
            (text_width, text_height), _ = cv2.getTextSize(line, font, font_scale, font_thickness)
            x = (width - text_width) // 2  # Center horizontally
            cv2.putText(frame, line, (x, y), font, font_scale, text_color, font_thickness)
            y += line_height

    out.write(frame)

cap.release()
out.release()

print("Video with subtitles done:", output_filename)

video_clip = mp.VideoFileClip(video_file)
audio_clip = video_clip.audio
audio_file = "output_audio.mp3"
audio_clip.write_audiofile(audio_file)

print("Audio ripped from original video:", audio_file)

final_output_filename = "final_output_video_with_audio.mp4"
video_with_subtitles = mp.VideoFileClip(output_filename)
final_video = video_with_subtitles.set_audio(mp.AudioFileClip(audio_file))
final_video.write_videofile(final_output_filename, codec="libx264", audio_codec="aac")
os.remove("output_audio.mp3")
os.remove("output_video_with_subtitles_opencv.mp4")

print("Final video with audio done:", final_output_filename)
