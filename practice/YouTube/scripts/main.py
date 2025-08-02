from utils import dl_youtube


# configファイルを読み込む
cfg_path = "cfg.txt"
with open(cfg_path) as f:
    urls = [s.rstrip() for s in f.readlines()]

# ファイルを保存するデータパスを指定
dir_path = "../output"

# 動画のダウンロード
dl_youtube(urls, dir_path)
