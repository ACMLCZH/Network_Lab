import wave
import requests
import time
import base64
from pyaudio import PyAudio, paInt16
import webbrowser
# FILEPATH = 'test6.wav'


class Audio2Text:
    def __init__(self):
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        self.APIKey = "GWS3cAGudlndSaYmSBK4N93R"
        self.SecretKey = "qG2iwMfP3Rlu5kdyzlO5Yapco1mcl3wu"
        self.transfer_url = 'https://vop.baidu.com/server_api'
        self.dev_pid = 1537
        self.host = self.token_url % (self.APIKey, self.SecretKey)
        self.token = None

    def get_token(self):
        res = requests.post(self.host)
        self.token = res.json()['access_token']

    def audio_to_text(self, file):
        # FORMAT = 'wav'
        # RATE = '16000'
        # CHANNEL = 1
        with open(file, 'rb') as f:
            data = f.read()
        audio_file = wave.open(file, "r")
        audio_channel = audio_file.getnchannels()
        audio_rate = audio_file.getframerate()
        print("###", audio_channel, audio_rate)
        base64_data = base64.b64encode(data).decode('utf-8')
        json_data = {
            'format': "wav",
            'rate': audio_rate,
            'channel': audio_channel,
            'cuid': '*******',
            'len': len(base64_data),
            'speech': base64_data,
            'token': self.token,
            'dev_pid': self.dev_pid
        }
        headers = {'Content-Type': 'application/json'}
        print('正在识别...')
        res = requests.post(self.transfer_url, json=json_data, headers=headers).json()
        if 'result' in res:
            return res['result'][0]
        else:
            return res
        # Result = res.json()
            # r=requests.post(url,data=json.dumps(data),headers=headers)


# def callback(in_data, frame_count, time_info, status):
#     data = wf.readframes(frame_count)
#     return (data, pyaudio.paContinue)


# def save_wave_file(filepath, data):
#     wf = wave.open(filepath, 'wb')
#     wf.setnchannels(channels)
#     wf.setsampwidth(sampwidth)
#     wf.setframerate(framerate)
#     wf.writeframes(b''.join(data))
#     wf.close()


# def my_record():
#     framerate = 16000  # 采样率
#     num_samples = 2000  # 采样点
#     channels = 1  # 声道
#     sampwidth = 2  # 采样宽度2bytes
#     FILEPATH = 'new.wav'
#     pa = PyAudio()
#     stream = pa.open(format=paInt16, channels=channels,
#                      rate=framerate, input=True, frames_per_buffer=num_samples)
#     my_buf = []
#     # count = 0
#     t = time.time()
#     print('正在录音...')
#
#     while time.time() < t + 4:  # 秒
#         string_audio_data = stream.read(num_samples)
#         my_buf.append(string_audio_data)
#     print('录音结束.')
#     save_wave_file(FILEPATH, my_buf)
#     stream.close()

# def openbrowser(text):
#     maps = {
#         '百度': ['百度', 'baidu'],
#         '腾讯': ['腾讯', 'tengxun'],
#         '网易': ['网易', 'wangyi']
#
#     }
#     if text in maps['百度']:
#         webbrowser.open_new_tab('https://www.baidu.com')
#     elif text in maps['腾讯']:
#         webbrowser.open_new_tab('https://www.qq.com')
#     elif text in maps['网易']:
#         webbrowser.open_new_tab('https://www.163.com/')
#     else:
#         webbrowser.open_new_tab('https://www.baidu.com/s?wd=%s' % text)

# if __name__ == '__main__':
#     flag = 'y'
#     while flag.lower() == 'y':
#         print('请输入数字选择语言：')
#         # devpid = input('1536：普通话(简单英文),1537:普通话(有标点),1737:英语,1637:粤语,1837:四川话\n')
#         # my_record()
#         # speech = get_audio(FILEPATH)
#         print(result)
#         # if type(result) == str:
#         #     openbrowser(result.strip('，'))
#         flag = input('Continue?(y/n):')

# import speech_recognition as sr
#
# r = sr.Recognizer()
#
# test = sr.AudioFile('./test3.wav')
#
# with test as source:
#     audio = r.record(source)
#
# print(type(audio))
#
# print("Text:" + r.recognize_sphinx(audio, language='zh-CN'))
# print(r.recognize_google(audio, language='zh-CN', show_all=True))
