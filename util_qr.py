from PIL import Image
from pyzbar.pyzbar import decode
# import cv2

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

if __name__ == "__main__":
    # 你的QR code圖片路徑
    path = './upload_img/test2/C010504072.png'
    read_qr_code(path, is_img=False)

