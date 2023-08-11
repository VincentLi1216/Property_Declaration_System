from PIL import Image
from pyzbar.pyzbar import decode
import qrcode
import cv2
import os

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

def create_qr(data):
    """
    Generate a QR code.

    Parameters:
    - data: The data to be stored in the QR code
    - file_path: Path where the QR code image will be saved
    """
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    file_path = os.path.join("./qr_cache", f"{data}.png")
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)



if __name__ == "__main__":
    # # 你的QR code圖片路徑
    # path = './upload_img/test2/C010504072.png'
    # read_qr_code(path, is_img=False)

    # 使用方法
    data = "Vincent is so handsome"
    file_path = "example_qr.png"
    create_qr("Allan")
