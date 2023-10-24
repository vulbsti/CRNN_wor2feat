# Import the libraries
import os
import csv
import glob
import random
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# Define some parameters
num_images = 2000  # Number of images to generate
image_size = (480, 480)  # Size of each image
font_dir = "imgcnn/fonts"  # Directory where fonts are stored
output_dir = "imgcnn/dataset"  # Directory where images and labels are saved
label_file = "labels.csv"  # File name for labels
pre_words = []  # list to store the words already used

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
# choose a random word from the csv file
def choose_word(pre_words):
    words=pd.read_csv('imgcnn/common.csv',skiprows=0)
    length = len(words)
    word = words.iloc[(random.randint(0,length)),0]
    word = str(word)
    if word in pre_words == True:
        choose_word(pre_words)
    else :
        pre_words.append(word)
    return word

#words = ['simon','plastic','waka','gesdptfs','hardesti','blunt','specigs']

# Open the label file for writing
with open(os.path.join(output_dir, label_file), "w") as f:
    # Create a csv writer object
    writer = csv.writer(f)
    # Write the header row
    writer.writerow(["image", "label"])
    # Loop over the number of images to generate
    indx=0
    
    for i in range(num_images):
        word=choose_word(pre_words)
       
        for j in range(8):
            indx += 1
   
            font = random.choice(glob.glob(os.path.join(font_dir, "*.ttf")))
            font_size = random.randint(50, 80)
            font_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            if font_color == bg_color:
                font_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                            
            image = Image.new("RGB", image_size, bg_color)

            draw = ImageDraw.Draw(image)
            
            #since getsize,textsize methods are deprecated in pillow creating new method to get text size
            #function also makes sure the text fits in the image
            def get_size(font,font_size,word):
                font_obj = ImageFont.truetype(font, font_size)
                bbox=draw.textbbox((0,0),word,font=font_obj)
                text_width,text_height = bbox[2]-bbox[0] ,bbox[3]-bbox[1]
                if (image_size[0]-text_width) < 100 or (image_size[1]-text_height) < 100:
                    font_size1= random.randint(30,60)
                    get_size(font,font_size1,word)
                return text_width,text_height,font_obj
                                   
            #a,b are text width and height and fontimg is the font object
            a,b,fontimg=get_size(font,font_size,word)
            
            min_w= max(image_size[0] - a, 30)
            min_h =max(image_size[1] - b,30)
            x,y = random.randint(20,min_w),random.randint(20,min_h)
            print(a,b,x, y)

            draw.text((x, y), word, font_color, fontimg)

            image = image.rotate(random.choice([0, 90, 180, 270]))
            # Crop the image by a random margin between 0 and 10 pixels on each side
            image = image.crop((random.randint(0, 10), random.randint(0, 10), image_size[0] - random.randint(0, 10),
                               image_size[1] - random.randint(0, 10)))
             #Resize the image back to the original size
            image = image.resize(image_size)
            image = image.filter(ImageFilter.GaussianBlur(random.uniform(0, 2)))
            ImageEnhance.Color(image).enhance(random.uniform(0, 2))
            ImageEnhance.Contrast(image).enhance(random.uniform(0, 3))
            ImageEnhance.Brightness(image).enhance(random.uniform(0, 3))
            ImageEnhance.Sharpness(image).enhance(random.uniform(0, 3))

            # Generate a file name for the image
            image_file = f"image_{indx}.jpg"
            # Save the image in the output directory
            image.save(os.path.join(output_dir, image_file))
            # Write the image file name and the label in the label file
            writer.writerow([image_file, word])
