import qrcode
import cv2
import numpy as np

def create_white_img(width, height):
    img = np.ones((height, width, 3), np.uint8) * 255

    return img

def add_border(img, width=0, height=0, margin = 3, border =1, color=(100, 100, 100)):
    if width * height == 0:
        [width, height, _] = img.shape
    return cv2.rectangle(img, (margin, margin),(width-margin, height-margin), color,border)


def overlay_img(img1, img2, x, y):
    [height1, width1, _] = img1.shape
    [height2, width2, _] = img2.shape

    # 確保img2不會超出img1的邊界
    end_y = min(y+height2, height1)
    end_x = min(x+width2, width1)

    img1[y:end_y, x:end_x] = img2[0:end_y-y, 0:end_x-x]
    img1 = add_border(img1, width = 1000, height = 200)
    
    cv2.imshow("img1", img1)
    cv2.waitKey()
    cv2.destroyWindow("img1")
    return img1


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
    
    if file_path != None:
        # Save the resized image
        cv2.imwrite(file_path, img_resized)
    else:
        return img_resized



if __name__ == "__main__":

    # Example usage
    data = "https://www.example.com"
    file_path = "example_qr_with_title_right_opencv.png"
    title = "Example QR Code"
    create_qr("Vincent", "qr.png")
    # create_qr_with_title(data, file_path, title, box_size=10, border=6)

    img = overlay_img(create_white_img(1000, 200), create_qr("Vincent"), 190, 0)
    logo = cv2.imread("qr_cache/attachment/ttv_logo.png")
    logo = cv2.resize(logo,(150,150))
    overlay_img(img, logo , 25, 25)
    text = "C140427028"
    cv2.putText(img, text, (410, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.putText(img, "視訊處理放大器", (410, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.imshow("final", img)
    cv2.waitKey()
    cv2.destroyAllWindows()




