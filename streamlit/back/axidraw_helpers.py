from pyaxidraw import axidraw
import os

def draw_svg(svg_path, speed_pendown=50, skip_draw=False):
    print("Trying to draw SVG...")
    ad = axidraw.AxiDraw() # Initialize class
    ad.interactive()            # Enter interactive mode
    connected = ad.connect()    # Open serial port to AxiDraw
    if not connected:
        print("Error: Could not connect to AxiDraw")
        return "error", 0
    ad.moveto(0, 0)             # Move to the origin
    ad.plot_setup(svg_path)   # plot the document
    ad.options.preview = skip_draw
    #ad.options.report_time = False # Enable time and distance estimates
    ad.options.speed_pendown = speed_pendown # Set maximum pen-down speed to 50%
    ad.plot_run()   # plot the document
    drawing_time_seconds = ad.time_estimate
    return "completed", drawing_time_seconds

def clean_svg(input_svg, output_svg):
    os.system(f'/Applications/Inkscape.app/Contents/MacOS/inkscape {input_svg} --export-plain-svg={output_svg}  --actions="select-all;object-to-path;export-do"')
    return