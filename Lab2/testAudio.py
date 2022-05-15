import speech_recognition as sr

r = sr.Recognizer()

test = sr.AudioFile('./test3.wav')

with test as source:
    audio = r.record(source)

print(type(audio))

print("Text:" + r.recognize_sphinx(audio, language='zh-CN'))
# print(r.recognize_google(audio, language='zh-CN', show_all=True))
