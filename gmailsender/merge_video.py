import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from gmailmonitor import send_email

def merge_videos(directory, output_file):
    video_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.mov')]
    clips = []
    
    for video_file in video_files:
        video_path = os.path.join(directory, video_file)
        clip = VideoFileClip(video_path)
        clips.append(clip)
    
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_file)

# Example usage:
directory = 'D:\Project\MyProject\OttisTourist\merge'
output_file = 'output.mp4'
merge_videos(directory, output_file)
# link_addr = directory + output_file
# send_email('Your video', 'This is your video link: {link_addr}', 'codemaster9428@gmail.com')