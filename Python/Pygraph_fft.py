from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys

import pyaudio
import struct

# betata=np.array(0)

class PlotWindow:
    def __init__(self):
        #マイクインプット設定
        # global bedata
        # bedata=np.zeros(4096)
        self.CHUNK=1024            #1度に読み取る音声のデータ幅
        self.RATE=44100             #サンプリング周波数
        self.update_seconds=5      #更新時間[ms]
        self.audio=pyaudio.PyAudio()
        self.stream=self.audio.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

        #音声データの格納場所(プロットデータ)
        self.data=np.zeros(self.CHUNK)
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)

        #プロット初期設定
        self.win=pg.GraphicsWindow()
        self.win.setWindowTitle("SpectrumAnalyzer")
        self.plt=self.win.addPlot() #プロットのビジュアル関係
        self.plt.setYRange(0,100)    #y軸の制限

        #アップデート時間設定
        self.timer=QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_seconds)    #10msごとにupdateを呼び出し

    def update(self):
        self.data=np.append(self.data,self.AudioInput())
        if len(self.data)/1024 > 10:
            self.data=self.data[1024:]
        self.fft_data=self.FFT_AMP(self.data)
        self.axis=np.fft.fftfreq(len(self.data), d=1.0/self.RATE)
        self.plt.plot(x=self.axis, y=self.fft_data, clear=True, pen="y")  #symbol="o", symbolPen="y", symbolBrush="b")

    def AudioInput(self):
        ret=self.stream.read(self.CHUNK)    #音声の読み取り(バイナリ) CHUNKが大きいとここで時間かかる
        #バイナリ → 数値(int16)に変換
        #32768.0=2^16で割ってるのは正規化(絶対値を1以下にすること)
        ret=np.frombuffer(ret, dtype="int16")/32768.0
        return ret

    # def BeforeData(self,data):
    #     self.be=bedata
        # self.bedata=data
    #     return self.be

    def FFT_AMP(self, data):
        # global bedata
        # print(type(bedata))
        data=np.hamming(len(data))*data
        data=np.fft.fft(data)
        data=np.abs(data)
        # print(type(data))
        # self.long=4000
        # if(data.size<4000):self.long=min([data.size,bedata.size])
        # print(self.long)
        print(np.abs(np.where(data[:4000]>100)))
        # bedata=data
        return data

if __name__=="__main__":
    plotwin=PlotWindow() 
    if (sys.flags.interactive!=1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()