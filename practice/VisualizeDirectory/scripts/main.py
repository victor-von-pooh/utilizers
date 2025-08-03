from utils import VisualDirectory


path = "../.."
directory = VisualDirectory(path)
out = "../output/dir_tree.png"
directory.visualize(out)
