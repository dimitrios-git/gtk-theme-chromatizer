import colorsys

# Target colors for demonstration
target_colors = {
    'reds': 'rgb(249, 0, 0)',
    'yellows': 'rgb(128, 128, 0)',
    'greens': 'rgb(0, 145, 0)',  # This is the accent color
    'cyans': 'rgb(0, 201, 201)',
    'blues': 'rgb(104, 104, 255)',
    'magentas': 'rgb(219, 0, 219)',
    'grays': 'rgb(0, 0, 0)' # This is the background color
}

def parse_rgb_string(rgb_string):
    """
    Parse an RGB string in the format 'rgb(R, G, B)' and return a tuple of integers (R, G, B).
    """
    rgb_values = rgb_string.strip('rgb()').split(',')
    return tuple(int(value.strip()) for value in rgb_values)

def rgb_to_rgb_string(rgb_color):
    """
    Format an RGB tuple of integers (R, G, B) into a string 'rgb(R, G, B)'.
    """
    return 'rgb({0}, {1}, {2})'.format(*rgb_color)

def rgb_to_hls(rgb_color):
    return colorsys.rgb_to_hls(*rgb_color)

def determine_category(rgb_color):
    h, l, s = rgb_to_hls([x / 255.0 for x in rgb_color])  # Convert RGB to HLS

    if s < 0.1 and 0.1 < l < 0.9:
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

def adjust_color(base_color, differences):
    base_hls = colorsys.rgb_to_hls(base_color[0] / 255.0, base_color[1] / 255.0, base_color[2] / 255.0)
    new_h = max(0, min(1, base_hls[0] + differences[0]))
    new_l = max(0, min(1, base_hls[1] + differences[1]))
    new_s = max(0, min(1, base_hls[2] + differences[2]))
    adjusted_rgb = colorsys.hls_to_rgb(new_h, new_l, new_s)
    return tuple(int(x * 255) for x in adjusted_rgb)

def calculate_color_differences(base_color, other_color):
    base_hls = colorsys.rgb_to_hls(base_color[0] / 255.0, base_color[1] / 255.0, base_color[2] / 255.0)
    other_hls = colorsys.rgb_to_hls(other_color[0] / 255.0, other_color[1] / 255.0, other_color[2] / 255.0)
    h_diff = other_hls[0] - base_hls[0]
    l_diff = other_hls[1] - base_hls[1]
    s_diff = other_hls[2] - base_hls[2]
    return (h_diff, l_diff, s_diff)

def process_file(input_file, output_file):
    current_category = None
    base_color = None
    differences = []
    is_first_category = True

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()

            if line.startswith('[') and line.endswith(']'):
                if current_category and base_color and differences:
                    target_rgb = parse_rgb_string(target_colors.get(current_category.lower(), 'rgb(0, 0, 0)'))
                    for diff in differences:
                        new_color_rgb = adjust_color(target_rgb, diff)
                        outfile.write(f"  {rgb_to_rgb_string(new_color_rgb)}\n")
                
                if not is_first_category:
                    outfile.write("\n")
                else:
                    is_first_category = False

                current_category = line[1:-1].lower()
                base_color = None
                differences = []
                outfile.write(f"{line}\n")
                continue

            if line:
                freq, rgb_values = line.split(' ', 1)
                rgb_values = rgb_values.replace('rgb(', '').replace(')', '')
                rgb_color = tuple(map(int, rgb_values.split(',')))

                if base_color is None:
                    base_color = rgb_color
                    target_rgb = parse_rgb_string(target_colors.get(current_category.lower(), 'rgb(0, 0, 0)'))
                    outfile.write(f"  {freq} {rgb_to_rgb_string(target_rgb)}\n")
                else:
                    diff = calculate_color_differences(base_color, rgb_color)
                    differences.append(diff)

        if current_category and base_color and differences:
            target_rgb = parse_rgb_string(target_colors[current_category.lower()])
            for diff in differences:
                new_color_rgb = adjust_color(target_rgb, diff)
                outfile.write(f"  {rgb_to_rgb_string(new_color_rgb)}\n")

if __name__ == '__main__':
    input_file = 'theme_colors_rgb_freq_sorted.data'
    output_file = 'theme_colors_rgb_freq_sorted_target.data'
    process_file(input_file, output_file)

