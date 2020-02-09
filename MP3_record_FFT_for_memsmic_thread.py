# coding: utf-8
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  #グラフ化ライブラリ
from pydub import AudioSegment  #メディアデータの変換ライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
from threading import Thread
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed

t00 = time.time()

#ファイルの名前をタイムスタンプ化する
#def timestamp():
#    timestamp = datetime.today()
#    filename = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)

def recording():
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename
    timestamp = datetime.today()
    filename = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)
            
    #録音実行（16ビット、44.1kHz、2秒）
    record = 'arecord -d 2 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename+'.wav'
    subprocess.call(record, shell=True)
    t1 = time.time()

    #MP3に圧縮             
    mpeg = 'lame -V 2 /home/pi/Documents/admp441_data/'+filename+'.wav ''/home/pi/Documents/admp441_data/'+filename+'.mp3'
    subprocess.call(mpeg, shell=True)
    t2 = time.time()
    print('t1-t0',t1-t0)
    print('t2-t1',t2-t1)


def FFT():
    #mp3の読み込み
    t3 = time.time()
    mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+filename+'.mp3', format='mp3')
    samples = np.array(mp3_version.get_array_of_samples())
    #スペクトルをプロット表示
    spec = np.fft.fft(samples)
    freq = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
    t4 = time.time()

    #グラフ作成
    fig = plt.figure(figsize=(10,10),dpi=200)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(freq, np.abs(spec))
    plt.axis([0,mp3_version.frame_rate/2,0,10000000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)

    ax2 = fig.add_subplot(2, 2, 3)
    plt.plot(freq, np.abs(spec))
    plt.xlim(0, 1000)
    plt.ylim(0, 10000000)
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)

    ax3 = fig.add_subplot(2, 2, 4)
    plt.plot(freq, np.abs(spec))
    plt.xlim(0, 10000)
    plt.ylim(0, 10000000)
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.show()
    t5 = time.time()
    plt.savefig('/home/pi/Documents/admp441_data/'+filename+'.png')
    print('/home/pi/Documents/admp441_data/'+filename+'.png', 'saved')
    t6 = time.time()
    #print('t3-t2',t3-t2)
    print('t4-t3',t4-t3)
    print('t5-t4',t5-t4)
    print('t6-t5',t6-t5)

#timestamp()
#recording()
#FFT()

index_loop = 1
while True:
    t7=time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    result = executor.submit(recording) #recordingを実行し、これを変数resultとしておく
    executor.submit(FFT) #FFTを実行する(上記と平行)
    as_completed([result]).__next__() #変数resultが終了したら、次に進む
    t8 = time.time()
    print('t8-t7',t8-t7)
    index_loop += 1

#print('t8-t7',t8-t7)

#except KeyboardInterrupt:
#    print('!!FINISH!!')
