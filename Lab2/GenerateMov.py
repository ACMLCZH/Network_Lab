# from TransferMovie import Movie2Text
# from TransferMovie import Movie2Text
import ModifyBGM
# import numpy as np
from CutVideo import cut_video, hor_to_ver, add_caption, add_title
from summarization import digest, keyword, keyphrase
from TransferMovie import Movie2Text

if __name__ == "__main__":
    # ex_tmp_aud = "./audio/tmp_new.wav"
    # input_mov = "./movie/main1.mp4"
    data = [
        ["main1", "mp4", 600, 1500, ["“双重领导”下的矛盾"]],
        ["main2", "flv", None, None, ["一面盾牌引发的“惨案”"]],
        ["main4", "mkv", 780, 1980, ["当历史课不及格的公子", "参加考古工作"]],
        ["main5", "mp4", 1800, 2700, ["“精神是不能肮脏的”"]],  # == "main1"
    ]
    sel = 3
    # mov_name = "main4"
    # fmt = "mkv"
    # mov_begin = 780
    # mov_end = 1980
    # title = ["当历史课不及格的公子", "参加考古工作"]
    input_mov = f"./movie/{data[sel][0]}.{data[sel][1]}"
    output_mov = f"./movie/{data[sel][0]}_ex.mp4"
    # title = ["一面盾牌引发的“惨案”"]
    transfer = Movie2Text()
    transfer.set_movie(input_mov, data[sel][2], data[sel][3])
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
    mov = add_title(mov, data[sel][4])
    # mov = add_caption(mov, keyphrase(txt, 4))
    mov.write_videofile(output_mov)
    # generator1 = ModifyBGM.Generator()
    # generator1.set_input(test_mov, 1200, 2940)
    # generator1.get_output()
    # tmp_aud = "./audio/tmp.wav"
    # mov = me.VideoFileClip(test_mov)

    # res = transfer.audio_to_text(ex_tmp_aud)
    # print(res)
