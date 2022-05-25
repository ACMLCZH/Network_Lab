# from TransferMovie import Movie2Text
# from TransferMovie import Movie2Text
import ModifyBGM
# import numpy as np


if __name__ == "__main__":
    # ex_tmp_aud = "./audio/tmp_new.wav"
    test_mov = "./movie/test5.mkv"
    generator1 = ModifyBGM.Generator()
    generator1.set_input(test_mov, 1200, 2940)
    generator1.get_output()
    # tmp_aud = "./audio/tmp.wav"
    # mov = me.VideoFileClip(test_mov)

    # res = transfer.audio_to_text(ex_tmp_aud)
    # print(res)
