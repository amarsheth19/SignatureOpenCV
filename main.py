import cv2
import os
import streamlit
from PIL import ImageColor
from PIL import Image

streamlit.title('Signature App')
uploaded_file = streamlit.file_uploader('Upload your input file here')
threshold_value = streamlit.number_input("Please enter the threshold value: ", 0, 255, 90)

if uploaded_file:
    image = Image.open(uploaded_file)
    image.save(uploaded_file.name)

    streamlit.write("Original Image")
    streamlit.image(image)

    image = cv2.imread(uploaded_file.name, cv2.IMREAD_GRAYSCALE)

    temp,black_and_white_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    os.chdir(os.getcwd())
    cv2.imwrite("black_and_white_image.jpg", black_and_white_image)

    rgba = cv2.cvtColor(black_and_white_image, cv2.COLOR_RGB2RGBA)
    r,g,b,a = cv2.split(rgba)
    rgba = cv2.merge((r, g, b, (a-r)))

    hex_value = streamlit.color_picker("Choose the color of your signature:")
    r, g, b = ImageColor.getcolor(hex_value, "RGB")
    rgba[:,:,0] = r
    rgba[:, :, 1] = g
    rgba[:, :, 2] = b

    cv2.imwrite("transparent_image.png", rgba)
    streamlit.write("Edited Image")
    streamlit.image(rgba)

    streamlit.download_button(label="Download image", data=open("transparent_image.png", "rb"), file_name="transparent_signature.png")

