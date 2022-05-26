# from TransferMovie import Movie2Text
# from TransferMovie import Movie2Text
import ModifyBGM
# import numpy as np
from cut_video import cut_video
from digest import digest
from TransferMovie import Movie2Text

if __name__ == "__main__":
    # ex_tmp_aud = "./audio/tmp_new.wav"
    input_mov = "./movie/main1.mp4"
    output_mov = "./movie/main1_new.mp4"
    transfer = Movie2Text()
    transfer.set_movie(input_mov, 600, 1500)
    transfer.audio_to_text()
    ori_list = [s[:-1].replace("？", "，").replace("！", "，").replace("…", "，") + s[-1:]
                for s in transfer.txt_list if s != ""]
    ori_seg = [transfer.seg_list[i] for i in range(len(transfer.txt_list)) if transfer.txt_list[i] != ""]
    txt = "".join(ori_list)

    txt_idx, txt_sentence = digest(txt)
    txt_seg = list()
    for idx in txt_idx:
        txt_seg.append((ori_seg[idx][0] * transfer.slot,
                        ori_seg[idx][1] * transfer.slot))
    cut_video(txt_seg, txt_sentence, output_mov, input_video_path=None, input_video=transfer.mov, add_caption=False)
    # generator1 = ModifyBGM.Generator()
    # generator1.set_input(test_mov, 1200, 2940)
    # generator1.get_output()
    # tmp_aud = "./audio/tmp.wav"
    # mov = me.VideoFileClip(test_mov)

    # res = transfer.audio_to_text(ex_tmp_aud)
    # print(res)
