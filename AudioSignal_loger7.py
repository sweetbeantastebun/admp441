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
import schedule

#グラフのリアルタイムプロットの更新時間数
Loop_count_Value = 1800

t00 = time.time()
path = '/home/pi/Documents/admp441_data/'  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)

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
    #plt.subplot(2, 1, 1)
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
    
    fig2 = plt.figure(2)
    plt.cla()
    #plt.subplot(2, 1, 2)
    plt.plot(frequency_A, np.abs(spectrum_A), lw=1)
    plt.axis([0,fs_A/2, 0,100])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    
    fig3 = plt.figure(3)
    plt.cla()
    plt.subplot(2, 1, 1)
    plt.plot(frequency_A, np.abs(spectrum_A), lw=1)
    plt.axis([0,1600, 0,50])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.subplot(2, 2, 3)
    plt.plot(frequency_A, np.abs(spectrum_A), lw=1)
    plt.axis([1600,5000, 0,80])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.subplot(2, 2, 4)
    plt.plot(frequency_A, np.abs(spectrum_A), lw=1)
    plt.axis([5000,fs_A/2, 0,20])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間 
    plt.draw()
    plt.pause(0.01)
    t18 = time.time()
    if rms_A >= 0.087:
        fig1.savefig('/home/pi/Documents/admp441_data/'+filename_A+'fig1''.png')
        fig2.savefig('/home/pi/Documents/admp441_data/'+filename_A+'fig2''.png')
        fig3.savefig('/home/pi/Documents/admp441_data/'+filename_A+'fig3''.png')
        #データをテキストに出力
        np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'audio_signal', audio_signal_A, delimiter = " ", fmt='%.5f')
        #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'spectrum', np.abs(spectrum_A), delimiter = " ", fmt='%.5f')
        #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'frequency', frequency_A, delimiter = " ", fmt='%.2f') 
    #schedule.every(1).minutes.do(job_A) 
    #wavファイル削除
    file = filename_A + '.wav'
    os.remove(path + file)
    #print(path + file, 'deleted')
    t19 = time.time()
    print("Greph_A", t19-t10)

def Recording_B():
    global t20
    global t21
    t20 = time.time()
    #ファイルの名前をタイムスタンプ化する
    global filename_B
    timestamp = datetime.today()
    filename_B = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "." + str(timestamp.microsecond)
    #録音実行（16ビット量子化、44.1kHz）
    record = 'arecord -d 2 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename_B+'.wav'
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
    global spectrum_B
    global frequency_B
    t22 = time.time()
    wavfile_B = path + filename_B + '.wav'
    wr = wave.open(wavfile_B, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs_B = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    samples = np.frombuffer(samples, dtype="int16")  / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
    t23 = time.time()
    #samplesを変数audio_signalとしてコピー
    audio_signal_B = samples.copy()
    
    #RMS
    rms_B = np.sqrt((audio_signal_B**2).mean())
    print('RMS', rms_B)
    t24= time.time()
        
    #FFT
    N = 8192  #サンプル数を指定 #録音10秒で4096データの周波数分解能は10Hz #8192=5Hz
    spectrum_B = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_B = np.fft.fftfreq(N, 1.0/fs_B)  #周波数軸の計算
    #spectrum_B = np.fft.fft(samples)  #2次元配列(実部，虚部)
    #frequency_B = np.fft.fftfreq(samples.shape[0], 1.0/fs_B)  #周波数軸の計算
    #グラフ準備
    spectrum_B = spectrum_B[:int(spectrum_B.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_B = frequency_B[:int(frequency_B.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除    
    t25 = time.time()
    #print("Recording_B", t25-t20)

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
    RMS_data.append(rms_B)
    RMS_data.pop(0)
    No1.set_data(np.arange(0, index_loop), RMS_data)
    plt.subplot(2, 1, 2)
    plt.plot(frequency_B, np.abs(spectrum_B), lw=1)
    plt.axis([0,1600, 0,50])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.savefig('/home/pi/Documents/admp441_data/'+filename_B+'.png')
    plt.close()

def Graph_B1():
    global fig1
    global fig2
    global fig3
    global t30
    global t39
    t30 = time.time()
    #グラフ作成
    plt.ion()
    plt.clf()
    fig1 = plt.figure(1)
    plt.cla()
    #plt.subplot(2, 1, 1)
    No1, = plt.plot(np.arange(0, index_loop), RMS_data, lw=1)
    plt.xlim(np.arange(0, index_loop)[-Loop_count_Value], np.arange(0, index_loop)[-1])
    plt.ylim(0, 0.12)
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.xlabel("Sample Number", fontsize=8)
    plt.ylabel("RMS", fontsize=8)
    plt.grid(which="both")
    RMS_data.append(rms_B)
    RMS_data.pop(0)
    No1.set_data(np.arange(0, index_loop), RMS_data)

    fig2 = plt.figure(2)
    plt.cla()
    #plt.subplot(2, 1, 2)
    plt.plot(frequency_A, np.abs(spectrum_B), lw=1)
    plt.axis([0,fs_B/2, 0,100])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    
    fig3 = plt.figure(3)
    plt.cla()
    plt.subplot(2, 1, 1)
    plt.plot(frequency_B, np.abs(spectrum_B), lw=1)
    plt.axis([0,1600, 0,50])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.subplot(2, 2, 3)
    plt.plot(frequency_B, np.abs(spectrum_B), lw=1)
    plt.axis([1600,5000, 0,80])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間
    plt.subplot(2, 2, 4)
    plt.plot(frequency_B, np.abs(spectrum_B), lw=1)
    plt.axis([5000,fs_B/2, 0,20])
    plt.xticks(fontsize = 8)
    plt.yticks(fontsize = 8)
    plt.grid(which="both")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)  #隣接グラフとの隙間 
    plt.draw()
    plt.pause(0.01)
    t38 = time.time()
    if rms_B >= 0.087:
        fig1.savefig('/home/pi/Documents/admp441_data/'+filename_B+'fig1''.png')
        fig2.savefig('/home/pi/Documents/admp441_data/'+filename_B+'fig2''.png')
        fig3.savefig('/home/pi/Documents/admp441_data/'+filename_B+'fig3''.png')
        #データをテキストに出力
        np.savetxt('/home/pi/Documents/admp441_data/'+filename_B+'audio_signal', audio_signal_B, delimiter = " ", fmt='%.5f')
        #np.savetxt('/home/pi/Documents/admp441_data/'+filename_B+'spectrum', np.abs(spectrum_B), delimiter = " ", fmt='%.5f')
        #np.savetxt('/home/pi/Documents/admp441_data/'+filename_B+'frequency', frequency_B, delimiter = " ", fmt='%.2f')
    #schedule.every(2).minutes.do(job_B) 
    #wavファイル削除
    file = filename_B + '.wav'
    os.remove(path + file)
    #print(path + file, 'deleted')
    t39 = time.time()
    print("Greph_B", t39-t30)


RMS_data = []
index_loop = 1
while index_loop <= Loop_count_Value:
    Recording_A()
    RMS_data.append(rms_A)
    #wavファイル削除
    file = filename_A + '.wav'
    os.remove(path + file)
    index_loop += 1

#Recording_A()を実行
Recording_A()
#１時間毎に関数job_Bを実施
schedule.every().hour.do(job) 
#schedule.every(3).minutes.do(job)

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
    t52 = time.time()
    index_loop += 1
    schedule.run_pending()
    print('thread_1',t51-t50)
    print('thread_2',t52-t51)
    
#except KeyboardInterrupt:
#print("FINISH!")
