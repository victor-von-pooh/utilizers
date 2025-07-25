# scripts
`utils.py` から `dl_youtube()` 関数を使って, `cfg.txt` に記載したYouTubeのリンク全てを `main.py` の実行で `utilizers/practice/YouTube/downloaded` の中に保存する.

## 実行手順
1. `cfg.txt` に以下のようにURLを貼り付けて保存する

    ```txt
    https://youtu.be/xxx
    https://youtu.be/yyy
    https://youtu.be/zzz
    ```

2. `main.py` をターミナル上で次のように実行する
    ```sh
    python3 main.py
    ```