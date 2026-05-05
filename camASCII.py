import cv2 as cv
import time
ASCII_CHARS = "█▉▊▋▌▍▎▏ "
# ASCII_CHARS=ASCII_CHARS[::-1]
def resize_image(image, new_width):
    original_height = image.shape[0]
    original_width = image.shape[1]
    ratio = original_height / original_width
    new_height = int(new_width * ratio * 0.35)
    resized_image = cv.resize(image, (new_width, new_height))
    return resized_image
def pixel_to_ascii(pixel_value):
    if pixel_value >= (len(ASCII_CHARS)-1)*(255//len(ASCII_CHARS)):
        return ASCII_CHARS[len(ASCII_CHARS)-1]
    else:
        return ASCII_CHARS[pixel_value//(255//len(ASCII_CHARS))]
    
def convert_to_ascii_art(gray_image):
    ascii_image = ""
    for row in range(gray_image.shape[0]):
        for col in range(gray_image.shape[1]):
            pixel = gray_image[row][col]
            ascii_char = pixel_to_ascii(pixel)
            ascii_image = ascii_image + ascii_char
        ascii_image = ascii_image + "\n"
    return ascii_image

def VideoToAscii(frame,width):
    resize_frame=resize_image(frame,width)
    gray = cv.cvtColor(resize_frame, cv.COLOR_BGR2GRAY)
    formatascii=convert_to_ascii_art(gray)
    return formatascii
   

