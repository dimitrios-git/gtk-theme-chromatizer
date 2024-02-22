import colorsys

def hex_to_rgb(hex_color):
    # Convert a hex color to an RGB tuple
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hls(rgb_color):
    # Convert an RGB tuple to HLS
    return colorsys.rgb_to_hls(*rgb_color)

def categorize_and_sort_colors(colors):
    categorized = {}
    for freq, hex_color in colors:
        rgb = hex_to_rgb(hex_color)
        hls = rgb_to_hls(rgb)
        hue, lightness, saturation = hls

        # Check for low saturation to identify grays
        if saturation < 0.1 and lightness > 0.1:
            category = 'grays'
        else:
            # Categorize by hue
            if hue < 1/12 or hue >= 11/12:
                category = 'reds'
            elif hue < 3/12:
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
        categorized[category].append((freq, hex_color, hls))

    # Sort each category by lightness and saturation
    for category in categorized:
        categorized[category].sort(key=lambda x: (x[2][1], -x[2][2]))  # Sort primarily by lightness, then by saturation inversely

    return categorized

def read_colors(file_path):
    with open(file_path, 'r') as file:
        # Initialize an empty list to hold tuples of (frequency, hex color)
        colors = []
        for line in file:
            if line.strip():  # Ensure the line is not empty
                parts = line.strip().split(maxsplit=1)
                frequency = parts[0]
                hex_color = parts[1].lower()
                colors.append((frequency, hex_color))
    return colors

def main():
    file_path = 'theme_colors_hex_freq.data'
    colors = read_colors(file_path)
    categorized_colors = categorize_and_sort_colors(colors)

    for category, color_list in categorized_colors.items():
        print(f"[{category.capitalize()}]")
        for freq, hex_color, _ in color_list:
            print(f"{freq} {hex_color}")
        print()

if __name__ == '__main__':
    main()

