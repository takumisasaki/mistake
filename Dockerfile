# python:3.8の公式 image をベースの image として設定
FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリの作成
RUN mkdir /code

# 作業ディレクトリの設定
WORKDIR /code

# カレントディレクトリにある資産をコンテナ上の指定のディレクトリにコピーする
ADD . /code

#requirements.txtをコピーする
COPY requirements.txt .

# pipでrequirements.txtに指定されているパッケージを追加する
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql
