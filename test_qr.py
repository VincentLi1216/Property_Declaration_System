import qrcode
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def create_white_img(width, height):
    img = np.ones((height, width, 3), np.uint8) * 255

    return img

def cv2_to_pil(cv2_image):
    """Convert an OpenCV image to PIL format."""
    # Convert BGR to RGB
    cv2_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(cv2_rgb)
    
    return pil_image

def pil_to_cv2(pil_image):
    """Convert a PIL image to OpenCV format."""
    # Convert PIL image to numpy array (RGB format)
    cv2_rgb = np.array(pil_image)
    
    # Convert RGB to BGR
    cv2_image = cv2.cvtColor(cv2_rgb, cv2.COLOR_RGB2BGR)
    
    return cv2_image 

def add_text(img, text, x, y, font_size=50, color=(0, 0, 0)):

    img = cv2_to_pil(img)
     
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
     
    # Custom font style and font size
    myFont = ImageFont.truetype('./qr_cache/attachment/TaipeiSansTCBeta-Bold.ttf', font_size)
     
    # Add Text to an image
    I1.text((x, y), text, font=myFont, fill = color)

    img = pil_to_cv2(img)
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
    create_qr("C140427028", "qr.png")
    # create_qr_with_title(data, file_path, title, box_size=10, border=6)

    img = overlay_img(create_white_img(750, 200), create_qr("C140427028"), 15, 0)
    logo = cv2.imread("qr_cache/attachment/ttv_logo.png")
    logo = cv2.resize(logo,(150,150))
    # overlay_img(img, logo , 25, 25)
    img = add_text(img, "數位非線性剪輯系統", 230, 40, font_size=50)
    img = add_text(img, "C140427028", 230, 100, font_size=70)
    # cv2.putText(img, "視訊處理放大器", (410, 120), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
    cv2.imshow("final", img)
    cv2.waitKey()
    cv2.destroyAllWindows()




