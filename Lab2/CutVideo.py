from moviepy.editor import *
import moviepy.config_defaults
import ffmpy


def hor_to_ver(input_video, output_ratio=(1080, 1920)):
    input_ratio = input_video.size
    ori_width = int(input_ratio[1] * output_ratio[0] / output_ratio[1])
    x1 = int(input_ratio[0] / 2 - ori_width / 2)
    x2 = x1 + ori_width
    bg_video = input_video.crop(x1=x1, y1=0, x2=x2, y2=input_ratio[1]).resize(output_ratio)
    bg_file = "./movie/tmp/bg.mp4"
    bg_video.write_videofile(bg_file)
    bg_blur_file = "./movie/tmp/bg_blur.mp4"
    ff = ffmpy.FFmpeg(              # 原音频不是采样率为16000Hz的，必须转换为16000Hz
        # executable="./lib/ffmpeg-master-latest-win64-lgpl-shared/bin/ffmpeg.exe",
        inputs={bg_file: None},
        outputs={bg_blur_file: '-filter_complex "boxblur=20:1:cr=0:ar=0" -y'}
    )
    print(ff.cmd)
    ff.run()
    bg_blur_video = VideoFileClip(bg_blur_file)
    input_video = input_video.resize(width=output_ratio[0]).set_pos("center")
    return CompositeVideoClip([bg_blur_video, input_video])


def add_caption(input_video, captions):
    print(captions)
    seg_dur = input_video.duration / len(captions)
    start = 0
    txt_list = list()
    for cap in captions:
        txt = (TextClip(cap, fontsize=150, font='SimHei', size=(300, 150),
                        align='center', color='black', bg_color="yellow")
               .set_position(lambda t: ("center", 1400 + t))
               .set_duration(seg_dur).set_start(start))
        txt_list.append(txt)
        start += seg_dur
    video = CompositeVideoClip([input_video, *txt_list])
    return video


# def cut_video(time_stamps, captions, output_video_path, input_video_path=None, input_video=None, add_caption=False):
def cut_video(input_video, time_stamps, captions, add_caption=False):
    '''
        time_stamps: list of tuples, each tuple indicates the start and the end time(second)
        captions: list of str, same length with time_stamps
    '''
    # if input_video is None:
    #     input_video = VideoFileClip(input_video_path)
    if add_caption:
        txt_list = []
        for ts, c in zip(time_stamps, captions):
            start, end = ts

            print(int(input_video.size[1] / 8))
            txt = (TextClip(c, fontsize=int(input_video.size[1] / 8),
                            font='SimHei', size=(input_video.size[0], int(input_video.size[1] / 8)),
                            align='center', color='white')
                 .set_position((0.0, 0.8), relative=True)
                 .set_duration(end - start).set_start(start))

            txt_list.append(txt)

        video = CompositeVideoClip([input_video, *txt_list])
    else:
        video = input_video
    # video = video.set_audio(AudioFileClip(input_video_path))

    video_list = []
    for ts in time_stamps:
        start, end = ts
        clip = video.subclip(start, end)
        video_list.append(clip)
    final_clip = concatenate_videoclips(video_list)

    # final_clip.write_videofile(output_video_path)
    return final_clip


if __name__ == "__main__":
    time_stamps = [(0, 3), (4, 6), (10, 15)]
    captions = ['我不到啊', '嗒嗒嗒嘀嗒嗒', '这里测试一下长度很长很长很长很长的字幕会发生什么事情']
    input_video_path = "./shenyang.mp4"
    output_video_path = "./cut.mp4"
    cut_video(time_stamps, captions, input_video_path, output_video_path, add_caption=True)