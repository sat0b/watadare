# 顔画像検索

## install
依存パッケージをインストール
```
$ pip3 install -r requirements.txt
```

## image_download.py
googleの画像検索から画像をダウンロードしてくる
```
$ python3 image_download.py 芸能人
```

## train.py
画像から特徴ベクトルを作成し、jsonファイルにdumpする
```
$ python3 train.py
```

## server.py
類似顔画像検索のデモツール

```
$ python3 server.py
```

## build docker image
```
$ docker build -t facesearch .
```

## run docker image
```
$ docker run -p 80:8080 -it facesearch
```