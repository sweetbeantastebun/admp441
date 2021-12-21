#coding:utf-8
"""
ファイル圧縮
SFTPによるファイル転送（リモートサーバーからローカル）
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
    timestamp = datetime.today()
    timename = timestamp.strftime("%Y%m%d%H%M%S")
    #SFTP転送先のパス
    #SFTPPath = "/home/pi/Documents/" + timename + ".zip"
    SFTPPath = path + timename + ".zip"
    with zipfile.ZipFile(path+timename+".zip", "w", zipfile.ZIP_DEFLATED) as zipfile:
        for f in natsorted(os.listdir(TargetPath)): #os.listdir:ファイルのみの一覧を取得する
            zipfile.write(os.path.join(TargetPath,f),f)  #第二引数にファイル名だけ渡すとディレクトリ無しで.zip作ることできる

    with paramiko.SSHClient() as client:
        #初回ログイン時に「Are you sure you want to continue connecting(yes/no)?」と聞かれても接続できるようにする
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, port=host_port, username=host_username, password=host_password)
        #SFTPセッション開始
        sftp_connection = client.open_sftp()
        #ローカルへファイルからリモートサーバーへ転送
        sftp_connection.put(SFTPPath, SFTPPath)
        client.close()
    #フォルダごと削除
    shutil.rmtree(TargetPath)
    #フォルダを作成
    os.mkdir(TargetPath)
    print("finish " + timename)

#関数の読み出しコマンド
schedule.every().day.at("00:00").do(SFTP)
#schedule.every(1).minutes.do(SFTP)

while True:
    #定期実行の読み出し
    schedule.run_pending()
