import pandas as pd

from utils import dl_pdf

# data.csv ファイルを読み込む
csv_path = "data.csv"
df = pd.read_csv(csv_path)

# 論文の URL リストとタイトルリストを取得
urls = df["URL"].to_list()
titles = df["Title"].to_list()

# 論文を保存するディレクトリパスを指定
dir_path = "../output"

# 論文のダウンロード
for url, title in zip(urls, titles):
    path = f"{dir_path}/{title}.pdf"
    dl_pdf(url, path)
print("Done.")
