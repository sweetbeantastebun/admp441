# coding: utf-8
"""
録音、オーディオファイル読み込んでFFT処理
Threadで並列処理
"""
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
import psutil  #Hardware情報（CPU,memory使用率）を確認するライブラリ

t00 = time.time()
path = '/home/pi/Documents/admp441_data/'  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)

def Recording_A():
    global t0
    global t1
    t0 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_A
    timestamp = datetime.today()
    filename_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + ":" + str(timestamp.minute) + ":" + str(timestamp.second)
    #録音実行（16ビット量子化、44.1kHz）
    record = 'arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_A+'.wav'
    subprocess.call(record, shell=True)
    t1 = time.time()

def FFT_A():
    global t2
    global t3
    global t7
    global wavfile_A
    t2 = time.time()
    #wavファイルの読み込み
    wavfile_A = path + filename_A+'.wav'
    wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    t3 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_A = samples.copy()
    #RMS
    rms_A = np.sqrt((audio_signal_A**2).mean())
    print("RMS", round(rms_A,4))
    #FFT1
    N = 32768  #周波数分解能は2.5Hz(N=32768)
    spectrum_A1 = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_A1 = np.fft.fftfreq(N, 1.0/fs)  #周波数軸の計算
    #spectrum_A1 = np.fft.fft(samples)  #2次元配列(実部，虚部)
    #frequency_A1 = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算
    #FFT2
    N = 8192  #周波数分解能は5Hz(N=8192)
    spectrum_A2 = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_A2 = np.fft.fftfreq(N, 1.0/fs)  #周波数軸の計算
    #グラフ作成準備
    spectrum_A1 = spectrum_A1[:int(spectrum_A1.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    spectrum_A2 = spectrum_A2[:int(spectrum_A2.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_A1 = frequency_A1[:int(frequency_A1.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除
    frequency_A2 = frequency_A2[:int(frequency_A2.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除
    #dB
    abs_spectrum_A = np.abs(spectrum_A1)
    spectrum_dB_A = 20 * np.log10(abs_spectrum_A / 2e-5)
    #t5 = time.time()
    #グラフ作成
    plt.ion()
    plt.clf()
    plt.subplot(2, 1, 1)
    plt.plot(frequency_A1, spectrum_dB_A)
    plt.axis([0,fs/2,0,160])
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("SPL(dB)", fontsize=8)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.subplot(2, 1, 2)
    plt.plot(frequency_A2, np.abs(spectrum_A2))
    plt.xlim(0, 1000)
    plt.ylim(0, 100)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum(Pa)", fontsize=8)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.draw()
    plt.pause(0.01)

    #np.savetxt(path +filename_A+'spectrum', np.abs(spectrum_A), delimiter = " ", fmt='%.2f')
    #np.savetxt(path +filename_A+'frequency', frequency_A, delimiter = " ", fmt='%.2f')
    
    #wavファイル削除
    file = filename_A + '.wav'
    os.remove(path + file)
    #print(path + file, 'deleted')
    t7 = time.time()

def Recording_B():
    global t8
    global t9
    t8 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_B
    timestamp = datetime.today()
    filename_B = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + ":" + str(timestamp.minute) + ":" + str(timestamp.second)
    #録音実行（16ビット量子化、44.1kHz)
    record = 'arecord -d 1 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_B+'.wav'
    subprocess.call(record, shell=True)
    t9 = time.time()

def FFT_B():
    global t10
    global t11
    global t14
    global wavfile_B
    t10 = time.time()
    #wavファイルの読み込み
    wavfile_B = path + filename_B+'.wav'
    wr = wave.open(wavfile_B, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    t11 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_B = samples.copy()
    #RMS
    rms_B = np.sqrt((audio_signal_B**2).mean())
    print("RMS", round(rms_B,4))
    #FFT1
    N = 32768  ##周波数分解能は2.5Hz(N=32768)
    spectrum_B1 = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_B1 = np.fft.fftfreq(N, 1.0/fs)  #周波数軸の計算
    #spectrum_B1 = np.fft.fft(samples)  #2次元配列(実部，虚部)
    #frequency_B1 = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算
    #FFT2
    N = 8192  ##周波数分解能は5Hz(N=8192)
    spectrum_B2 = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_B2 = np.fft.fftfreq(N, 1.0/fs)  #周波数軸の計算
    #グラフ作成準備
    spectrum_B1 = spectrum_B1[:int(spectrum_B1.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    spectrum_B2 = spectrum_B2[:int(spectrum_B2.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_B1 = frequency_B1[:int(frequency_B1.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除
    frequency_B2 = frequency_B2[:int(frequency_B2.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除
    #dB
    abs_spectrum_B = np.abs(spectrum_B1)
    spectrum_dB_B = 20 * np.log10(abs_spectrum_B / 2e-5)
    #t13 = time.time()
    
    #グラフ作成
    plt.ion()
    plt.clf()
    plt.subplot(2, 1, 1)
    plt.plot(frequency_B1, spectrum_dB_B)
    plt.axis([0,fs/2,0,160])
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("SPL(dB)", fontsize=8)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.subplot(2, 1, 2)
    plt.plot(frequency_B2, np.abs(spectrum_B2))
    plt.xlim(0, 1000)
    plt.ylim(0, 100)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum(Pa)", fontsize=8)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.draw()
    plt.pause(0.01)

    #np.savetxt(path +filename_B+'spectrum', np.abs(spectrum_B), delimiter = " ", fmt='%.2f')
    #np.savetxt(path +filename_B+'frequency', frequency_B, delimiter = " ", fmt='%.2f')
    
    #wavファイル削除
    file = filename_B + '.wav'
    os.remove(path + file)
    #print(path + file, 'deleted')
    t14 = time.time()

Recording_A()

#ここから無限ループ。
#並列処理でレコード中に音声解析(FFT)を実行する。
#タスクを4つ(Recording_AとB、FFT_AとB)作成し、
#Recording_BとFFT_Aの組み合わせ(Recording_B実行中にFFT_Aを処理)
#Recording_AとFFT_Bの組み合わせ(Recording_A実行中にFFT_Bを処理)
#で処理していく。

while True:
    t16=time.time()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    result_B = executor.submit(Recording_B())  #Recording_Bを実行し、これを変数result_Bとしておく
    executor.submit(FFT_A())  #FFT_Aを実行する(上記と平行)
    as_completed([result_B]).__next__()  #変数result_Bが終了したら、次に進む
    t17 = time.time()
    result_A = executor.submit(Recording_A())  #Recording_Aを実行し、これを変数result_Aとしておく
    executor.submit(FFT_B())  #FFT_Bを実行する(上記と平行)
    as_completed([result_A]).__next__()  #変数result_Aが終了したら、次に進む
    t18 = time.time()
    """
    #print('thread_1',t17-t16)
    #print('thread_2',t18-t17)
    #print('record_A',t1-t0)
    #print('record_B',t9-t8)
    #print('FFT_A',t7-t2)
    #print('FFT_B',t14-t10)
    """
    """
    #memory使用率を出力
    #memory = psutil.virtual_memory()
    #print('memory.percent',memory.percent)
    #cpu使用率を出力
    #cpu = psutil.cpu_percent(interval=1)
    #print('cpu',cpu)
    #diskの容量を出力
    #disk = psutil.disk_usage('/')
    #print('disk.percent',disk.percent)
    """
#except KeyboardInterrupt:
#    print('!!FINISH!!')
