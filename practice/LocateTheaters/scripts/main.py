import json

import folium
import pandas as pd

from utils import address_to_latlon

# 住所のファイルを読み込む
address_data_path = "addresses.json"
with open(address_data_path) as f:
    data = json.load(f)

# データを劇場名と住所に分解
theaters = list(data.keys())
addresses = list(data.values())

# 住所から緯度経度を取り出す
lats = []
lons = []
for address in addresses:
    latlon_dict = address_to_latlon(address)
    lats.append(latlon_dict["lat"])
    lons.append(latlon_dict["lon"])

# データフレームを作成
data_dict = {
    "劇場名": theaters, "住所": addresses,
    "緯度": lats, "経度": lons
}
df = pd.DataFrame(data_dict)

# 地図の初期位置を設定
map_center = [df["緯度"].mean(), df["経度"].mean()]
m = folium.Map(location=map_center, zoom_start=5)

# 各劇場をマーカーとして追加
for _, row in df.iterrows():
    folium.Marker(
        location=[row["緯度"], row["経度"]],
        popup=row["劇場名"], tooltip=row["劇場名"]
    ).add_to(m)

# 地図を HTML として保存
output_path = "../output/theaters_map.html"
m.save(output_path)
