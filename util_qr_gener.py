import qrcode
import cv2
import numpy as np
import math
from PIL import ImageFont, ImageDraw, Image
import util_json

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
    # img1 = add_border(img1, width = 1000, height = 200)
    
    # cv2.imshow("img1", img1)
    # cv2.waitKey()
    # cv2.destroyWindow("img1")
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

def create_one_qr_sticker(item_id, chinese_name):
    img = overlay_img(create_white_img(700, 200), create_qr(item_id), 15, 0)
    img = add_border(img, width=700, height=200)
    img = add_text(img, item_id, 230, 30, font_size=70)
    img = add_text(img, chinese_name, 230, 110, font_size=50)
    return img

def show_img(img):
    cv2.imshow("show_img func", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    

def create_qr_stickers4location(session, location, x_num, y_num):
    item_list = util_json.get_not_done_loc_dict(session)[location]
    # print(item_list)
    top_margin = 200
    blank_img = create_white_img(700*x_num, 200*y_num+top_margin)
    item_num = len(item_list)
    page_num = math.ceil(item_num/(x_num*y_num))
    # print(f"page_num:{page_num}, item_num:{item_num}")
    output_imgs = []
    i = 0

    for page_index in range(page_num):
        img = np.copy(blank_img)
        for row in range(y_num):
            for column in range(x_num):
                if i >= item_num:
                    break
                overlay_img(img, create_one_qr_sticker(item_list[i]["資產編號"], item_list[i]["中文名稱"]), 700*column, 200*row+top_margin)
                i += 1
                # print(f"i:{i}, page_index:{page_index}, column:{column}, row:{row}")
        page_title = f"Page: {page_index+1}/{page_num}"
        img = add_text(img, location, 10, 10, 100)
        img = add_text(img, page_title, 10, 130, 50)
        output_imgs.append(img)
        # show_img(img)
    
    return output_imgs

def create_qr_stickers4session(session, x_num, y_num):
    loc_list = util_json.get_not_done_loc_dict(session)
    output_imgs = []
    loc_dict = {}
    index = 0
    for i,location in enumerate(loc_list):
        for img in create_qr_stickers4location(session, location, x_num, y_num):
            output_imgs.append(img)
            loc_dict[i] = location
            index += 1
            # show_img(img)
    return output_imgs, loc_dict
    


if __name__ == "__main__":
    # img = create_one_qr_sticker("C140427028", "硬碟")
    # cv2.imshow("final", img)
    # cv2.imwrite("qr_sticer.png", img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    place = "無位置描述"
    session = "./sessions/Iphone1.json"
    # place = "VTR"
    # img1, img2 = create_qr_stickers4location("./sessions/Iphone1.json", place, 5, 15)
    # show_img(img1)
    # show_img(img2)
    create_qr_stickers4session(session, 5, 15)



