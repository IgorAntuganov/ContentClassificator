import moviepy

clip = moviepy.VideoFileClip("source_path.mp4")
clip.audio.write_audiofile("audio_path.mp3")
cut_clip = clip.subclipped(50, 60)
cut_clip.write_videofile("cut_video_path.mp4")
