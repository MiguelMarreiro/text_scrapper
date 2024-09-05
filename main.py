import openai
from os import environ, path
import dotenv
import base64

import tkinter as tk
from tkinter import filedialog

"""Load Keys"""
dotenv.load_dotenv()
# print(environ['OPENAI_API_KEY'])


def select_file():
    """Creates a guy file selector which returns the file path for the selected file"""
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog and ask the user to select a file
    file_path = filedialog.askopenfilename()

    # Print the selected file path
    if file_path:
        return file_path
    else:
        print("No file selected.")



# Function to encode the image
def encode_image(image_path):
    """Encodes the image in base64 so it can be sent with the message text"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


""" Initiates the openAI connection"""
client = openai.OpenAI()
THIS_MODEL = "gpt-4o-mini"


#_______________Path selection___________________

IMAGE_PATH = select_file()

# IMAGE_PATH = 'source/font_emotions.png'

image_name, image_type = path.splitext(IMAGE_PATH)
# Removing the dot from the extension
clean_extension = image_type.lstrip('.')
output_name = image_name.lstrip('D:/Projects/OCR/openai/source/')
print(clean_extension)  # Output: extension
print(output_name)

# Getting the base64 string
base64_image = encode_image(IMAGE_PATH)


# Send the request to the API
response = client.chat.completions.create(
        model=THIS_MODEL,
        messages=[
            {
                "role": "system",
                "content": [
                    {"type": "text",
                    "text": "You are a cool image analyst.  Your goal is to extract and return the text which "
                            " is in the image provided as a file."
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type":"text",
                        "text": "What is the text in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url":
                            {
                                "url": f"data:image/{clean_extension};base64,{base64_image}"
                            }
                    }
                ]
            }
        ],
        max_tokens=300
    )
print(f"response: {response}")
# Extract the description
description = response.choices[0].message.content
print(f"Desription: {description}")

with open(f'output/{output_name}.txt', 'w', encoding='utf-8') as out_file:
    out_file.write(description)
