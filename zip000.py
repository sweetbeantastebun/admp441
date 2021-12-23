"""
ファイル圧縮
"""
import zipfile
import paramiko
from datetime import datetime  #タイムスタンプを実行するライブラリ
import os  #ファイルやディレクトリをパス操作するライブラリ
import shutil  #ファイル、ディレクトリの移動、コピーするライブラリ
import glob  #複数のファイルを選択するライブラリ
from natsort import natsorted  #数字の順番に並べ替えるライブラリ（自然順アルゴリズム）
import schedule

#サーバー情報
host = "10.103.193.74"  #リモート側のIPアドレスを入力すること
host_port = "22"
host_username = "pi"
host_password = "1234"

#パス先
path = "/home/pi/Documents/admp441_data/"  #ディレクトリ先を変数pathに格納(データの格納先デレクトリを読み出すときに使用する)
#圧縮するファイルのディレクトリパス
TargetPath = path + "20211105"


def SFTP():
    global zipfile
    timestamp = datetime.today()
    timename = str(timestamp.year) + str(timestamp.month) + str(timestamp.day) + "_" + str(timestamp.hour) + str(timestamp.minute) + str(timestamp.second)
    #SFTP転送先のパス
    #SFTPPath = "/home/pi/Documents/" + timename + ".zip"
    SFTPPath = path + timename + ".zip"
    with zipfile.ZipFile(path+timename+".zip", "w", zipfile.ZIP_DEFLATED) as zipfile:
        for f in natsorted(os.listdir(TargetPath)): #os.listdir:ファイルのみの一覧を取得する
            zipfile.write(os.path.join(TargetPath,f),f)  #第二引数にファイル名だけ渡すとディレクトリ無しで.zip作ることできる
            
SFTP()
print("finish")