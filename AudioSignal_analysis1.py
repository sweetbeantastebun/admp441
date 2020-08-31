# coding: utf-8
import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ

t00 = time.time()
path = '/home/pi/Documents/admp441_data/'  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)

def recording_A():
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

def Analytics_A():
    global t2
    global t3
    global t7
    global wavfile_A
    global rms
    t2 = time.time()
    #wavファイルの読み込み
    wavfile_A = path + filename_A + '.wav'
    wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    samples = np.frombuffer(samples, dtype="int16")  / float((np.power(2, 16) / 2) - 1)  #符号付き整数型16ビットに正規化した配列へ変換する
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。 
    t3 = time.time()

    #samplesを変数audio_signalとしてコピー
    audio_signal = samples.copy()
    #RMS
    rms = np.sqrt((audio_signal**2).mean())
    #print('RMS', rms)
    t4= time.time()
        
    #FFT
    N = 4096  #サンプル数を指定 #録音2秒で4096データの周波数分解能は10Hz
    spectrum_A = np.fft.fft(samples[0:N])  #2次元配列(実部，虚部)
    frequency_A = np.fft.fftfreq(N, 1.0/fs)  #周波数軸の計算
    #spectrum_A = np.fft.fft(samples)  #2次元配列(実部，虚部)
    #frequency_A = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算
    t5 = time.time()

    #dB換算
    def db(x,dBref):
        y = 20 * np.log10(x / dBref)
        return y
    #振幅スペクトルをdBに変換    
    spectrum_dB_A = db(spectrum_A, 2e-5)
    
    #リファレンスデータの読み込み
    reffrence_spectrum_filename = '/home/pi/Documents/admp441_data/****'
    reffrence_spectrum = np.loadtxt(reffrence_spectrum_filename,delimiter=",")
    reffrence_spectrum_dB = db(reffrence_spectrum, 2e-5)
    #print(reffrence_spectrum.read())
    reffrence_frequency_filename = '/home/pi/Documents/admp441_data/*****'
    reffrence_frequency = np.loadtxt(reffrence_frequency_filename,delimiter=",")
    t6 = time.time()
    
    #グラフ準備
    spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    spectrum_dB_A = spectrum_dB_A[:int(spectrum_dB_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除    
  
    #グラフ作成
    plt.ion()
    plt.clf()
    plt.subplot(2, 1, 1)
    #plt.plot(frequency_A, np.abs(spectrum_A))
    plt.plot(frequency_A, np.abs(spectrum_dB_A))
    plt.axis([0,fs/2, 10,1000])
    #plt.xlim(0,fs/2)
    plt.grid(which="both")
    plt.yscale("log")
    #plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum(dB)", fontsize=8)
    plt.subplot(2, 1, 2)
    plt.plot(frequency_A, np.abs(spectrum_A))
    plt.plot(reffrence_frequency, reffrence_spectrum)
    #plt.plot(frequency_A, np.abs(spectrum_dB_A))
    #plt.plot(reffrence_frequency, reffrence_spectrum_dB)   
    plt.axis([0,1400, 0.01,1000])
    #plt.axis([0,1400, 10,1000])
    plt.grid(which="both")
    plt.yscale("log")
    plt.xlabel("freqency(Hz)", fontsize=8)
    plt.ylabel("Amplitude Spectrum", fontsize=8)
    #plt.savefig('/home/pi/Documents/admp441_data/'+filename_A+'.png') 
    plt.draw()
    plt.pause(0.1)
    #plt.close()
#    #print('/home/pi/Documents/admp441_data/'+filename_A+'.png', 'saved')
    
    #データをテキストに出力
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'audio_signal', audio_signal, delimiter = " ", fmt='%.5f')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'spectrum', np.abs(spectrum_A), delimiter = " ", fmt='%.5f')
    #np.savetxt('/home/pi/Documents/admp441_data/'+filename_A+'frequency', frequency_A, delimiter = " ", fmt='%.2f')
     
    #wavファイル削除
    #file = filename_A + '.wav'
    #os.remove(path + file)
#    #print(path + file, 'deleted')  
    t7 = time.time()

RMS_data = []
data_quantity = 3
index_loop = 1
while index_loop <= data_quantity +1:
    recording_A()
    if index_loop == 1:
        pass
    else:
        Analytics_A()
        #print('RMS', rms)
        RMS_data.append(rms)
    index_loop += 1

#print('RMS_data', RMS_data)
average = sum(RMS_data) / len(RMS_data)
print('RMS_average', average)
