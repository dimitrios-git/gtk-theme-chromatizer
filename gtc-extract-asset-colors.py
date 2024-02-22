import os
from PIL import Image

def extract_colors_from_image(image_path):
    with Image.open(image_path) as img:
        # Convert palette-based images with transparency to 'RGBA' to handle transparency
        if img.mode == 'P':
            img = img.convert('RGBA')
        
        # If the image is 'RGBA', convert to 'RGB' to ignore the alpha channel
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Extract all colors from the image
        colors = img.getcolors(img.size[0] * img.size[1])
        # `colors` is a list of (count, (r, g, b)) tuples

        # Extract just the unique RGB values
        unique_rgb = {color[1] for color in colors}  # Use a set comprehension for uniqueness
        return unique_rgb

def find_png_files(folder_path):
    png_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.png'):
                png_files.append(os.path.join(root, file))
    return png_files

def main(folder_path, output_file_path):
    all_unique_rgbs = set()
    png_files = find_png_files(folder_path)

    for png_file in png_files:
        unique_rgbs = extract_colors_from_image(png_file)
        all_unique_rgbs.update(unique_rgbs)  # Update the set with unique colors from this image

    # Write the unique RGB values to the output file
    with open(output_file_path, 'w') as f:
        for rgb in sorted(all_unique_rgbs):  # Sort the colors for consistency
            f.write(f'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})\n')

# Provide the folder path and output file path here
folder_path = 'assets'
output_file_path = 'theme_colors_rgb_png.data'

if __name__ == '__main__':
    main(folder_path, output_file_path)

