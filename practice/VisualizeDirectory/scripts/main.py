from utils import VisualDirectory

# ディレクトリのパスを指定して, VisualDirectory クラスをインスタンス化
path = "../.."
directory = VisualDirectory(path)

# ディレクトリ構造を画像として保存
out = "../output/dir_tree.png"
directory.visualize(out)
