from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
import cv2
import os
import numpy as np

def read_qr_code(img, is_img=True):
    # # 使用Pillow來讀取圖片
    if not is_img:
        img = Image.open(path)
        print(decode(img))
    # 用pyzbar.decode來讀取QR code
    for barcode in decode(img):
        data = barcode.data.decode('utf-8')
        print(data)
        return data

def create_qr(data, file_path=None, size=200, box_size=5, border=2):
    """
    Generate a QR code.

    Parameters:
    - data: The data to be stored in the QR code
    - file_path: Path where the QR code image will be saved
    - box_size: Controls the size of each box (pixel) in the QR code
    - border: Controls the number of boxes (pixels) for the border around the QR code
    """
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    # Convert PIL image to numpy array
    img_np = np.array(img.convert("RGB"))  # Convert to RGB before converting to NumPy array

    # Convert RGB to BGR
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Resize using cv2
    img_resized = cv2.resize(img_np, (size, size))
    
    if path != None:
        # Save the resized image
        cv2.imwrite(file_path, img_resized)
    else:
        return img_resized



if __name__ == "__main__":
    # # 你的QR code圖片路徑
    # path = './upload_img/test2/C010504072.png'
    # read_qr_code(path, is_img=False)

    # 使用方法
    data = "Vincent is so handsome"
    file_path = "example_qr.png"
    create_qr("Allan")
