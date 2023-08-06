from PIL import Image
from pyzbar.pyzbar import decode

def read_qr_code(img):
    # # 使用Pillow來讀取圖片
    # img = Image.open(path)
    # print(decode(img))
    # 用pyzbar.decode來讀取QR code
    for barcode in decode(img):
        data = barcode.data.decode('utf-8')
        return data

if __name__ == "__main__":
    # 你的QR code圖片路徑
    path = 'Egg_Defense.png'
    read_qr_code(path)

