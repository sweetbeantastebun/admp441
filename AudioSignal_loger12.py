# coding: utf-8
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
from threading import Thread  #スレッド処理するライブラリ
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed  #複数の処理を並列実行するためのライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
import pandas as  pd
import psutil  #メモリ、CPUの使用率をモニターするライブラリ

#グラフのリアルタイムプロットの更新時間数
Loop_count_Value = 330

t00 = time.time()
path = '/home/pi/Documents/admp441_data/'  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
path2 ='/home/pi/Documents/admp441_data/Save_wavfile'

def Recording_A():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "." + str(timestamp.microsecond)
    #録音実行（16ビット量子化、44.1kHz）
    record = 'arecord -d 2 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_A+'.wav'
    subprocess.call(record, shell=True)
    t1 = time.time()
    #wavファイルの読み込み
    global t2
    global t3
    global t4
    global t5
    global t6
    global wavfile_A
    global fs_A
    global audio_signal_A
    global rms_A
    global spectrum_A
    global frequency_A
    t2 = time.time()
    wavfile_A = path + filename_A + '.wav'
    wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs_A = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    samples = np.frombuffer(samples, dtype="int16")  / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
    t3 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_A = samples.copy()
    #RMS
    rms_A = np.sqrt((audio_signal_A**2).mean())
    print('RMS', rms_A)
    t4= time.time()
    #FFT
    N = 8192  #サンプル数を指定 #録音10秒で4096データの周波数分解能は10Hz #8192=5Hz
    spectrum_A = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_A = np.fft.fftfreq(N, 1.0/fs_A)  #周波数軸の計算
    #spectrum_A = np.fft.fft(samples)  #2次元配列(実部，虚部)
    #frequency_A = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算
    #グラフ準備
    spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除    
    t5 = time.time()
    #print("Recording_A", t5-t0)

def Graph_A1():
    global fig1
    global fig2
    global fig3
    global t10
    global t19
    t10 = time.time()
    #グラフ作成
    plt.ion()
    plt.clf()
    fig1 = plt.figure(1)
    plt.cla()
    plt.subplot(2, 1, 1)
    No1, = plt.plot(np.arange(0, index_loop), RMS_data, lw=1)
    plt.xlim(np.arange(0, index_loop)[-Loop_count_Value], np.arange(0, index_loop)[-1])
    plt.ylim(0, 0.12)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    RMS_data.append(rms_A)
    RMS_data.pop(0)
    No1.set_data(np.arange(0, index_loop), RMS_data)
    plt.subplot(2, 1, 2)
    plt.plot(frequency_A, np.abs(spectrum_A), lw=1)
    plt.axis([0,1600, 0,50])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.draw()
    plt.pause(0.01) 
    t18 = time.time()
    if rms_A >= 0.044:
        fig1.savefig('/home/pi/Documents/admp441_data/'+filename_A+'fig1''.png')
        file =  filename_A + '.wav'
        shutil.copy(path + file , path2)
    t19 = time.time()
    print("Greph_A", t19-t10)


def job():
    plt.clf()
    plt.subplot(2, 1, 1)
    No1, = plt.plot(np.arange(0, index_loop), RMS_data, lw=1)
    plt.xlim(np.arange(0, index_loop)[-Loop_count_Value], np.arange(0, index_loop)[-1])
    plt.ylim(0, 0.12)
    #plt.plot(np.arange(0, index_loop), RMS_data, lw=1)
    #plt.axis([0,index_loop, 0,0.12])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    RMS_data.append(rms_A)
    RMS_data.pop(0)
    No1.set_data(np.arange(0, index_loop), RMS_data)
    plt.subplot(2, 1, 2)
    plt.plot(frequency_A, np.abs(spectrum_A), lw=1)
    plt.axis([0,1600, 0,50])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.savefig('/home/pi/Documents/admp441_data/'+filename_A+'.png')
    plt.close()
    #波形の個数を数値化
    data_frame = pd.DataFrame(np.abs(spectrum_A), columns=["spectrum"])  #データフレーム作成
    peeks = (data_frame["spectrum"] >= 0.005).sum()  #0.085以上の検出ピークをカウント
    #memory,cpu,harddiskの使用率をモニタ
    memory = psutil.virtual_memory()  #memory使用率の出力
    cpu = psutil.cpu_percent(interval = 1)  #cpu使用率を出力
    disk = psutil.disk_usage("/")  #disk容量を出力
    #csvファイルに書き込むフレーム作成
    header_names = [["number_of_peeks",  "memory.percent", "cpu", "disk.percent"],
    [peeks, memory.percent, cpu, disk.percent]]
     #csv作成
    with open("/home/pi/Documents/admp441_data/"+filename_A+"peeks"+".csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(header_names)
    """
    #wavファイル削除
    #file = filename_A + '.wav'
    #os.remove(path + file)
    file_list = glob.glob(path + "*.wav")
    for file in file_list:
        os.remove(file)
    #print(path + file, 'deleted')
    """


RMS_data = []
index_loop = 1
while index_loop <= Loop_count_Value:
    Recording_A()
    RMS_data.append(rms_A)
    #wavファイル削除
    file = filename_A + '.wav'
    os.remove(path + file)
    index_loop += 1

index_loop = Loop_count_Value + 1
while True:
    Recording_A()
    RMS_data.append(rms_A)
    Graph_A1()
    if index_loop % Loop_count_Value == 0:
        job()
    #wavファイル削除
    file = filename_A + '.wav'
    os.remove(path + file)
    index_loop += 1

"""
index_loop = Loop_count_Value
while True:
    t50=time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    result_B = executor.submit(Recording_B()) #recording_Bを実行し、これを変数result_Bとしておく
    executor.submit(Graph_A1()) #Graph_Aを実行する(上記と平行)
    as_completed([result_B]).__next__() #変数result_Bが終了したら、次に進む
    RMS_data.append(rms_B)
    t51 = time.time()
    index_loop += 1
    result_A = executor.submit(Recording_A()) #recording_Aを実行し、これを変数result_Aとしておく
    executor.submit(Graph_B1()) #Graph_Bを実行する(上記と平行)
    as_completed([result_A]).__next__() #変数result_Aが終了したら、次に進む
    RMS_data.append(rms_A)
    #if i % 10 == 0:
    #    job()
    t52 = time.time()
    index_loop += 1
    #print('thread_1',t51-t50)
    #print('thread_2',t52-t51)
    
"""
#except KeyboardInterrupt:
#print("FINISH!")
