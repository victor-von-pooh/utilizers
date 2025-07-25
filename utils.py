import time
from typing import Union

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from yt_dlp import YoutubeDL


def dl_youtube(
    url: Union[str, list[str]], file_path: str, format: str = "mp4"
) -> None:
    """
    YouTube動画をダウンロードする関数

    Parameters
    ----------
    url: Union[str, list[str]]
        URLを指定(複数指定可)
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


def get_html(url: str, sleep_time: int = 5) -> BeautifulSoup:
    """
    スクレイピングする関数

    Parameters
    ----------
    url: str
        URLを指定
    sleep_time: int = 5
        URL情報取得直後の待機時間(秒)

    Returns
    ----------
    soup: BeautifulSoup
        HTML情報を持ったBeautifulSoupインスタンス
    """
    # Chromeのオプション設定
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ChromeDriverのパスを指定(パスを通していれば不要)
    service = Service()

    # ドライバ起動
    driver = webdriver.Chrome(service=service, options=options)

    # ターゲットページを開く
    driver.get(url)
    time.sleep(sleep_time)
    body_html = driver.find_element(
        "tag name", "body"
    ).get_attribute("innerHTML")
    soup = BeautifulSoup(body_html, "html.parser")

    return soup
