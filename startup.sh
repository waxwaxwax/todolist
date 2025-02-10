#!/bin/bash

PROJECT_DIR="$(dirname "$0")"
VENV_DIR="$PROJECT_DIR/venv"
REQUIREMENTS="$PROJECT_DIR/requirements.txt"

# 仮想環境が存在しない場合、作成
if [ ! -d "$VENV_DIR" ]; then
    echo "仮想環境を作成しています..."
    python3 -m venv "$VENV_DIR"
fi

# 仮想環境をアクティベート
echo "仮想環境をアクティベートしています..."
source "$VENV_DIR/bin/activate"

# requirements.txt の存在を確認
if [ ! -f "$REQUIREMENTS" ]; then
    echo "⚠️ ERROR: requirements.txt が見つかりません"
    exit 1
fi

# 必要なパッケージをインストール
echo "必要なパッケージをインストールしています..."
pip install -r "$REQUIREMENTS"

# Flask のインストール確認
if ! command -v flask &> /dev/null; then
    echo "⚠️ ERROR: Flask がインストールされていません"
    exit 1
fi

# Flaskアプリケーションを起動
echo "Flaskアプリケーションを起動しています..."
export FLASK_APP="$PROJECT_DIR/app.py"
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
