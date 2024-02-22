import re
import subprocess

def generate_sed_commands(original_file, target_file):
    with open(original_file, 'r') as orig, open(target_file, 'r') as targ:
        orig_lines = orig.readlines()
        targ_lines = targ.readlines()

        for orig_line, targ_line in zip(orig_lines, targ_lines):
            orig_line = orig_line.strip()
            targ_line = targ_line.strip()

            # Skip category headers and empty lines
            if orig_line.startswith('[') or orig_line == '' or targ_line.startswith('[') or targ_line == '':
                continue

            # Use regular expression to extract RGB values
            orig_rgb = re.search(r'rgb\((.*?)\)', orig_line).group(1)
            targ_rgb = re.search(r'rgb\((.*?)\)', targ_line).group(1)

            # Generate sed command to replace the original RGB value with the target RGB value
            sed_command = f"sed -i 's/{orig_rgb}/{targ_rgb}/g' gtk.css"

            # Execute the sed command
            subprocess.run(sed_command, shell=True)

# Example usage for RGB color files
generate_sed_commands('theme_colors_rgb_freq_sorted.data', 'theme_colors_rgb_freq_sorted_target.data')

