#!/usr/bin/env python3

import argparse
import math
import sys
import os
import random
from PIL import Image, ImageFilter, ImageOps
import svgwrite
from svgwrite import Drawing
import re

def print_progress(progress, message=""):
    """Print a simple progress bar."""
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    sys.stdout.write(f'\r{message} [{bar}] {int(progress * 100)}%')
    sys.stdout.flush()

def create_squiggles_svg(image, rows, cols, freq, amp, bidi=False, connect_ends=False):
    """Create squiggly paths as SVG."""
    width = image.width
    height = image.height
    
    # Calculate amplitude divisor
    divisors = [128, 64, 32, 16, 8, 4]
    sq_divisor = divisors[amp - 1]
    sq_max = 256 / sq_divisor
    
    # Create SVG drawing
    dwg = Drawing(size=(width, height))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill='white'))
    
    # Set random seed for reproducibility
    random.seed(42)
    
    for y in range(rows):
        print_progress(y / rows, "Generating squiggles")
        cy = (height / rows * (y + 1)) - (height / rows / 2)
        xinc = width / (cols - 1)
        
        start_x = 0
        end_x = cols - 1
        step_x = 1
        
        if bidi and y % 2 != 0:
            start_x = cols - 2
            end_x = -1
            xinc *= -1
            step_x = -1
        
        points = []
        for x in range(start_x, end_x, step_x):
            # Get base amplitude from image
            base_amp = sq_max - image.getpixel((x * (width / cols), y * (height / rows))) / sq_divisor
            if bidi and y % 2 != 0:
                base_amp *= -1
            
            # Calculate points for this segment
            for sq in range(freq):
                t = sq / freq
                x1 = x * xinc + (t * xinc / freq)
                
                # Add multiple sine waves with different frequencies and random phase
                y1 = cy
                # Main sine wave
                y1 += base_amp * math.sin(t * math.pi)
                # Secondary sine wave with higher frequency
                y1 += base_amp * 0.3 * math.sin(t * math.pi * 2 + random.uniform(0, math.pi))
                # Random noise
                y1 += base_amp * 0.2 * random.uniform(-1, 1)
                
                points.append((x1, y1))
        
        # Create path
        if points:
            path_data = f"M {points[0][0]:.2f} {points[0][1]:.2f}"
            for point in points[1:]:
                path_data += f" L {point[0]:.2f} {point[1]:.2f}"
            dwg.add(dwg.path(d=path_data, stroke='black', stroke_width=1, fill='none'))
    
    print_progress(1.0, "Generating squiggles")
    print()  # New line after progress bar
    return dwg

def process_image(image_path, rows, cols, invert=False):
    """Process an image and return a PIL Image object."""
    print_progress(0, "Loading image")
    im = Image.open(image_path)
    im = im.convert('RGBA')
    print_progress(0.2, "Processing image")
    
    # Create white image to paste over in case of transparency
    white_im = Image.new('RGBA', im.size, (255, 255, 255))
    tmp_im = Image.alpha_composite(white_im, im)
    print_progress(0.4, "Processing image")
    
    # Convert to grayscale and blur it
    im = tmp_im.convert('L')
    if invert:
        im = ImageOps.invert(im)
    im = im.filter(ImageFilter.GaussianBlur)
    print_progress(0.6, "Processing image")
    
    # Resize to match the grid
    tmp_im = im.resize((cols, rows))
    im = tmp_im.resize((im.width + 1, im.height + 1), Image.LANCZOS)
    print_progress(1.0, "Processing image")
    print()  # New line after progress bar
    
    return im

