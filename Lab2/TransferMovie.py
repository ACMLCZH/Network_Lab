import wave
import requests
import base64
import json
import moviepy.editor as me
import ffmpy
import os


class Movie2Text:
    def __init__(self):
        self.tmp_dir = "./audio/tmp"
        self.slot = 0.05
        self.low_threshold = 0.20
        self.low_dur = 4
        self.seg_limit = 5
        self.seg_list = list()
        self.mov = None
        self.aud = None

        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        self.APIKey = "GWS3cAGudlndSaYmSBK4N93R"
        self.SecretKey = "qG2iwMfP3Rlu5kdyzlO5Yapco1mcl3wu"
        self.transfer_url = 'https://vop.baidu.com/server_api'
        self.cuID = "*******"
        self.format = "wav"
        self.dev_pid = 1537
        self.host = self.token_url % (self.APIKey, self.SecretKey)
        self.token = requests.post(self.host).json()['access_token']
        self.txt_file = "./txt/tmp.txt"
        self.data_file = None
        # self.txt_file = None
        self.txt_list = list()
        self.aud_list_vol = list()
        print("Token:", self.token)

    def set_movie(self, mov_file, mov_begin=None, mov_end=None):
        self.mov = me.VideoFileClip(mov_file)
        if mov_begin is None:
            mov_begin = 0
        if mov_end is None:
            mov_end = self.mov.duration
        self.data_file = f"./txt/{mov_file[mov_file.rfind('/') + 1: mov_file.rfind('.')]}.json"
        self.mov = self.mov.subclip(mov_begin, mov_end)
        self.aud = self.mov.audio.fx(me.afx.audio_normalize)
        self.mov.audio = self.aud
        aud_duration = self.mov.duration
        print("Movie Duration:", aud_duration)

        del self.aud_list_vol[:], self.seg_list[:]
        cur_begin, cur_low_count, cur_starting = 0, 0, False
        for i in range(int(self.mov.duration / self.slot)):     # 将音频片段细分为slot，根据每个slot的音量来判断一句话的结束
            clip_aud = self.aud.subclip(self.slot * i, self.slot * (i + 1))
            clip_vol = clip_aud.max_volume()
            self.aud_list_vol.append(clip_vol)
            if clip_vol > self.low_threshold:
                if cur_starting:
                    cur_low_count = 0
                else:
                    cur_starting = True
                    cur_begin = i
            else:
                if cur_starting:
                    cur_low_count += 1
                    if cur_low_count >= self.low_dur:
                        cur_low_count = 0
                        cur_starting = False
                        cur_end = i
                        if len(self.seg_list) > 0 and (cur_end - self.seg_list[-1][0]) * self.slot < self.seg_limit:
                            self.seg_list[-1][1] = cur_end
                        else:
                            if (cur_end - cur_begin) * self.slot < self.seg_limit:
                                self.seg_list.append([cur_begin, cur_end])
                            else:
                                print("Too long speech:", [cur_begin, cur_end])
        if cur_starting:
            cur_end = int(self.mov.duration / self.slot)
            if len(self.seg_list) > 0 and (cur_end - self.seg_list[-1][0]) * self.slot < self.seg_limit:
                self.seg_list[-1][1] = cur_end
            else:
                if (cur_end - cur_begin) * self.slot < self.seg_limit:
                    self.seg_list.append([cur_begin, cur_end])
                else:
                    print("Too long speech:", [cur_begin, cur_end])
        print(self.aud_list_vol)
        print(self.seg_list)

    def audio_to_text(self):
        if os.path.exists(self.data_file):          # 减少语音转文本的查询次数
            print("TXT Cache detected!")
            fr = open(self.data_file, "r")
            dj = json.load(fr)
            fr.close()
            old_list = dj["seg_list"]
            self.txt_list = dj["txt_list"]
            equal = len(old_list) == len(self.txt_list)
            if equal:
                for i in range(len(self.seg_list)):
                    if self.seg_list[i][0] != old_list[i][0] or self.seg_list[i][1] != old_list[i][1]:
                        equal = False
            if equal:
                return
            else:
                print("Not equal to Cache!")

        del self.txt_list[:]
        open(self.txt_file, "w").close()
        for i in range(len(self.seg_list)):
            print("\n##################")
            clip_begin, clip_end = self.seg_list[i]
            tmp_aud_file = os.path.join(self.tmp_dir, f"t{i}.wav")
            tmp_ex_file = os.path.join(self.tmp_dir, f"ext{i}.wav")
            self.aud.subclip(clip_begin * self.slot, clip_end * self.slot).write_audiofile(tmp_aud_file)
            ff = ffmpy.FFmpeg(              # 原音频不是采样率为16000Hz的，必须转换为16000Hz
                # executable="./lib/ffmpeg-master-latest-win64-lgpl-shared/bin/ffmpeg.exe",
                inputs={tmp_aud_file: None},
                outputs={tmp_ex_file: '-f {} -vn -ac 1 -ar 16000 -y'.format('wav')}
            )
            ff.run()

            with open(tmp_ex_file, 'rb') as f:
                data = f.read()
            audio_file = wave.open(tmp_ex_file, "r")
            audio_channel = audio_file.getnchannels()
            audio_rate = audio_file.getframerate()
            print("###", audio_channel, audio_rate)
            base64_data = base64.b64encode(data).decode('utf-8')
            json_data = {
                'format': self.format, 'rate': audio_rate, 'channel': audio_channel, 'cuid': self.cuID,
                'len': len(data), 'speech': base64_data, 'token': self.token, 'dev_pid': self.dev_pid
            }
            # print(json_data)
            headers = {'Content-Type': 'application/json'}
            res = requests.post(self.transfer_url, json=json_data, headers=headers).json()
            fw = open(self.txt_file, "a")
            if 'result' in res:
                self.txt_list.append(res['result'][0])
                print(self.txt_list[-1], file=fw)
            else:
                self.txt_list.append("")
                print(res, file=fw)
            fw.close()
            print(self.txt_list[-1])
        fw = open(self.data_file, "w")
        json.dump({"seg_list": self.seg_list, "txt_list": self.txt_list}, fw)
        fw.close()

