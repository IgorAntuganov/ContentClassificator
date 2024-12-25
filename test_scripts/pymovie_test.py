import moviepy

clip = moviepy.VideoFileClip("../video_test/myvideo.mp4")
clip.audio.write_audiofile("../video_test/myaudio.mp3")
cut_clip = clip.subclipped(50, 60)
cut_clip.write_videofile("../video_test/cut_video.mp4")
