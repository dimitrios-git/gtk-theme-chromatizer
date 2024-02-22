import colorsys

# Target colors for demonstration
target_colors = {
    'reds': '#f90000',
    'yellows': '#808000',
    'greens': '#009100', # This is the accent color
    'cyans': '#00c9c9',
    'blues': '#6868ff',
    'magentas': '#db00db',
    'grays': '#000000' # This is the background color
}

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def rgb_to_hls(rgb_color):
    return colorsys.rgb_to_hls(*rgb_color)

def determine_category(hex_color):
    rgb = hex_to_rgb(hex_color)
    h, l, s = rgb_to_hls(rgb)

    if s < 0.1 and 0.1 < l < 0.9:  # Consider as gray if low saturation and not too dark or light
        return 'grays'
    elif h < 1/12 or h >= 11/12:
        return 'reds'
    elif h < 3/12:
        return 'yellows'
    elif h < 5/12:
        return 'greens'
    elif h < 7/12:
        return 'cyans'
    elif h < 9/12:
        return 'blues'
    elif h < 11/12:
        return 'magentas'
    return 'unknown'

# Define target_colors, hex_to_rgb, rgb_to_hex, and other necessary functions

def calculate_color_differences(base_color, other_color):
    """Calculate differences in hue, saturation, and lightness between two colors."""
    base_hls = colorsys.rgb_to_hls(*[x / 255.0 for x in base_color])
    other_hls = colorsys.rgb_to_hls(*[x / 255.0 for x in other_color])
    return (
        other_hls[0] - base_hls[0],  # Hue difference
        other_hls[1] - base_hls[1],  # Lightness difference
        other_hls[2] - base_hls[2],  # Saturation difference
    )

def adjust_color(base_color, differences):
    """Adjust base color using the provided hue, lightness, and saturation differences."""
    base_hls = colorsys.rgb_to_hls(*[x / 255.0 for x in base_color])
    adjusted_hls = (
        max(0, min(1, base_hls[0] + differences[0])),  # Adjusted hue
        max(0, min(1, base_hls[1] + differences[1])),  # Adjusted lightness
        max(0, min(1, base_hls[2] + differences[2])),  # Adjusted saturation
    )
    adjusted_rgb = colorsys.hls_to_rgb(*adjusted_hls)
    return tuple(int(x * 255) for x in adjusted_rgb)


def process_file(input_file, output_file):
    current_category = None
    base_color = None
    differences = []
    is_first_category = True  # Flag to check if it's the first category

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()

            if line.startswith('[') and line.endswith(']'):  # Category header
                # Process the previous category
                if current_category and base_color and differences:
                    target_rgb = hex_to_rgb(target_colors.get(current_category.lower(), '#000000'))
                    for diff in differences:
                        new_color_rgb = adjust_color(target_rgb, diff)
                        outfile.write(f"  {rgb_to_hex(new_color_rgb)}\n")
                
                if not is_first_category:
                    # Add a newline before the next category header, if it's not the first
                    outfile.write("\n")
                else:
                    # After writing the first category, set the flag to False
                    is_first_category = False

                current_category = line[1:-1].lower()  # Update current category in lowercase
                base_color = None
                differences = []
                outfile.write(f"{line}\n")  # Write the category header to the output file
                continue

            if line:
                freq, hex_color = line.split(' ')
                rgb_color = hex_to_rgb(hex_color)
                
                if base_color is None:  # First color in the category
                    base_color = rgb_color
                    target_rgb = hex_to_rgb(target_colors.get(current_category.lower(), '#000000'))
                    outfile.write(f"  {freq} {rgb_to_hex(target_rgb)}\n")  # Write the adjusted base color
                else:
                    diff = calculate_color_differences(base_color, rgb_color)
                    differences.append(diff)

        # Process the last category
        if current_category and base_color and differences:
            target_rgb = hex_to_rgb(target_colors[current_category.lower()])
            for diff in differences:
                new_color_rgb = adjust_color(target_rgb, diff)
                outfile.write(f"  {rgb_to_hex(new_color_rgb)}\n")

if __name__ == '__main__':
    input_file = 'theme_colors_hex_freq_sorted.data'
    output_file = 'theme_colors_hex_freq_sorted_target.data'
    process_file(input_file, output_file)

