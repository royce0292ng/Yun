import imagehash
import requests
from bs4 import BeautifulSoup
import urllib.parse
import sqlite3
from PIL import Image, ImageDraw, ImageFont
import os

# Function to save the data (character and meaning) to the database
def save_to_database(character, meaning):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('../data/chinese_dataset/chinese_characters.db')
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            character TEXT PRIMARY KEY,
            meaning TEXT
        )
    ''')

    # Insert the character and meaning into the database
    cursor.execute('''
        INSERT OR REPLACE INTO characters (character, meaning)
        VALUES (?, ?)
    ''', (character, meaning))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Character {character} and meaning saved to database.")


def is_missing_character(img):

    missing_character = "../data/chinese_dataset/images/Error.png"

    known_img = Image.open(missing_character).convert("L")
    hash1 = imagehash.phash(img)
    hash2 = imagehash.phash(known_img)

    return hash1 == hash2

def character_image(character):

    output_dir = "../data/chinese_dataset"
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    font_paths = [
        "../data/fonts/NotoSerifJP-Regular.ttf",  # Primary font: Noto Serif JP
        "../data/fonts/NotoSerifTC-Regular.ttf"  # Fallback font: Noto Serif TC
    ]
    font_names = [
        "NotoSerifJP",  # Primary font: Noto Serif JP
        "NotoSerifTC"  # Fallback font: Noto Serif TC
    ]

    for font_path, font_name in zip(font_paths, font_names):
        try:
            font = ImageFont.truetype(font_path, size=64)

            # Create an image with a white background
            img_size = (64, 64)
            img = Image.new('L', img_size, color="white")  # 'L' mode for grayscale (black and white)
            draw = ImageDraw.Draw(img)

            # Draw the Chinese character in the center
            bbox = draw.textbbox((0, 0), character, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (img.width - text_width) / 2 - bbox[0]
            text_y = (img.height - text_height) / 2 - bbox[1]
            draw.text((text_x, text_y), character, font=font, fill="black")

            # Check if the character was rendered as a missing glyph
            if is_missing_character(img):
                print(f"Missing character: '{character}' with font {font_name}")
                continue  # Try the next font

            # Save the image
            image_filename = f"{character}_{font_name}.png"
            img_path = os.path.join(images_dir, image_filename)
            img.save(img_path)

            print(f"Character image saved as {image_filename}")
            return image_filename

        except Exception as e:
            print(f"Error using font {font_name}: {e}")
            continue  # Try next font

def scrape_char_eng_meaning(start_char, end_char):
    # Base URL
    base_url = "https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word="

    # Loop through Unicode characters from start_char to end_char
    # for char_code in range(ord(start_char), ord(end_char) + 1):
    for char_code in range(start_char, end_char + 1):
        # Get the character from Unicode code point
        character = chr(char_code)

        # Encode the character for the URL
        encoded_character = urllib.parse.quote(character)
        url = f"{base_url}{encoded_character}"

        print(f"Scraping: {url}")
        try:
            # Send GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses

            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the content of the <td> with class "char_eng_meaning"
            meaning_section = soup.find('td', class_='char_eng_meaning')
            if meaning_section:
                # Get the text content and clean it up
                meaning = meaning_section.get_text(separator="").strip()
                print(f"Character: {character} {char_code}, English Meaning: {meaning} ")
                save_to_database(character, meaning)
                character_image(character)

            else:
                print(f"Character: {character} {char_code}, English Meaning not found. Skipped ")

        except Exception as e:
            print(f"Error occurred for {character}: {e}")


# Example usage:
if __name__ == "__main__":
    # Define the range of characters to scrape (e.g., start from 鵂)
    start_char = int('4E00', 16)
    end_char = int('9FFF', 16)  # Adjust to the desired range
    # scrape_char_eng_meaning(start_char, end_char)
    character_image("齙")
    character_image("龤")




