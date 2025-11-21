from collections import Counter
import os
import time
from typing import Callable, Optional, Union
from urllib.parse import quote

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
import requests
from scipy.stats import skew, kurtosis
from selenium import webdriver
from selenium.webdriver import chrome
from yt_dlp import YoutubeDL


class VisualDirectory():
    def __init__(self, root_path: str):
        self.root_path = root_path

    def build_tree(self, path: str, prefix: str = "") -> list[str]:
        """
        ディレクトリ構造を文字列のリストとしてまとめるメソッド

        Parameters
        ----------
        path: str
            パス名
        prefix: str = ""
            ディレクトリ名やファイル名の前の接頭辞

        Returns
        ----------
        lines: list[str]
            階層表現リスト
        """
        # ディレクトリとファイルでそれぞれソート
        dirs = []
        files = []
        for f in os.listdir(path):
            if os.path.isdir(os.path.join(path, f)):
                dirs.append(f)
            else:
                files.append(f)
        entries = sorted(dirs) + sorted(files)

        # 階層表現を lines に格納
        lines = []
        for i, entry in enumerate(entries):
            full_path = os.path.join(path, entry)
            connector = "└── " if i == len(entries) - 1 else "├── "
            lines.append(prefix + connector + entry)
            if os.path.isdir(full_path):
                extension = "      " if i == len(entries) - 1 else "│     "
                lines.extend(self.build_tree(full_path, prefix + extension))

        return lines

    def visualize(self, output_path: str) -> None:
        """
        ディレクトリ構造を画像として保存するメソッド

        Parameters
        ----------
        output_path : str
            保存する画像ファイルのパス

        Returns
        ----------
        None
        """
        # build_tree メソッドを使ってディレクトリ構造を取得
        root_alias = os.path.basename(os.path.abspath(self.root_path))
        tree_lines = [root_alias] + self.build_tree(self.root_path)

        # 可視化処理
        plt.figure(figsize=(10, 0.01 * len(tree_lines)))
        plt.axis("off")
        for i, line in enumerate(tree_lines):
            plt.text(0, len(tree_lines) - i, line, fontsize=10)
        plt.savefig(output_path, bbox_inches="tight", dpi=200)
        plt.close()


def address_to_latlon(address: str) -> dict:
    """
    住所から緯度経度を取得する関数

    Parameters
    ----------
    address: str
        住所

    Returns
    ----------
    latlon_dict: dict
        緯度経度の辞書
    """
    # 国土地理院の URL からデータを取得
    url = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    address_quote = quote(address)
    response = requests.get(url + address_quote)

    # 緯度経度の情報を抽出して辞書として保存
    latlon = response.json()[0]["geometry"]["coordinates"]
    latlon_dict = {"lat": latlon[1], "lon": latlon[0]}

    return latlon_dict


def dl_pdf(url: str, file_path: str) -> None:
    """
    PDF ファイルをダウンロードする関数

    Parameters
    ----------
    url: str
        URL を指定
    file_path: str
        保存先のパス名

    Returns
    ----------
    None
    """
    # PDF ファイルを取得
    response = requests.get(url)

    # 保存先にファイルを書き込み
    with open(file_path, "wb") as f:
        f.write(response.content)

    # ダウンロード完了のメッセージを表示
    print(f"Downloaded: {file_path}")


def dl_youtube(
    url: Union[str, list[str]], file_path: str, format: str = "mp4"
) -> None:
    """
    YouTube 動画をダウンロードする関数

    Parameters
    ----------
    url: Union[str, list[str]]
        URL を指定(複数指定可)
    file_path: str
        保存先のパス名
    format: str = "mp4"
        保存ファイルのフォーマット指定

    Returns
    ----------
    None
    """
    # 動画ダウンロード用のインスタンスの生成
    yt_opts = YoutubeDL(
        {"outtmpl": file_path + "/%(title)s.%(ext)s", "format": format}
    )

    # 動画を指定パスにダウンロード
    yt_opts.download(url)


def get_html(
    url: str, sleep_time: int = 5, optional: Optional[Callable] = None,
    optional_kwargs: dict = {}
) -> BeautifulSoup:
    """
    スクレイピングする関数

    Parameters
    ----------
    url: str
        URL を指定
    sleep_time: int = 5
        URL 情報取得直後の待機時間(秒)
    optional: Optional[Callable] = None
        必要に応じて適用する関数
    optional_kwargs: dict = {}
        必要に応じて適用する関数の引数の辞書

    Returns
    ----------
    soup: BeautifulSoup
        HTML 情報を持った BeautifulSoup インスタンス
    """
    # Chrome のオプション設定
    options = chrome.options.Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ChromeDriver のパスを指定(パスを通していれば不要)
    service = chrome.service.Service()

    # ドライバ起動
    driver = webdriver.Chrome(service=service, options=options)

    # ターゲットページを開く
    driver.get(url)
    time.sleep(sleep_time)

    # オプションがあれば実行する
    if optional is not None:
        optional(driver, **optional_kwargs)

    # BeautifulSoup で返す
    body_html = driver.find_element(
        "tag name", "body"
    ).get_attribute("innerHTML")
    soup = BeautifulSoup(body_html, "html.parser")

    return soup


def stats_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    統計量を分析する関数

    Parameters
    ----------
    df: pd.DataFrame
        統計量を求めたい Pandas の DataFrame データ

    Returns
    ----------
    stats_df: pd.DataFrame
        統計量をまとめたデータフレーム
    """
    # 統計量計算が可能な型のデータのみ抽出
    extracted_df = df.select_dtypes(include=["int64", "float64"]).copy()

    # カラムごとに各統計量のデータを辞書で管理
    data = []
    for col in extracted_df.columns:
        non_null = extracted_df[extracted_df[col].notna()][col]
        uniques = len(Counter(non_null.to_list()))
        stats = {
            "カウント": extracted_df[col].count(), "ユニーク数": uniques,
            "最小値": extracted_df[col].min(),
            "第1四分位数": extracted_df[col].quantile(0.25),
            "中央値": extracted_df[col].median(),
            "第3四分位数": extracted_df[col].quantile(0.75),
            "最大値": extracted_df[col].max(), "平均値": extracted_df[col].mean(),
            "標準偏差": extracted_df[col].std(),
            "歪度": skew(non_null), "尖度": kurtosis(non_null)
        }
        data.append(pd.Series(stats))

    # 統計量データフレームの作成
    stats_df = pd.DataFrame(dict(zip(extracted_df.columns, data))).T
    stats_df = stats_df.astype({"カウント": int, "ユニーク数": int})
    stats_df = stats_df.sort_values("カウント", ascending=False)

    return stats_df
