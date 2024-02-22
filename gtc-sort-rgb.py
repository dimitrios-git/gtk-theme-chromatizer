import colorsys

def parse_rgb(rgb_string):
    # Remove 'rgb' prefix and extract the numeric values
    rgb_string = rgb_string.strip("rgb()")
    return tuple(map(int, rgb_string.split(',')))

def rgb_to_hls(rgb_color):
    # Normalize RGB values to [0, 1] range and convert to HLS
    normalized_rgb = tuple(value / 255.0 for value in rgb_color)
    return colorsys.rgb_to_hls(*normalized_rgb)

def categorize_and_sort_colors(rgb_colors):
    categorized = {}
    for freq, rgb_string in rgb_colors:
        rgb = parse_rgb(rgb_string)
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
        categorized[category].append((freq, rgb_string, hls))

    # Sort each category by lightness and saturation
    for category in categorized:
        categorized[category].sort(key=lambda x: (x[2][1], -x[2][2]))  # Sort primarily by lightness, then by saturation inversely

    return categorized

def read_colors(file_path):
    with open(file_path, 'r') as file:
        # Initialize an empty list to hold tuples of (frequency, RGB color string)
        rgb_colors = []
        for line in file:
            if line.strip():  # Ensure the line is not empty
                parts = line.strip().split(maxsplit=1)
                frequency = parts[0]
                rgb_part = parts[1]
                # Format the RGB part as needed for the rest of your code
                rgb_string = f"rgb({rgb_part})"
                rgb_colors.append((frequency, rgb_string.lower()))
    return rgb_colors

def main():
    file_path = 'theme_colors_rgb_freq.data'
    rgb_colors = read_colors(file_path)
    categorized_colors = categorize_and_sort_colors(rgb_colors)

    for category, color_list in categorized_colors.items():
        print(f"[{category.capitalize()}]")
        for freq, rgb_string, _ in color_list:
            print(f"{freq} {rgb_string}")
        print()

if __name__ == '__main__':
    main()

