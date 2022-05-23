import moviepy.editor as me
from TransferAudio import Audio2Text

if __name__ == "__main__":
    transfer = Audio2Text()
    test_mov = "./movie/test1.mp4"
    tmp_aud = "./audio/tmp.wav"
    mov = me.VideoFileClip(test_mov).subclip(10, 14)
    aud = mov.audio
    aud.write_audiofile(tmp_aud)
    res = transfer.audio_to_text(tmp_aud)
    print(res)
