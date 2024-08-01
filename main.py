import tkinter as tk
from PIL import Image, ImageTk, ImageGrab, ImageDraw
import os
import time

# Initialize screenshot count and interaction variables
screenshot_count = 1
start_x = start_y = 0
start_time = 0

def take_screenshot(event=None):
    global screenshot_count, start_x, start_y, start_time
    
    # Calculate time and distance of mouse movement
    elapsed_time = time.time() - start_time
    distance = ((event.x - start_x) ** 2 + (event.y - start_y) ** 2) ** 0.5
    
    # Ignore if the click is on the close button or if it's a drag (moved more than 5 pixels in 200ms)
    if canvas.find_withtag(tk.CURRENT) and "close" in canvas.gettags(tk.CURRENT):
        return
    if elapsed_time > 0.2 or distance > 5:
        return
    
    # Remove topmost attribute and hide the main window while taking the screenshot
    root.attributes('-topmost', False)
    root.withdraw()
    
    # Create a fullscreen overlay to simulate the dimming effect
    overlay = tk.Toplevel(root)
    overlay.attributes('-fullscreen', True)
    overlay.attributes('-alpha', 0.3)  # Dim effect
    overlay.config(bg='black')
    overlay.lift()
    
    # Take screenshot
    root.after(200, lambda: capture_and_save_screenshot(overlay))

def capture_and_save_screenshot(overlay):
    global screenshot_count
    
    # Capture the screenshot
    screenshot = ImageGrab.grab()
    
    # Save the screenshot with a sequence number
    screenshot_path = os.path.join(os.getcwd(), f"screenshot_{screenshot_count}.png")
    screenshot.save(screenshot_path)
    
    # Increment the screenshot count for the next screenshot
    screenshot_count += 1
    
    # Remove the overlay
    overlay.destroy()
    
    # Show the main window again and restore topmost attribute
    root.deiconify()
    root.attributes('-topmost', True)

def close_window(event=None):
    root.destroy()

def start_move(event):
    global start_x, start_y, start_time
    start_x = event.x
    start_y = event.y
    start_time = time.time()
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_x() + (event.x - root.x)
    y = root.winfo_y() + (event.y - root.y)
    root.geometry(f"+{x}+{y}")

def create_circle(diameter, color):
    image = Image.new('RGBA', (diameter, diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse([0, 0, diameter, diameter], fill=color)
    return ImageTk.PhotoImage(image)

# Create the main window
root = tk.Tk()
root.title("")

# Remove title bar, make window transparent, and set it to be always on top
root.overrideredirect(True)
root.attributes('-transparentcolor', 'grey')
root.attributes('-topmost', True)

# Set the size of the window to a small circle
window_diameter = 100
root.geometry(f"{window_diameter}x{window_diameter}")

# Create a canvas to draw the circular window
canvas = tk.Canvas(root, width=window_diameter, height=window_diameter, bg='grey', highlightthickness=0)
canvas.pack()

# Create a smooth circle
circle_image = create_circle(window_diameter, "#4a90e2")
main_circle = canvas.create_image(0, 0, anchor=tk.NW, image=circle_image, tags="main")

# Load and resize the camera icon
icon_size = int(window_diameter * 0.6)
icon_path = os.path.join("images", "camera.png")
icon_image = Image.open(icon_path)
icon_image = icon_image.resize((icon_size, icon_size), Image.LANCZOS)
icon_photo = ImageTk.PhotoImage(icon_image)

# Add the camera icon to the center of the circle
icon_x = window_diameter // 2 - icon_size // 2
icon_y = window_diameter // 2 - icon_size // 2
canvas.create_image(icon_x, icon_y, anchor=tk.NW, image=icon_photo, tags="icon")

# Create a close button as a small red circle on the top right
close_diameter = 20
close_image = create_circle(close_diameter, "#ff0000")
close_button = canvas.create_image(window_diameter - close_diameter - 5, 5, anchor=tk.NW, image=close_image, tags="close")

# Bind events
canvas.tag_bind("main", "<ButtonRelease-1>", take_screenshot)
canvas.tag_bind("icon", "<ButtonRelease-1>", take_screenshot)
canvas.tag_bind("close", "<Button-1>", close_window)
canvas.bind("<Button-1>", start_move)
canvas.bind("<B1-Motion>", do_move)

# Run the application
root.mainloop()