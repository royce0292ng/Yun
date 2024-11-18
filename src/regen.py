import os
import imagehash
from PIL import Image, ImageDraw, ImageFont

# Directory containing images
images_dir = "../data/chinese_dataset/images"
missing_character = "../data/chinese_dataset/images/Error.png"

font_paths = [
    "../data/fonts/NotoSerifJP-Regular.ttf",  # Primary font: Noto Serif JP
    "../data/fonts/NotoSerifTC-Regular.ttf"  # Fallback font: Noto Serif TC
]
font_names = [
    "NotoSerifJP",  # Primary font:  Noto Serif JP
    "NotoSerifTC"   # Fallback font: Noto Serif TC
]

# Placeholder hash for a missing character image
missing_character_img = Image.new("L", (64, 64), color="white")


missing_img = Image.open(missing_character).convert("L")
missing_character_hash = imagehash.phash(missing_img)

# Loop through all files in the images directory
for image_file in os.listdir(images_dir):

    if not image_file.endswith(".png"):
        continue

    # Skip if the file is named "Error.png"
    if image_file == "Error.png":
        print(f"Skipping file named 'Error.png': {image_file}")
        continue

    # Try to split the file name to extract character and font details
    try:
        character, font_name = os.path.splitext(image_file)[0].rsplit("_", 1)
    except ValueError:
        print(f"Invalid file name format: {image_file}")
        continue

    # Full path of the image file
    image_path = os.path.join(images_dir, image_file)

    # Open the image and calculate its hash
    with Image.open(image_path) as img:
        img_hash = imagehash.phash(img)

        # Check if the image is a missing character
        if img_hash == missing_character_hash:
            print(f"Missing character detected: {image_file} (Character: {character}, Font: {font_name})")
            os.remove(image_path)  # Remove the old image
            print(f"Removed: {image_file}")

            # Use the next font in the fallback list
            for font in font_names:
                try:
                    # Create a new image with a white background
                    img_size = (64, 64)
                    img = Image.new("L", img_size, color="white")  # 'L' mode for grayscale
                    draw = ImageDraw.Draw(img)

                    # Render the character using the fallback font
                    font = ImageFont.truetype(font, size=64)  # Adjust size as needed
                    bbox = draw.textbbox((0, 0), character, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    text_x = (img.width - text_width) / 2 - bbox[0]
                    text_y = (img.height - text_height) / 2 - bbox[1]
                    draw.text((text_x, text_y), character, font=font, fill="black")
                    print(f"Recreated image for {character} with font: {font}")

                    # Save the new image with the updated font name
                    new_image_file = f"{character}_{font.split('-')[0]}.png"
                    new_image_path = os.path.join(images_dir, new_image_file)
                    img.save(new_image_path)
                    print(f"Saved new image: {new_image_file}")
                    break  # Stop once a fallback font works
                except Exception as e:
                    print(f"Font {font} could not render {character}. Trying next fallback...")