from datetime import datetime as dt
import time

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from utils import get_html


def search_web(
    driver: webdriver.Chrome, year: int,
    month: int, sleep_time: int = 5
) -> None:
    """
    WEB内で検索する関数

    Parameters
    ----------
    driver: webdriver.Chrome
        Seleniumで作成したドライバ
    year: int
        検索対象年
    month: int
        検索対象月
    sleep_time: int = 5
        URL情報取得直後の待機時間(秒)

    Returns
    ----------
    None
    """
    # 年を指定
    year_select = Select(
        driver.find_elements(By.CLASS_NAME, "form-select")[0]
    )
    year_select.select_by_value(str(year))

    # 月を指定
    month_select = Select(
        driver.find_elements(By.CLASS_NAME, "form-select")[1]
    )
    month_select.select_by_value(str(month))

    # 表示ボタンをクリック
    wait = WebDriverWait(driver, sleep_time)
    display_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@value='表示']")
        )
    )
    driver.execute_script(
        "arguments[0].scrollIntoView(true);", display_button
    )
    time.sleep(sleep_time)
    display_button.click()

    # 表示が変わるまで待機
    time.sleep(sleep_time)


def single_fetch(soup: BeautifulSoup) -> pd.DataFrame:
    """
    1回分のデータを取得する関数

    Parameters
    ----------
    soup: BeautifulSoup
        HTML情報を持ったBeautifulSoupインスタンス

    Returns
    ----------
    df: pd.DataFrame
        取得したデータのデータフレーム
    """
    # WEBから必要なデータのリストを抽出
    table = soup.find("div", class_="idx-archive table-responsive-md")
    data_list = table.find_all("tr")

    # データフレーム用のカラムとデータのリストの用意
    cols = []
    targets = []
    for i, data in enumerate(data_list):
        # 1つ目のデータはカラム、それ以外はデータ
        if i == 0:
            # カラムを順に取得
            ths = data.find_all("th")
            for th in ths:
                cols.append(str(th.text))
        else:
            # データをカラムごとに取得
            tds = data.find_all("td")

            # 1つ目は日付なのでdatetime型として保存
            date = str(tds[0].text).replace(".", "-")
            date = dt.strptime(date, "%Y-%m-%d").date()
            target = [date]

            # それ以外は値なのでfloat型として保存
            for i in range(1, 5):
                tmp = float(str(tds[i].text).replace(",", ""))
                target.append(tmp)

            # targetsリストに格納
            targets.append(target)

    # targetsを転置させてカラムと紐付けた辞書を作成
    targets = np.array(targets).T
    df_dict = dict(zip(cols, targets))

    # データフレームとして保存
    df = pd.DataFrame(df_dict)

    return df


# 日経平均アーカイブのWEBサイトのURL
url = "https://indexes.nikkei.co.jp/nkave/archives/data"

# 1986年から2024年までのリストを用意
years = list(range(1986, 2025))
months = list(range(1, 13))

# データフレームをdfsに格納する
dfs = []
for year in years:
    for month in months:
        tmp_soup = get_html(
            url, optional=search_web, optional_kwargs={
                "year": year, "month": month
            }
        )
        df = single_fetch(tmp_soup)
        dfs.append(df)

# データフレームを結合してCSVファイルとして保存
all_df = pd.concat(dfs, ignore_index=True)
file_path = "../output/stocks.csv"
all_df.to_csv(file_path, index=False)
