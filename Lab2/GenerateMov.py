# from TransferMovie import Movie2Text
# from TransferMovie import Movie2Text
import ModifyBGM
# import numpy as np
from CutVideo import cut_video, hor_to_ver, add_caption
from summarization import digest, keyword, keyphrase
from TransferMovie import Movie2Text

if __name__ == "__main__":
    # ex_tmp_aud = "./audio/tmp_new.wav"
    # input_mov = "./movie/main1.mp4"
    mov_name = "main3"
    fmt = "flv"
    mov_begin = None
    mov_end = None
    input_mov = f"./movie/{mov_name}.{fmt}"
    output_mov = f"./movie/{mov_name}_ex.mp4"
    transfer = Movie2Text()
    transfer.set_movie(input_mov, mov_begin, mov_end)
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
    mov = cut_video(transfer.mov, txt_seg, txt_sentence, add_caption=False)
    mov = hor_to_ver(mov)
    mov = add_caption(mov, keyword(txt))
    # mov = add_caption(mov, keyphrase(txt, 4))
    mov.write_videofile(output_mov)
    # generator1 = ModifyBGM.Generator()
    # generator1.set_input(test_mov, 1200, 2940)
    # generator1.get_output()
    # tmp_aud = "./audio/tmp.wav"
    # mov = me.VideoFileClip(test_mov)

    # res = transfer.audio_to_text(ex_tmp_aud)
    # print(res)
