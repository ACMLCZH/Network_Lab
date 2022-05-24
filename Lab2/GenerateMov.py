from TransferMovie import Movie2Text
import numpy as np
import time

if __name__ == "__main__":
    transfer = Movie2Text()
    # ex_tmp_aud = "./audio/tmp_new.wav"
    test_mov = "./movie/test1.mp4"
    # tmp_aud = "./audio/tmp.wav"
    # mov = me.VideoFileClip(test_mov)
    transfer.set_movie(test_mov)
    transfer.audio_to_text()
    fw = open(f"./log/log_{time.time()}.txt", "w")
    print(transfer.aud_list_vol, file=fw)
    for i in range(len(transfer.txt_list)):
        lowd, highd = transfer.seg_list[i]
        print(i, transfer.seg_list[i], transfer.txt_list[i],
              np.max(transfer.aud_list_vol[lowd: highd]), np.min(transfer.aud_list_vol[lowd: highd]), file=fw)
    fw.close()

    # res = transfer.audio_to_text(ex_tmp_aud)
    # print(res)
