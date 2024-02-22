import colorsys
import sys

def parse_color(color_string):
    if '#' in color_string:
        # It's a hex color
        hex_color = color_string.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    else:
        # It's an RGB color in 'rgb(R,G,B)' format
        color_string = color_string.strip("rgb()")
        return tuple(int(value) / 255.0 for value in color_string.split(','))

def rgb_to_hls(rgb_color):
    return colorsys.rgb_to_hls(*rgb_color)

def categorize_and_sort_colors(colors):
    categorized = {}
    for freq, color_string in colors:
        rgb = parse_color(color_string)
        hls = rgb_to_hls(rgb)
        hue, lightness, saturation = hls

        # Check for low saturation to identify grays, considering both very light and very dark colors
        if saturation < 0.1 or lightness < 0.1 or lightness > 0.9:
            category = 'grays'
        else:
            # Categorize by hue with a more precise range for yellows to avoid capturing grays
            if hue < 1/12 or hue >= 11/12:
                category = 'reds'
            elif 1/12 <= hue < 1/6:  # More precise range for yellows
                category = 'yellows'
            elif hue < 5/12:
                category = 'greens'
            elif hue < 7/12:
                category = 'cyans'
            elif hue < 9/12:
                category = 'blues'
            elif hue < 11/12:
                category = 'magentas'
            else:
                category = 'unknown'

        if category not in categorized:
            categorized[category] = []
        categorized[category].append((int(freq), color_string, hls))

    # Sort each category by frequency (descending), then by lightness and saturation
    for category in categorized:
        categorized[category].sort(key=lambda x: (-x[0], x[2][1], -x[2][2]))

    return categorized

def read_colors(file_path):
    try:
        with open(file_path, 'r') as file:
            colors = []
            for line in file:
                if line.strip():
                    parts = line.strip().split(maxsplit=1)
                    frequency = parts[0]
                    color_string = parts[1].lower()
                    colors.append((frequency, color_string))
            return colors
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(2)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(3)

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    colors = read_colors(file_path)
    if not colors:
        print("No colors found in the file.")
        sys.exit(4)
    categorized_colors = categorize_and_sort_colors(colors)

    if not categorized_colors:
        print("No colors were categorized.")
        sys.exit(5)

    for category, color_list in categorized_colors.items():
        print(f"[{category.capitalize()}]")
        for freq, color_string, _ in color_list:
            print(f"{freq} {color_string}")
        print()

if __name__ == '__main__':
    main()

