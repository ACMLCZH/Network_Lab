import os
import jieba
import Debug
from TransferMovie import Movie2Text


class Generator:
    def __init__(self):
        self.transfer = Movie2Text()
        self.txt = ""
        self.txt_word_list = None
        self.punctuation = ["。", "，", "！", "？", "…", "：", "；", "“", "”"]
        self.stop_word = ["嗯", "嘿", "你", "我", "的", "是", "呵呵", "了", "他", "啊", "吧"]
        self.word_num = dict()
        self.word_list = list()

    def set_input(self, mov_file, mov_begin, mov_end):
        self.transfer.set_movie(mov_file, mov_begin, mov_end)

    def get_output(self):
        self.transfer.audio_to_text()
        Debug.info1(self.transfer)

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
        for i in range(5):
            print(self.word_list[i], self.word_num[self.word_list[i]])



