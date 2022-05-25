import os
import jieba
import Debug
import gc
import numpy as np
from TransferMovie import Movie2Text
import moviepy.editor as me


class Generator:
    def __init__(self):
        self.transfer = Movie2Text()
        self.txt_word_list = None
        self.txt = ""
        self.punctuation = ["。", "，", "！", "？", "…", "：", "；", "“", "”"]
        self.stop_word = ["嗯", "嘿嘿", "你", "我", "的", "是", "呵呵", "了", "他", "啊", "吧"]

        self.new_mov = None
        self.selected_word = None
        self.word_num = dict()
        self.word_list = list()
        self.choose_list = list()
        self.add_BGM = "./audio/NM1.mp3"
        # self.new_mov_file = "./movie/res/output.mp4"
        self.bpm = 128

    def set_input(self, mov_file, mov_begin, mov_end):
        self.transfer.set_movie(mov_file, mov_begin, mov_end)

    def get_output(self):
        def get_bound(x, y, sx, sy, fi, fj):
            x1 = int(x - x * fi / fj)
            y1 = int(y - y * fi / fj)
            x2 = int(x + (sx - x) * fi / fj)
            y2 = int(y + (sy - y) * fi / fj)
            return x1, y1, x2, y2

        self.transfer.audio_to_text()
        # Debug.info1(self.transfer)

        self.txt = "".join(self.transfer.txt_list)
        self.txt_word_list = jieba.lcut(self.txt)
        self.word_num.clear()
        for word in self.txt_word_list:
            if word not in self.punctuation and word not in self.stop_word:
                if word in self.word_num:
                    self.word_num[word] += 1
                else:
                    self.word_num[word] = 1
        self.word_list = list(self.word_num.keys())
        self.word_list.sort(key=lambda x: self.word_num[x], reverse=True)

        self.selected_word = self.word_list[0]
        print(self.selected_word)
        if self.word_num[self.selected_word] < 4:
            print("关键词太少！")
            return
        del self.choose_list[:]
        for i in range(len(self.transfer.txt_list)):
            if self.selected_word in self.transfer.txt_list[i]:
                self.choose_list.append(i)
        for ep in range(10):
            np.random.shuffle(self.choose_list)
            seg_clip_list = list()
            seg_clap = 60 / self.bpm
            for i in range(3):
                clip_end = self.transfer.seg_list[self.choose_list[i]][1] * self.transfer.slot - np.random.rand() * 0.5
                clip_begin = clip_end - seg_clap * 8
                seg_clip_list.append(self.transfer.mov.subclip(clip_begin, clip_end))
            clip_pos3 = self.transfer.seg_list[self.choose_list[3]][1] * self.transfer.slot - np.random.rand() * 0.5
            clip_pos2 = clip_pos3 - seg_clap * 1
            clip_pos1 = clip_pos3 - seg_clap * 2
            clip_pos0 = clip_pos3 - seg_clap * 6
            clip_size = self.transfer.mov.size
            pos_x, pos_y = int(np.random.rand() * clip_size[0]), int(np.random.rand() * clip_size[1])
            print(pos_x, pos_y)
            clip3 = self.transfer.mov.subclip(clip_pos1, clip_pos3)
            clip2 = self.transfer.mov.subclip(clip_pos1, clip_pos2)
            clip1 = self.transfer.mov.subclip(clip_pos0, clip_pos1)
            p1x1, p1y1, p1x2, p1y2 = get_bound(pos_x, pos_y, clip_size[0], clip_size[1], 3, 4)
            p2x1, p2y1, p2x2, p2y2 = get_bound(pos_x, pos_y, clip_size[0], clip_size[1], 2, 4)
            p3x1, p3y1, p3x2, p3y2 = get_bound(pos_x, pos_y, clip_size[0], clip_size[1], 1, 4)
            seg_clip_list.extend([
                clip1,
                clip2.crop(x1=p1x1, y1=p1y1, x2=p1x2, y2=p1y2).resize(width=clip_size[0]),
                clip2.crop(x1=p2x1, y1=p2y1, x2=p2x2, y2=p2y2).resize(width=clip_size[0]),
                clip3.crop(x1=p3x1, y1=p3y1, x2=p3x2, y2=p3y2).resize(width=clip_size[0])
            ])
            self.new_mov = me.concatenate_videoclips(seg_clip_list)
            aud1 = self.new_mov.audio
            aud2 = me.AudioFileClip(self.add_BGM).volumex(0.6)
            self.new_mov.audio = me.CompositeAudioClip([aud2, aud1])
            new_mov_file = f"./movie/res/output{ep}.mp4"
            self.new_mov.write_videofile(new_mov_file)

        gc.collect()
