import os
from PIL import Image

THRESHOLD = 30
OUTPUT_DIR = "output"

def black_to_white_keep_transparency(img):
    img = img.convert("RGBA")
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if r < THRESHOLD and g < THRESHOLD and b < THRESHOLD:
                pixels[x, y] = (255, 255, 255, a)
    return img
def process_folder():
    script_dir = os.getcwd()
    output_path = os.path.join(script_dir, OUTPUT_DIR)
    os.makedirs(output_path, exist_ok=True)
    for file in os.listdir(script_dir):
        if not file.lower().endswith(".png"):
            continue
        input_file = os.path.join(script_dir, file)
        output_file = os.path.join(output_path, file)
        try:
            img = Image.open(input_file)
            img = black_to_white_keep_transparency(img)
            img.save(output_file, "PNG")
            print(f"ok : {file}")
        except Exception as e:
            print(f"no: {file} : {e}")

if __name__ == "__main__":
    process_folder()
