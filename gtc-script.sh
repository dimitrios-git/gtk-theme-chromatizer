#!/bin/bash
#
# This script is for colorizing the Yaru theme for GTK2, GTK3, and GTK4.
#
# 1. I will use the Yaru Colors repo for easy access to the theme's files.
# 2. I will extract the colors from the gtk.css file.
# 3. I will count the frequency of each color and identify the primary colors.
# 4. I will use the primary colors to colorize the theme.

# For the hexadecimal colors, we will use the following command:
grep -o -i "#[0-9A-Fa-f]\{6\}\b" gtk.css | sort | uniq -c | sort -nr > theme_colors_hex_freq.data.tmp

# For the rgb colors, we will use the following command:
grep -oE 'rgba?\([0-9]+, [0-9]+, [0-9]+(, [0-9.]+)?\)' gtk.css | sed 's/rgba(\([0-9]\{1,3\}, [0-9]\{1,3\}, [0-9]\{1,3\}\), [0-9.]\+)/rgb(\1)/' | sort | uniq -c |  sort -nr > theme_colors_rgb_freq.data.tmp

# We will now use the frequency.data.tmp to identify the primary colors.
# First, let's sort them by color:
python3 gtc-sort.py "theme_colors_hex_freq.data.tmp" > theme_colors_hex_freq_sorted.data.tmp
python3 gtc-sort.py "theme_colors_rgb_freq.data.tmp" > theme_colors_rgb_freq_sorted.data.tmp

# Now, we can identify the primary colors as the top colors in each color category.
# We can now use the primary colors to colorize the theme.
python3 gtc-replace-hex.py "theme_colors_hex_freq_sorted.data.tmp" > theme_colors_hex_sorted_target.data.tmp
python3 gtc-replace-rgb.py "theme_colors_rgb_freq_sorted.data.tmp" > theme_colors_rgb_sorted_target.data.tmp

# Now, we have all the hex and rgb colors of the original theme and the corresponding new colors we want to use.
# Lets use sed to replace the colors in the theme files.

python3 gtc-sed-hex.py
python3 gtc-sed-rgb.py

# Remove temporary files
# rm theme_colors*
