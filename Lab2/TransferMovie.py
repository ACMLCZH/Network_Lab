import wave
import requests
import base64
import moviepy.editor as me
import ffmpy
import os


class Movie2Text:
    def __init__(self):
        self.tmp_dir = "./audio/tmp"
        self.slot = 0.05
        self.low_threshold = 0.15
        self.low_dur = 5
        self.seg_limit = 4.5
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
        self.txt_list = list()
        self.aud_list_vol = list()
        print("Token:", self.token)

    def set_movie(self, mov_file):
        self.mov = me.VideoFileClip(mov_file)
        self.aud = self.mov.audio.fx(me.afx.audio_normalize)
        aud_duration = self.mov.duration
        print("Movie Duration:", aud_duration)
        del self.aud_list_vol[:], self.seg_list[:]
        cur_begin, cur_low_count, cur_starting = 0, 0, False
        for i in range(int(self.mov.duration / self.slot)):
            # clip_mov = self.mov.subclip(self.slot * i, self.slot * (i + 1))
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
                    if cur_low_count >= self.low_threshold:
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

        # AClip.write_audiofile(os.path.join(self.tmp_dir, f"t{i}.wav"))
        # tmp_aud_file = os.path.join(self.tmp_dir, "t.wav")
        # self.aud.write_audiofile(tmp_aud_file)

    def audio_to_text(self):
        del self.txt_list[:]
        for i in range(len(self.seg_list)):
            print("\n##################")
            clip_begin, clip_end = self.seg_list[i]
            tmp_aud_file = os.path.join(self.tmp_dir, f"t{i}.wav")
            tmp_ex_file = os.path.join(self.tmp_dir, f"ext{i}.wav")
            self.aud.subclip(clip_begin * self.slot, clip_end * self.slot).write_audiofile(tmp_aud_file)
            ff = ffmpy.FFmpeg(
                executable="./lib/ffmpeg-master-latest-win64-lgpl-shared/bin/ffmpeg.exe",
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
            print("###", type(audio_channel), type(audio_rate))
            # print(self)
            base64_data = base64.b64encode(data).decode('utf-8')
            json_data = {
                'format': self.format,
                'rate': audio_rate,
                # 'channel': audio_channel,
                'channel': audio_channel,
                'cuid': self.cuID,
                'len': len(data),
                'speech': base64_data,
                'token': self.token,
                'dev_pid': self.dev_pid
            }
            # print(json_data)
            headers = {'Content-Type': 'application/json'}
            res = requests.post(self.transfer_url, json=json_data, headers=headers).json()
            if 'result' in res:
                self.txt_list.append(res['result'][0])
            else:
                self.txt_list.append(res)
            print(self.txt_list[-1])

