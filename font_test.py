# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import numpy as np

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
    myFont = ImageFont.truetype('./qr_cache/attachment/TaipeiSansTCBeta-Bold.ttf', 70)
     
    # Add Text to an image
    I1.text((x, y), text, font=myFont, fill = color)

    img = pil_to_cv2(img)
    return img

if __name__ == "__main__":
    img = cv2.imread("./qr_cache/attachment/photo-1565299543923-37dd37887442.jpeg")
    img = add_text(img, "早上好中國", 10, 10, 50)
    cv2.imshow("", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
