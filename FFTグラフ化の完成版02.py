# -*- coding: utf-8 -*-
import time  #タイムカウントに使用するライブラリ
import numpy as np  #配列計算、FFT化するライブラリ
import wave     #wavファイルの読み書きするライブラリ
import pyaudio  #録音機能を使うためのライブラリ
import csv  #csvを作成するライブラリ
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  #グラフ化ライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ


def MakeWavFile():
    global t0
    global t1
    global t2
    global t3
    global FileName
    global wavFileName
    t0 = time.time()
    timestamp = datetime.today()  #現在の日付、現在の時刻、ここでは測定開始時刻
    #print(timestamp)
    FileName = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + "_" + str(timestamp.second) + "-" + str(timestamp.microsecond)
    wavFileName = FileName + ".wav"  #wavファイル名前を定義
    #録音して（WAVファイル作成）、波形表示
    Record_Seconds = 5
    chunk = 512  #音源から1回(1/RATE毎)読み込む時のデータサイズ。1024(=2**10)
    FORMAT = pyaudio.paInt16  #音源(=バイナリデータ)符号付き16ビット(-32768～32767)のバイナリ文字 #内訳,15ビット数字と1ビットの符号
    CHANNELS = 1  #モノラル。ステレオは2
    RATE = 44100  #サンプルレート,fs(個/sec),44.1kHz

    p = pyaudio.PyAudio()  #PyAudioインスタンスを作成する
    stream = p.open(format = FORMAT,  #入力用Streamを開く。
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)  #frames:pythonのwaveモジュールではバイナリデータ個数
    t1 = time.time()
    #レコード開始
    print("Now Recording...")
    all = []  #append前に空リスト作成
    for i in range(0, int(RATE / chunk * Record_Seconds)):  #整数化。RATEをChunkで割り切れる数に合わせる
        data = stream.read(chunk)  #音声を読み取る
        all.append(data)  #データを追加
    #print('all',len(all))
    #レコード終了
    print("Finished Recording.")
    t2 = time.time()
    stream.close()  # Streamをcloseする
    p.terminate()  # PyAudioインスタンスを終了する    
    data = b"".join(all)  #録音したデータを配列に変換
    result = np.frombuffer(data,dtype="int16") / float((np.power(2, 16) / 2) - 1)  #-1～1に正規化のため、float(x)xの浮動小数点数への変換 #int16:符号付き16bit(=2byte)

    wavFile = wave.open(wavFileName, "wb")
    wavFile.setnchannels(CHANNELS)
    wavFile.setsampwidth(p.get_sample_size(FORMAT))
    wavFile.setframerate(RATE)
    wavFile.writeframes(b"".join(all)) 
    wavFile.close()
    t3 = time.time()


def ReadWavFile():
    global t4
    global t5
    global t6
    global samples
    t4 = time.time()
    #wavファイルを読み込み、高速フーリエ変換（FFT）
    wr = wave.open(wavFileName, "r")  #wavファイルの読み込み。ファイル開く。オブジェクト化。
    # waveファイルが持つ性質を取得
#    ch = wr.getnchannels()
#    width = wr.getsampwidth()
#    fr = wr.getframerate()
#    fn = wr.getnframes()
#    print("Channel: ", ch)  #1
#    print("Sample width: ", width)  #2
#    print("Frame Rate: ", fr)  #44100
#    print("Frame num: ", fn)  #220160
#    print("Total time: ", 1.0 * fn / fr)  #4.992290249433107
    
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    samples = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    samples = np.frombuffer(samples, dtype="int16") / float((np.power(2, 16) / 2) - 1)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    #print('samples',len(samples))
    t7 = time.time()
    
    F = np.fft.fft(samples)
    F_abs = np.abs(F)  # FFT結果（複素数）を絶対値に変換
    freq = np.fft.fftfreq(samples.shape[0], 1.0/fs)  #周波数リスト
    
    t5 = time.time()
    
    #グラフ化する命令文
    fig = plt.figure(figsize=(10,10),dpi=200)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(freq, F_abs)
    #plt.axis([0,fs/2,0,100])
    plt.grid(which="both")
    plt.xscale("log")
    plt.yscale("log")
    plt.axis([0,fs/2,0,10000])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("Amplitude Spectrum", fontsize=12)
    
    ax2 = fig.add_subplot(2, 2, 3)
    plt.plot(freq, F_abs)
    #plt.plot(flist, F)
    plt.xlim(0, 1000)
    plt.ylim(0, 100)
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("Amplitude Spectrum", fontsize=12)
    
    #ax3 = fig.add_subplot(2, 2, 4)
    #plt.plot(flist, amp)
    #plt.plot(flist, F)
    #plt.xlim(4000, 18000)
    #plt.ylim(0, 60)
    #plt.xlabel("freqency(Hz)", fontsize=12)
    plt.savefig('/home/pi/Documents/admp441_data/'+FileName+'.png')
    plt.tight_layout()  #グラフの位置やサイズが自動で調整されて、出力画像からのはみ出しを抑えることができるコード。
    plt.close()
    np.savetxt('/home/pi/Documents/admp441_data/'+FileName+'spec', F_abs, delimiter = " ", fmt='%.5f')
    np.savetxt('/home/pi/Documents/admp441_data/'+FileName+'freq', freq, delimiter = " ", fmt='%.5f')
    t6 = time.time()

#MakeWavFile()
#ReadWavFile()
#print('MakeWavFile',t3-t0)
#print('ReadWavFile',t6-t4)

while True:
    MakeWavFile()
    ReadWavFile()
    print('MakeWavFile',t3-t0)
    print('ReadWavFile',t6-t4)

#g = np.frombuffer(g, dtype="int16") / float(2**15)
#frombuffer(x, dtype="int16")は、xを2バイト単位のデータが並んでいるバイナリデータとみなして、1次元配列にする。
#符号付2バイトなので、各要素の値は、-32768～32767 になります。

#x=frombuffer(x, dtype="int16")   #(1)
#x=x/32768                        #(2)
#と分けて書くことができます。(1)は上で説明した通りです。
#(2)は numpy では、「ndarray / 数値」で、「ndarray内の各要素を数値で割る」という処理を表現できます。
#このため -32768～32767 の値を 32768で割るため、各要素が -1以上1未満のfloat な ndarray になります。
#正規化
