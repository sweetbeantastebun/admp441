#coding:utf-8
"""
マイクから録音、オーディオファイルを読み込み
短時間フーリエ変換(stft)を変数で実行
"""
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import numpy as np #行列、配列計算、FFT化するライブラリ
from scipy import signal  #信号処理や統計を使用するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
from threading import Thread  #スレッド処理するライブラリ
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed  #複数の処理を並列実行するためのライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
import pandas as  pd  #数式、配列を操作するライブラリ
import psutil  #メモリ、CPUの使用率をモニターするライブラリ

#グラフのリアルタイムプロットの更新時間数
Loop_count_Value1 = 29
Loop_count_Value2 = 60
#しきい値を指定
threshold_value_MAX = 0.017
threshold_value_MIN = 0.009
#FFT検出強度のフィルタリング
noise_reduction_filters = 0


t00 = time.time()
#ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
path_A1 = "/home/pi/Documents/admp441_data_A/"  
path_A2 = "/home/pi/Documents/admp441_data_A/Save_wavfile"
path_B1 = "/home/pi/Documents/admp441_data_B/"  
path_B2 = "/home/pi/Documents/admp441_data_B/Save_wavfile"


def Recording_A():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = timestamp.strftime("%Y%m%d%H%M%S")
    #録音実行（16ビット量子化、44.1kHz）
    record = "arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data_A/"+filename_A+".wav"
    subprocess.call(record, shell=True)
    t1 = time.time()
    #wavファイルの読み込み
    global t2
    global t3
    global t4
    global t5
    global wavfile_A
    global fs_A
    global audio_signal_A
    global rms_A
    global samples
    t2 = time.time()
    wavfile_A = path_A1 + filename_A + ".wav"
    wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs_A = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
    t3 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_A = samples.copy()
    """RMS"""
    rms_A = np.sqrt((audio_signal_A**2).mean())
    if rms_A is np.nan:
        rms_A == 0.001
    #print("RMS", round(rms_A,4))
    t5 = time.time()
    #print("Recording_A", t5-t0)

        
def Graph_A():
    global t10
    global t19
    global RMS_data
    global sample_of_numbers
    t10 = time.time()
    #RMS値と測定回数をリストに格納する
    RMS_data.append(round(rms_A,4))
    RMS_data.pop(0)
    sample_of_numbers.append(index_loop)
    sample_of_numbers.pop(0)
    """FFT"""
    N = 8192  #サンプル数を指定 #周波数分解能は#データ数8192=5Hz
    spectrum_A = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_A = np.fft.fftfreq(N, 1.0/fs_A)  #周波数軸の計算
    #グラフ準備
    spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除   
    #dB
    abs_spectrum_A = np.abs(spectrum_A)
    spectrum_dB_A = 20 * np.log10(abs_spectrum_A / 2e-5)
    #フィルタリング機能
    spectrum_dB_A[(spectrum_dB_A < noise_reduction_filters)] = 0  #しきい値未満の振幅はゼロにする
    """graph"""
    #グラフ作成
    plt.ion()
    plt.clf()
    plt.cla()
    plt.subplot(2, 1, 1)
    No1, = plt.plot(sample_of_numbers, RMS_data, lw=1)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    No1.set_data(sample_of_numbers, RMS_data)
    plt.xlim(sample_of_numbers[-Loop_count_Value1], sample_of_numbers[-1])
    #plt.ylim(0, 0.03)
    plt.subplot(2, 1, 2)
    plt.plot(frequency_A, spectrum_dB_A, lw=1)
    plt.axis([0,fs_A/2, 0,160])
    plt.grid(which="both")
    plt.xlabel("Frequency[Hz]", fontsize= 8)
    plt.ylabel("SPL[dB]", fontsize= 8)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.draw()
    plt.pause(0.01) 
    t11 = time.time()
    #wavファイル削除
    file = filename_A + ".wav"
    os.remove(path_A1 + file)
    t19 = time.time()
    #print("Greph_A", t19-t10)


