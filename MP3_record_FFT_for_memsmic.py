import time  #タイムカウントに使用するライブラリ
import subprocess  #Terminalを実行するライブラリ
from datetime import datetime  #タイムスタンプを実行するライブラリ
timestamp = datetime.today()
#print(timestamp)
t00 = time.time()
#ファイルの名前をタイムスタンプ化する
filename = str(timestamp.month) + str(timestamp.day) + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)
t0 = time.time()

#録音実行（16ビット、44.1kHz、2秒）
record = 'arecord -d 2 -f S16_LE -r 44100 /home/pi/Documents/admp441_data/'+filename+'.wav'
subprocess.call(record, shell=True)
t1 = time.time()
print(t1-t0)
#MP3に圧縮
mpeg = 'lame -V 2 /home/pi/Documents/admp441_data/'+filename+'.wav ''/home/pi/Documents/admp441_data/'+filename+'.mp3'
subprocess.call(mpeg, shell=True)
t2 = time.time()

import numpy as np #配列計算、FFT化するライブラリ
import wave  #wavファイルの読み書きするライブラリ
import csv  #csvを作成するライブラリ
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt  #グラフ化ライブラリ
from pydub import AudioSegment  #メディアデータの変換ライブラリ

t3 = time.time()
mp3_version = AudioSegment.from_file('/home/pi/Documents/admp441_data/'+filename+'.mp3', format='mp3')  #mp3の読み込み
samples = np.array(mp3_version.get_array_of_samples())
#スペクトルをプロット表示
spec = np.fft.fft(samples)
freq = np.fft.fftfreq(samples.shape[0], 1.0/mp3_version.frame_rate)
t4 = time.time()
#グラフ作成
fig = plt.figure(figsize=(10,10),dpi=200)
ax1 = fig.add_subplot(2, 1, 1)
plt.plot(freq, np.abs(spec))
plt.axis([0,mp3_version.frame_rate/2,0,100000000])
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
plt.savefig('/home/pi/Documents/admp441_data/'+filename+'.png')
print('/home/pi/Documents/admp441_data/'+filename+'.png', 'saved')
t4 = time.time()
#print(t4-t00)