def process_image_cmyk(image_path, rows, cols, invert=False):
    """Process an image and return CMYK channels as PIL Image objects."""
    print_progress(0, "Loading image")
    im = Image.open(image_path)
    im = im.convert('RGBA')
    print_progress(0.2, "Processing image")
    
    # Create white image to paste over in case of transparency
    white_im = Image.new('RGBA', im.size, (255, 255, 255, 255))
    tmp_im = Image.alpha_composite(white_im, im)
    print_progress(0.4, "Processing image")
    
    # Convert to CMYK and split image
    im = tmp_im.convert('CMYK')
    c, m, y, k = im.split()
    print_progress(0.6, "Processing image")
    
    if invert:
        c = ImageOps.invert(c)
        m = ImageOps.invert(m)
        y = ImageOps.invert(y)
        k = ImageOps.invert(k)
    
    # Invert to make sure color separations are correct
    c = ImageOps.invert(c.convert('L'))
    m = ImageOps.invert(m.convert('L'))
    y = ImageOps.invert(y.convert('L'))
    k = ImageOps.invert(k.convert('L'))
    print_progress(0.8, "Processing image")
    
    # Resize each channel
    c = c.resize((cols, rows)).resize((im.width + 1, im.height + 1), Image.LANCZOS)
    m = m.resize((cols, rows)).resize((im.width + 1, im.height + 1), Image.LANCZOS)
    y = y.resize((cols, rows)).resize((im.width + 1, im.height + 1), Image.LANCZOS)
    k = k.resize((cols, rows)).resize((im.width + 1, im.height + 1), Image.LANCZOS)
    print_progress(1.0, "Processing image")
    print()  # New line after progress bar
    
    return c, m, y, k

def main():
    parser = argparse.ArgumentParser(description='Convert images to squiggly paths')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('output', help='Output SVG file path')
    parser.add_argument('--rows', type=int, default=50, help='Number of rows (10-200)')
    parser.add_argument('--cols', type=int, default=50, help='Number of columns (10-200)')
    parser.add_argument('--freq', type=int, default=2, help='Squiggle frequency (1-6)')
    parser.add_argument('--amp', type=int, default=2, help='Squiggle amplitude (1-6)')
    parser.add_argument('--invert', action='store_true', help='Invert colors')
    parser.add_argument('--path-type', choices=['uni', 'bidi', 'join'], default='uni',
                      help='Path direction: uni (left-to-right), bidi (back-and-forth), join (back-and-forth with joined ends)')
    parser.add_argument('--color-mode', choices=['gray', 'cmyk'], default='gray',
                      help='Color mode: gray (single color) or cmyk (color separation)')
    
    args = parser.parse_args()
    
    # Validate arguments
    args.rows = max(10, min(200, args.rows))
    args.cols = max(10, min(200, args.cols))
    args.freq = max(1, min(6, args.freq))
    args.amp = max(1, min(6, args.amp))
    
    # Set path parameters
    bidi = args.path_type in ['bidi', 'join']
    connect_ends = args.path_type == 'join'
    
    try:
        if args.color_mode == 'gray':
            print(f"Processing image in grayscale mode")
            # Process image in grayscale mode
            image = process_image(args.input, args.rows, args.cols, args.invert)
            dwg = create_squiggles_svg(image, args.rows, args.cols, args.freq, args.amp, bidi, connect_ends)
        else:
            print(f"Processing image in CMYK mode")
            # Process image in CMYK mode
            c, m, y, k = process_image_cmyk(args.input, args.rows, args.cols, args.invert)
            
            # Create SVG drawing
            dwg = Drawing(size=(c.width, c.height))
            dwg.add(dwg.rect(insert=(0, 0), size=(c.width, c.height), fill='white'))
            
            # Process each channel
            colors = {
                'cyan': ('#00ffff', c),
                'magenta': ('#ff00ff', m),
                'yellow': ('#ffff00', y)
            }
            
            for i, (color_name, (color, channel)) in enumerate(colors.items()):
                print(f"\nProcessing {color_name} channel...")
                channel_dwg = create_squiggles_svg(channel, args.freq, args.amp, bidi, connect_ends)
                # Add paths with color
                for path in channel_dwg.elements:
                    if isinstance(path, svgwrite.path.Path):
                        path['stroke'] = color
                        dwg.add(path)
        
        print("\nSaving SVG file...")
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        
        # Save SVG file
        dwg.saveas(args.output)
        
        # Verify the file was created and has content
        if os.path.exists(args.output):
            file_size = os.path.getsize(args.output)
            print(f"File saved successfully. Size: {file_size} bytes")
            if file_size == 0:
                print("Warning: File is empty!")
        else:
            print("Error: File was not created!")
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise
    
    print("Done!")
    print(f"open {args.output}")

if __name__ == '__main__':
    main()
    # Must be run as:
    # python cli_squiggledraw.py input.png output.svg --rows 100 --cols 100 --freq 3 --amp 2 --path-type bidi --color-mode gray
