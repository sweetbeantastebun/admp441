import subprocess  #Terminalを実行するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
timestamp = datetime.today()
#print(timestamp)
#ファイルの名前をタイムスタンプ化する
filename = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)
#録音実行（32ビット、44.1kHz、2秒）
record = 'arecord -d 2 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename+'.wav'
subprocess.call(record, shell=True)

import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  #グラフ化ライブラリ

AudioFile = '/home/pi/Documents/admp441_data/'+str(filename)+'.wav'  #Audioファイルを変数にする

def ReadWavFile():
    #wavファイルを読み込み、高速フーリエ変換（FFT）
    wr = wave.open(AudioFile, 'r')
    
    fs = wr.getframerate()  #サンプリング周波数。Wave_readのメソッド（=処理）
    g = wr.readframes(wr.getnframes())  #オーディオフレーム数を読み込み。Wave_readのメソッド（=処理）
    #オーディオフレームの値を読み込んで、バイトごとに文字に変換して文字列
    #録音したデータを配列に変換
    g = np.frombuffer(g, dtype='int16') / float(2**15)
    wr.close()  #読み込み終了。ファイルオブジェクトの終了。
    #時間信号をCSVファイルに出力
    #np.savetxt(timestamp.strftime('%Y%m%d-%H%M%S-g'), g, fmt='%.5f')
    
    N = 32768  #サンプル数
    n0 = 0  #サンプリング開始位置
    F = np.fft.fft(g[n0:n0+N])  #高速フーリエ変換
    amp = [np.sqrt(c.real**2 +c.imag**2) for c in F]  #振幅スペクトル
    flist = np.fft.fftfreq(N,d=1.0/fs)  #周波数リスト
    #周波数信号をCSVファイルに出力.整数表示
    #np.savetxt("sample2.csv", flist, fmt='%.1f')
    #np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-flist"), flist, fmt='%.1f')
    #np.savetxt(timestamp.strftime("%Y%m%d-%H%M%S-amp"), amp, fmt='%.1f')
    
    #グラフ作成
    fig = plt.figure(figsize=(10,10),dpi=200)
    ax1 = fig.add_subplot(2, 1, 1)
    plt.plot(flist, amp)
    plt.axis([0,fs/2,0,100])
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)
    
    ax2 = fig.add_subplot(2, 2, 3)
    plt.plot(flist, amp)
    plt.xlim(0, 500)
    plt.ylim(0, 100)
    plt.xlabel("freqency(Hz)", fontsize=12)
    plt.ylabel("FFT", fontsize=12)
    
    ax3 = fig.add_subplot(2, 2, 4)
    plt.plot(flist, amp)
    plt.xlim(500, 4000)
    plt.ylim(0, 100)
    plt.xlabel("freqency(Hz)", fontsize=12)
    
    plt.tight_layout()
    plt.show()
    #pngファイルの作成と保存
    plt.savefig('/home/pi/Documents/admp441_data/'+filename+'.png')
    print('/home/pi/Documents/admp441_data/'+filename+'.png', 'saved')
    #csvに書き込み(w)、出力する(f)
    with open('/home/pi/Documents/admp441_data/'+filename+'.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows([amp, flist])
    print('/home/pi/Documents/admp441_data/'+filename+'.csv', 'saved')

if __name__ == "__main__" :
    ReadWavFile()
