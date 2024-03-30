import streamlit as st
from PIL import Image
import pytesseract
# from paddleocr import PaddleOCR
import requests
from io import BytesIO
import numpy as  np
import easyocr


def pytesseract_ocr(image):
    text = pytesseract.image_to_string(image)
    return text

# def paddleocr_ocr(image_input):
#     ocr = PaddleOCR(use_angle_cls=True, lang='en')
#     result = ocr.ocr(image_input, cls=True)
#     lines = [line[1][0] for line in result[0]]
#     text = '\n'.join(lines)
#     return text

def easyocr_ocr(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(np.array(image), paragraph="False")
    lines = [item[1] for item in result]
    text = '\n'.join(lines)
    return text

def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

st.title("OCR Application")
option = st.sidebar.radio("Choose Input Option", ("Upload Image", "URL"))

image = None 

if option == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
elif option == "URL":
    image_url = st.sidebar.text_input("Enter Image URL:")
    if image_url:
        try:
            image = load_image_from_url(image_url)
            st.image(image, caption='Image from URL', use_column_width=True)
        except Exception as e:
            st.error("Error: Unable to load image from URL. " + str(e))
            # return

ocr_engine = st.sidebar.selectbox("Select OCR Engine", ("Pytesseract", "EasyOCR"))

with st.spinner('Performing OCR...'):
    
    if st.button("Perform OCR") and image:
        if ocr_engine == "Pytesseract":
            text = pytesseract_ocr(image)
            st.write("### OCR Result (Pytesseract):")
            st.write(text)
        # elif ocr_engine == "PaddleOCR":
        #     image_input = image_url if option == "URL" else np.array(image)
        #     text = paddleocr_ocr(image_input)
        #     st.write("### OCR Result (PaddleOCR):")
        #     st.write(text)
        elif ocr_engine == "EasyOCR":
            text = easyocr_ocr(image)
            st.write("### OCR Result (EasyOCR):")
            st.write(text)
