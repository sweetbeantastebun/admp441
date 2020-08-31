# coding: utf-8
import time  #タイムカウントに使用するライブラリ
import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import matplotlib.pyplot as plt  #グラフを作成するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ

global filename_A
timestamp = datetime.today()
filename_A = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "." + str(timestamp.microsecond)

def frequency_analysis():   
    #wavファイルの読み込み
    wavfile_A = "2020618_1335_8.269419.wav"
    wr = wave.open(wavfile_A, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    samples_N = len(samples)
        
    #FFT
    spectrum_A = np.fft.fft(samples)  #2次元配列(実部，虚部)
    frequency_A = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算 
    
    #ローパスフィルタ処理（カットオフ周波数を超える帯域の周波数信号を0にする）
    spectrum2_A = spectrum_A.copy()
    cut_frequency = 5000
    spectrum2_A[(frequency_A > cut_frequency)] = 0  #カットオフを超える周波数のデータをゼロにする（ノイズ除去）

    #周波数リスト
    spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    spectrum2_A = spectrum2_A[:int(spectrum2_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除
        
    #グラフ作成
    plt.subplot(2, 1, 1)
    plt.plot(frequency_A, np.abs(spectrum_A))
    plt.axis([0,fs/2,0.0001,1000])
    plt.grid(which="both")
    plt.yscale("log")
    plt.xlabel("freqency(Hz)", fontsize=9)
    plt.ylabel("Amplitude Spectrum", fontsize=9)
    
    plt.subplot(2, 1, 2)
    plt.plot(frequency_A, np.abs(spectrum2_A))
    plt.axis([0,fs/2,0.0001,1000])
    plt.grid(which="both")
    plt.yscale("log")
    plt.xlabel("freqency(Hz)", fontsize=9)
    plt.ylabel("Amplitude Spectrum", fontsize=9)
    
    plt.show()
    plt.close()
    #plt.savefig(filename_A+'.png')
    #np.savetxt(filename_A+'spectrum', np.abs(spectrum_A), delimiter = " ", fmt='%.5f')
    #np.savetxt(filename_A+'spectrum2', np.abs(spectrum2_A), delimiter = " ", fmt='%.5f')
    #np.savetxt(filename_A+'frequency', frequency_A, delimiter = " ", fmt='%.2f')

frequency_analysis()

#index_loop = 1
#while index_loop <= 3:
#    frequency_analysis()
#    index_loop += 1
