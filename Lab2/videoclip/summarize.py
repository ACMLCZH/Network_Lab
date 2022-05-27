import pysrt
from datetime import datetime
from textrank4zh import TextRank4Sentence
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tqdm import tqdm
import os

class sentence:
    def __init__(self, start, end, text):
        self.text = text
        self.starttime = datetime.strptime(str(start), '%H:%M:%S,%f')
        self.endtime = datetime.strptime(str(end), '%H:%M:%S,%f')
        self.duration = (self.endtime - self.starttime).total_seconds()

def td2str(td):
    sec = td.seconds
    return '{:0>2d}:{:0>2d}:{:0>2d}.{:0>6d}'.format(sec // 3600, (sec % 3600) // 60, sec % 60, td.microseconds)

def readsrtfile(srtfilenm):
    srt = pysrt.open(srtfilenm)
    passage = str()
    textls = []
    for line in srt.data:
        passage += (line.text + '\n')
        textls.append(sentence(line.start, line.end, line.text))
    return passage, textls

def summarize(passage, textls, maxsentences=600, maxduration=600):
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=passage, lower=True, source='all_filters')
    sentencecnt = 0
    timecnt = float()
    for line in tr4s.key_sentences:
        if timecnt + textls[line['index']].duration > maxduration:
            break
        if sentencecnt == maxsentences:
            break
        timecnt += textls[line['index']].duration
        sentencecnt += 1
    print('%d sentences are selected, %.3f seconds in total.' % (sentencecnt, timecnt))
    resultls = []
    for item in tr4s.get_key_sentences(num=sentencecnt):
        resultls.append(item.index)
    resultls.sort()
    return resultls

def clipvideo_moviepy(clipconfls, srcfilenm, dstfilenm):
    clipls = []
    print('1. Load data...')
    video = VideoFileClip(srcfilenm)
    print('2. Cut videoclips...')
    for clipconf in tqdm(clipconfls):
        clipls.append(video.subclip(
            clipconf.starttime.strftime('%H:%M:%S.%f'), 
            clipconf.endtime.strftime('%H:%M:%S.%f')))
    print('3. Concatenate videoclips...')
    final_clip = concatenate_videoclips(clipls)
    print('4. Write result...')
    final_clip.write_videofile(dstfilenm)

def clipvideo_ffmpeg(clipconfls, srcfilenm, dstfilenm):
    clipnmls = []
    srcfilenm_1 = srcfilenm.split('/')[-1]
    print('1. Cut videoclips...')
    for i, clipconf in tqdm(enumerate(clipconfls)):
        clipnm = 'tmp.nosync/{}_subclip{}.mp4'.format(srcfilenm_1, i)
        clipnm_1 = '{}_subclip{}.mp4'.format(srcfilenm_1, i)
        starttime = clipconf.starttime.strftime('%H:%M:%S.%f')
        duration = td2str(clipconf.endtime - clipconf.starttime)
        os.system('ffmpeg -ss %s -t %s -i %s -vcodec copy -acodec copy %s -loglevel quiet' % (starttime, duration, srcfilenm, clipnm))
        clipnmls.append('file \'{}\'\n'.format(clipnm_1))
    print('2. Generate ffmpeg configuration file...')
    conffilenm = 'tmp.nosync/{}_config.txt'.format(srcfilenm_1)
    with open(conffilenm, 'w') as outfile:
        outfile.writelines(clipnmls)
    print('3. Concatenate videoclips...')
    os.system('ffmpeg -f concat -i {} -c copy {} -loglevel quiet'.format(conffilenm, dstfilenm))
    print('4. Remove temporaries...')
    os.system('rm tmp.nosync/*')

def slicetextls(textls, indexls):
    ls = []
    for i in indexls:
        ls.append(textls[i])
    return ls

if __name__ == '__main__':
    passage, textls = readsrtfile('srt.nosync/name.srt')
    resultls = summarize(passage, textls, maxduration=120)  #限制裁剪出的视频时间(s)
    ls = slicetextls(textls, resultls)
    clipvideo_moviepy(ls, 'video.nosync/name.mp4', 'result.nosync/name.mp4')
    #clipvideo_ffmpeg(ls, 'video.nosync/reset02.mp4', 'result.nosync/reset02_cut.mp4')