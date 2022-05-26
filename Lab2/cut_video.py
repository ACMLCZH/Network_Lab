from moviepy.editor import *
import moviepy.config_defaults


def cut_video(time_stamps, captions, output_video_path, input_video_path=None, input_video=None, add_caption=False):
    '''
        time_stamps: list of tuples, each tuple indicates the start and the end time(second)
        captions: list of str, same length with time_stamps
    '''
    if input_video is None:
        input_video = VideoFileClip(input_video_path)
    if add_caption:
        txt_list = []
        for ts, c in zip(time_stamps, captions):
            start, end = ts

            txt = (TextClip(c, fontsize=40,
                            font='SimHei', size=(1900, 40),
                            align='center', color='white')
                 .set_position('bottom')
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

    final_clip.write_videofile(output_video_path)
    return 


if __name__ == "__main__":
    time_stamps = [(0, 3), (4, 6), (10, 15)]
    captions = ['我不到啊', '嗒嗒嗒嘀嗒嗒', '这里测试一下长度很长很长很长很长的字幕会发生什么事情']
    input_video_path = "./shenyang.mp4"
    output_video_path = "./cut.mp4"
    cut_video(time_stamps, captions, input_video_path, output_video_path, add_caption=True)