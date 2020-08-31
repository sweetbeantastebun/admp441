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
    
    #FFT
    spectrum_A = np.fft.fft(samples)  #2次元配列(実部，虚部)
    frequency_A = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数軸の計算 
    
    #FFT結果コピー
    spectrum2_A = spectrum_A.copy() 
    
    #包絡線作成の流れ
    #スペクトルを対数変換する。
    #その値を逆フーリエ変換し、時間軸データに戻す。（ケプストラム波形作成）
    #ケプストラム波形の低次のみを抽出しフーリエ変換を再度することによって包絡線を作成する。
    
    #対数変換スペクトル作成
    #桁上げのため1を足して補正
    #小数（<1）を対数化するとマイナス値になることへの回避目的
    spectrum_A_correction = np.abs(spectrum2_A) + 1
    spectrum_A_log = np.log(spectrum_A_correction)
    
    #ケプストラム作成
    cepstrum_A = np.fft.ifft(spectrum_A_log)  #スペクトルの対数に変換した値を逆フーリエ変換
    cepstrum_real_A = cepstrum_A.real
    #print('cepstrum_real_A_before',len(cepstrum_real_A))
    #np.savetxt(filename_A+'cepstrum_real_before', cepstrum_real_A, delimiter = " ", fmt='%.5f')
    
    #包絡線を作成
    cut_lifter = 100  #カットオフ指数。
    cepstrum_real_A[cut_lifter:len(cepstrum_real_A) - cut_lifter] = 0  #ケプストラム波形の高次を0にする（低次のみを残す）
    #print('cepstrum_real_A_after',len(cepstrum_real_A))
    #np.savetxt(filename_A+'cepstrum_real_after', cepstrum_real_A, delimiter = " ", fmt='%.5f')
    cepstrum_low_A = np.fft.fft(cepstrum_real_A)
 
    #グラフ作成準備
    spectrum_A = spectrum_A[:int(spectrum_A.shape[0]/2)]    #スペクトルがマイナスになるスペクトル要素の削除
    cepstrum_low_A = cepstrum_low_A[:int(cepstrum_low_A.shape[0]/2)]
    frequency_A = frequency_A[:int(frequency_A.shape[0]/2)]    #周波数がマイナスになる周波数要素の削除    
        
    #グラフ作成
    #plt.subplot(2, 1, 1)
    plt.plot(frequency_A, np.abs(spectrum_A))  #振幅スペクトル
    plt.plot(frequency_A, np.abs(cepstrum_low_A))  #包絡スペクトル
    plt.axis([0,fs/2,0.0001,1000])
    #plt.xlim(0,fs/2)
    plt.grid(which="both")
    plt.yscale("log")
    plt.xlabel("freqency(Hz)", fontsize=9)
    plt.ylabel("Amplitude Spectrum", fontsize=9)
       
    #ケプストラム波形
    #x_axis = np.arange(0,len(cepstrum_real_A))/fs
    #plt.subplot(2, 1, 2)
    #plt.plot(x_axis, cepstrum_real_A)
    #plt.xlim(0, 3)
    #plt.grid(which="both")
    #plt.xlabel("quefrency(sec)", fontsize=9)
    #plt.ylabel("cepstrum", fontsize=9)
    
    #包絡スペクトル
    #plt.subplot(2, 1, 2)
    #plt.plot(frequency_A, np.abs(cepstrum_low_A))
    #plt.axis([0,fs/2,0.0001,100])
    #plt.xlim(0, fs/2)
    #plt.grid(which="both")
    #plt.yscale("log")
    #plt.xlabel("freqency(Hz)", fontsize=9)
    #plt.ylabel("Amplitude Spectrum", fontsize=9)
    
    plt.show()
    plt.close()
    #plt.savefig(filename_A+'.png')
    #np.savetxt(filename_A+'spectrum', np.abs(spectrum_A), delimiter = " ", fmt='%.5f')
    #np.savetxt(filename_A+'frequency', frequency_A, delimiter = " ", fmt='%.2f')
    #np.savetxt(filename_A+'spectrum envelope', np.abs(cepstrum_low_A), delimiter = " ", fmt='%.5f')

frequency_analysis()

#index_loop = 1
#while index_loop <= 3:
#    frequency_analysis()
#    index_loop += 1
