import streamlit as st
import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import Image
import os
import re

st.title("バーコードスキャナーアプリ")

uploaded_file = st.file_uploader("画像ファイルをアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像")

    if st.button("スキャンする"):
        # PIL 画像を OpenCV の形式に変換
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # pyzbarでデコード
        barcodes = pyzbar.decode(image_cv)
        
        # QRCODE を除外
        filtered_barcodes = [b for b in barcodes if b.type != "QRCODE"]

        if filtered_barcodes:
            st.subheader("📦 スキャン結果")
            for barcode in filtered_barcodes:
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type
                st.write(f"**{barcode_type}**: `{barcode_data}`")

            # 画像保存処理（最初のバーコードデータを使用）
            barcode_id = filtered_barcodes[0].data.decode("utf-8")
            # ファイル名として使えない文字を除去
            safe_id = re.sub(r'[^\w\-_.]', '_', barcode_id)

            # フォルダ作成（なければ）
            output_dir = "images"
            os.makedirs(output_dir, exist_ok=True)

            # ファイル保存
            output_path = os.path.join(output_dir, f"{safe_id}.jpg")
            image.save(output_path, "JPEG")
            st.success(f"画像を `{output_path}` に保存しました。")
        else:
            st.warning("バーコードが見つかりませんでした（QRコードは除外されています）。")
