import qrcode
import cv2
import numpy as np

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

# Test the function
data = "https://www.example.com"
file_path = "example_qr.png"

create_qr(data, file_path, size=200, box_size=5, border=2)

