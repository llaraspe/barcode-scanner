import streamlit as st
import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import Image
import os
import re
from io import BytesIO

st.title("📸 バーコードスキャナーアプリ")

# アップロード処理（複数可）
uploaded_files = st.file_uploader(
    "画像ファイルをアップロードしてください", type=["png", "jpg", "jpeg"], accept_multiple_files=True
)

# 処理用ディレクトリ
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

created_files = []  # 保存されたファイル名を格納

if uploaded_files:
    if st.button("スキャンして保存"):
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"アップロード: {uploaded_file.name}")

            # PIL → OpenCV 変換
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            barcodes = pyzbar.decode(image_cv)

            # QRコードを除外
            filtered_barcodes = [b for b in barcodes if b.type != "QRCODE"]

            if filtered_barcodes:
                barcode_id = filtered_barcodes[0].data.decode("utf-8")
                safe_id = re.sub(r'[^\w\-_.]', '_', barcode_id)
                output_path = os.path.join(output_dir, f"{safe_id}.jpg")
                image.save(output_path, "JPEG")
                created_files.append(output_path)

                st.success(f"✅ {uploaded_file.name} から {safe_id}.jpg を保存しました。")
            else:
                st.warning(f"⚠️ {uploaded_file.name} にバーコードが見つかりませんでした（QRコードは除外）。")

    # 保存ファイル表示・ダウンロード
    if created_files:
        st.subheader("📁 作成された画像ファイル")
        for file_path in created_files:
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                img_bytes = f.read()
            st.download_button(
                label=f"📥 {file_name} をダウンロード",
                data=img_bytes,
                file_name=file_name,
                mime="image/jpeg",
            )
