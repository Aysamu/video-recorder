import wave
import threading
from os import remove
from datetime import datetime
import pyaudio
from PIL import ImageGrab
from numpy import array
import cv2
from moviepy.editor import *
import globalvar as gl


CHUNK_sIZE = 128
CHANNELS = 2
FORMAT = pyaudio.paInt16
RATE = 48000


class recorder:
    def __init__(self):
        path = gl.get_value('path')
        self.now = str(datetime.now())[:19].replace(':', '_')
        self.audio_filename = path + "%s.mp3" % self.now
        self.screen_video_filename = path + "%s_video.avi" % self.now
        self.video_filename = path + "%s.avi" % self.now
        self.allowRecording = True

    def record_audio(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        # input_device_index=4,  # 立体混音，具体选哪个根据需要选择
                        frames_per_buffer=CHUNK_sIZE)
        wf = wave.open(self.audio_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        while self.allowRecording:
            # 从录音设备读取数据，直接写入wav文件
            data = stream.read(CHUNK_sIZE)
            wf.writeframes(data)
        wf.close()
        stream.stop_stream()
        stream.close()
        p.terminate()

    def record_screen(self):
        # 录制屏幕
        im = ImageGrab.grab()
        video = cv2.VideoWriter(self.screen_video_filename,
                                cv2.VideoWriter_fourcc(*'XVID'),
                                25, im.size)  # 帧速和视频宽度、高度
        while self.allowRecording:
            im = ImageGrab.grab()
            im = cv2.cvtColor(array(im), cv2.COLOR_RGB2BGR)
            video.write(im)
        video.release()

    def run(self):
        # 创建两个线程，分别录音和录屏
        self.t1 = threading.Thread(target=self.record_audio)
        self.t2 = threading.Thread(target=self.record_screen)

        for t in (self.t1, self.t2):
            t.start()

        print('开始录制')

    def stop(self):
        self.allowRecording = False
        for t in (self.t1, self.t2):
            t.join()
        print('结束录制')
        # 把录制的视频和音频合成视频文件
        audio = AudioFileClip(self.audio_filename)
        video = VideoFileClip(self.screen_video_filename)
        tatlevideo = video.set_audio(audio)
        tatlevideo.write_videofile(self.video_filename, codec='libx264', fps=25)
        remove(self.audio_filename)
        remove(self.screen_video_filename)
        self.__init__()