def Recording_B():
    global t20
    global t21
    t20 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_B
    timestamp = datetime.today()
    filename_B = timestamp.strftime("%Y%m%d%H%M%S")
    #録音実行（16ビット量子化、44.1kHz）
    record = "arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data_B/"+filename_B+".wav"
    subprocess.call(record, shell=True)
    t21 = time.time()
    #wavファイルの読み込み
    global t22
    global t23
    global t24
    global t25
    global t26
    global wavfile_B
    global fs_B
    global audio_signal_B
    global rms_B
    global samples
    t22 = time.time()
    wavfile_B = path_B1 + filename_B + ".wav"
    wr = wave.open(wavfile_B, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs_B = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
    t23 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_B = samples.copy()
    """RMS"""
    rms_B = np.sqrt((audio_signal_B**2).mean())
    if rms_B is np.nan:
        rms_B == 0.001
    #print("RMS", round(rms_B,4))
    t25 = time.time()
    #print("Recording_B", t25-t20)
        
        
def Graph_B():
    global t30
    global t39
    global RMS_data
    global sample_of_numbers
    t30 = time.time()
    #RMS値と測定回数をリストに格納する
    RMS_data.append(round(rms_B,4))
    RMS_data.pop(0)
    sample_of_numbers.append(index_loop)
    sample_of_numbers.pop(0)
    """FFT"""
    N = 8192  #サンプル数を指定 #周波数分解能は8192=5Hz
    spectrum_B = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_B = np.fft.fftfreq(N, 1.0/fs_B)  #周波数軸の計算
    #グラフ準備
    spectrum_B = spectrum_B[:int(spectrum_B.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_B = frequency_B[:int(frequency_B.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除    
    #dB
    abs_spectrum_B = np.abs(spectrum_B)
    spectrum_dB_B = 20 * np.log10(abs_spectrum_B / 2e-5)
    #フィルタリング機能
    spectrum_dB_B[(spectrum_dB_B < noise_reduction_filters)] = 0  #しきい値未満の振幅はゼロにする
    """graph"""
    #グラフ作成
    plt.ion()
    plt.clf()
    plt.cla()
    plt.subplot(2, 1, 1)
    No1, = plt.plot(sample_of_numbers, RMS_data, lw=1)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    No1.set_data(sample_of_numbers, RMS_data)
    plt.xlim(sample_of_numbers[-Loop_count_Value1], sample_of_numbers[-1])
    #plt.ylim(0, 0.03)
    plt.subplot(2, 1, 2)
    plt.plot(frequency_B, spectrum_dB_B, lw=1)
    plt.axis([0,fs_B/2, 0,160])
    plt.grid(which="both")
    plt.xlabel("Frequency[Hz]", fontsize= 8)
    plt.ylabel("SPL[dB]", fontsize= 8)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.draw()
    plt.pause(0.01) 
    t37 = time.time()
    #wavファイル削除
    file = filename_B + ".wav"
    os.remove(path_B1 + file)
    t39 = time.time()
    #print("Greph_B", t39-t30)
    
    
def job_A():
    t40 = time.time()
    plt.clf()
    No1, = plt.plot(sample_of_numbers, RMS_data, lw=1)
    plt.xlim(sample_of_numbers[-Loop_count_Value2], sample_of_numbers[-1])
    plt.ylim(0, 0.05)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    No1.set_data(sample_of_numbers, RMS_data)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.savefig("/home/pi/Documents/admp441_data/"+filename_A+"cron"".png")
    plt.close()
    #csv作成、出力
    header_names = ["SampleNo.","RMS"]
    Data_List = {"SampleNo.":sample_of_numbers, "RMS":RMS_data}
    df = pd.DataFrame(Data_List) 
    df = df.round({"RMS":4})
    df.to_csv("/home/pi/Documents/admp441_data/"+filename_A+"cron"+".csv")
    Data_List2 = {filename_A : RMS_data}
    Layout = pd.DataFrame(Data_List2)
    aggregate = Layout.describe()
    aggregate = aggregate.round(4)
    aggregate.to_csv("/home/pi/Documents/admp441_data/"+filename_A+"AGR"+".csv")
    """
    #録音実行（16ビット量子化、44.1kHz）
    record = "arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/"+filename_A+".wav"
    subprocess.call(record, shell=True)
    """

    
sample_of_numbers = []
RMS_data = []
index_loop = 1
while index_loop <= Loop_count_Value2:
    Recording_A()
    RMS_data.append(rms_A)
    sample_of_numbers.append(index_loop)
    #wavファイル削除
    file_A = filename_A + ".wav"
    os.remove(path_A1 + file_A)
    index_loop += 1
    Recording_B()
    RMS_data.append(rms_B)
    sample_of_numbers.append(index_loop)
    #wavファイル削除
    file_B = filename_B + ".wav"
    os.remove(path_B1 + file_B)
    index_loop += 1
 
Recording_A()
#ここから無限ループ。
#並列処理でレコード中に音声解析(FFT)を実行する。
#タスクを4つ(recording_AとB、FFT_AとB)作成し、
#recording_BとFFT_Aの組み合わせ(recording_B実行中にFFT_Aを処理)
#recording_AとFFT_Bの組み合わせ(recording_A実行中にFFT_Bを処理)
#で処理していく。
index_loop = Loop_count_Value1 + 1
while True:
    t100 = time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    result_B = executor.submit(Recording_B()) #recording_Bを実行し、これを変数result_Bとしておく
    executor.submit(Graph_A()) #FFT_Aを実行する(上記と平行)
    as_completed([result_B]).__next__() #変数result_Bが終了したら、次に進む
    index_loop += 1
    t102 = time.time()
    result_A = executor.submit(Recording_A()) #recording_Aを実行し、これを変数result_Aとしておく
    executor.submit(Graph_B()) #FFT_Bを実行する(上記と平行)
    as_completed([result_A]).__next__() #変数result_Aが終了したら、次に進む
    index_loop += 1
    t104 = time.time()
    
    #定期実行処理
    if index_loop % Loop_count_Value2 == 0:
        job_A()
    """
    print('thread_1',t102-t100)
    print('thread_2',t104-t102)
    print('Record_A',t5-t0)
    print('Record_B',t25-t20)
    print('Graph_A',t19-t10)
    print('Graph_B',t39-t30)
    """
    """
    #memory使用率を出力
    memory = psutil.virtual_memory()
    print('memory.percent',memory.percent)
    #cpu使用率を出力
    cpu = psutil.cpu_percent(interval=1)
    print('cpu',cpu)
    #diskの容量を出力
    disk = psutil.disk_usage('/')
    print('disk.percent',disk.percent)                    
    """
