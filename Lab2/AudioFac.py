import moviepy.editor as me


if __name__ == "__main__":
    new_clip = me.AudioFileClip("./audio/M1.mp3")
    print(new_clip.duration)
    new_clip = new_clip.subclip(128, 143)
    new_clip.write_audiofile("./audio/NM1.mp3")

