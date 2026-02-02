import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os



def pencil_sketch(image_path, color, blur_kernel=21):
    """
    Apply pencil sketch effect to an image.
    
    Args:
        image_path (str): Path to the input image.
        color (bool): If True, apply colored sketch; if False, apply grayscale sketch.
        blur_kernel (int): Kernel size for Gaussian blur (default: 21).
    
    Returns:
        tuple: (sketched_image, original_image) or (None, None) if loading fails.
    """
    if color:
        pencil_sketch, img = pencil_sketch_color(image_path, blur_kernel=blur_kernel)
        return pencil_sketch, img
        
    else:
        pencil_sketch, img = pencil_sketch_grayscale(image_path, blur_kernel=blur_kernel)
        return pencil_sketch, img


def load_file(image_path):
    """
    Load an image from the specified file path.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        numpy.ndarray: Image as a uint8 array, or None if loading fails.
    """
    try:
        img = cv.imread(image_path).astype(np.uint8)
    except AttributeError as e:
        print(f"An error occurred reading the image file!\nReturning None")
        return(None)
    except Exception as e:
        print(f"An error occurred: {e} \nReturning None")
        return(None)

    if img is None:
        print("An error occurred regarding file path! \nReturning None")
        return(None)
    
    return img

def pencil_sketch_grayscale(image_path, blur_kernel=21):
    """
    Apply grayscale pencil sketch effect to an image.
    
    Args:
        image_path (str): Path to the input image.
        blur_kernel (int): Kernel size for Gaussian blur (default: 21).
    
    Returns:
        tuple: (sketched_image, original_image) or (None, None) if loading fails.
    """
    img = load_file(image_path)
    if img is None:
        return(None, None)
    
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    inverted_gray_img = 255-gray_img
    blurred_gray_img = cv.GaussianBlur(inverted_gray_img, (blur_kernel, blur_kernel), 0)
    inverted_blurred_img = 255-blurred_gray_img

    sketched_img = cv.divide(gray_img, inverted_blurred_img, scale=255)
    sketched_img = np.clip(sketched_img, 0, 255)
    sketched_img = cv.convertScaleAbs(sketched_img)

    return sketched_img, img


def pencil_sketch_color(image_path, blur_kernel=21):
    """
    Apply colored pencil sketch effect to an image.
    
    Args:
        image_path (str): Path to the input image.
        blur_kernel (int): Kernel size for Gaussian blur (default: 21).
    
    Returns:
        tuple: (sketched_image, original_image) or (None, None) if loading fails.
    """
    img = load_file(image_path)
    if img is None:
        return(None, None)
    
    
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv_img)

    inverted_v = 255 - v
    blurred_v = cv.GaussianBlur(inverted_v, (blur_kernel, blur_kernel), 0)
    inverted_blurred_v = 255 - blurred_v

    sketched_v = cv.divide(v, inverted_blurred_v, scale=255)
    sketched_v = np.clip(sketched_v, 0, 255)
    sketched_v = cv.convertScaleAbs(sketched_v)


    h_resized = cv.resize(h, (sketched_v.shape[1], sketched_v.shape[0]))
    s_resized = cv.resize((s * 0.9).astype(np.uint8), (sketched_v.shape[1], sketched_v.shape[0]))
    sketched_img = cv.merge((h_resized, s_resized, sketched_v))

    sketched_img = cv.cvtColor(sketched_img, cv.COLOR_HSV2BGR)

    return sketched_img, img




def display_result(original, sketch, color, save_path=None):
    """
    Display original and sketched images side by side, optionally saving the result.
    
    Args:
        original (numpy.ndarray): Original image in BGR format.
        sketch (numpy.ndarray): Sketched image (BGR if colored, grayscale if not).
        color (bool): If True, sketch is in BGR format; if False, grayscale.
        save_path (str, optional): Path to save the sketched image (default: None).
    """
    fig, (orig_plot, sketch_plot) = plt.subplots(ncols=2, figsize=(10, 5))
    if not color:
        sketch_temp = cv.cvtColor(sketch, cv.COLOR_GRAY2RGB)
    else:
        sketch_temp = cv.cvtColor(sketch, cv.COLOR_BGR2RGB)
    original_temp = cv.cvtColor(original, cv.COLOR_BGR2RGB)
    orig_plot.imshow(original_temp)
    sketch_plot.imshow(sketch_temp)

    orig_plot.set_title("Original Image")
    orig_plot.set_axis_off()
    sketch_plot.set_title("Sketched Image")
    sketch_plot.set_axis_off()
    
    plt.suptitle("Pencil Sketch Effect")
    plt.show()

    if save_path:
        cv.imwrite(save_path, sketch)


CONFIG_FILE = '.last_dir.txt' # A hidden file is a good choice

def get_last_dir():
    """
    Read the last accessed directory from config file.
    
    Returns:
        str: Last directory path, or user home directory if file not found.
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return f.read().strip()
    return os.path.expanduser("~")

def save_last_dir(directory):
    """
    Save the current directory to config file.
    
    Args:
        directory (str): Directory path to save.
    """
    with open(CONFIG_FILE, 'w') as f:
        f.write(directory)


def select_file():    
    """
    Open file dialog for user to select an image file and save the selection.
    """
    filetypes = (
        ('Images', '*.jpg'),
        ('Images', '*.png'),
        ('Images', '*.jpeg'),
        ('All files', '*.*')
    )
    last_dir = get_last_dir()

    global filepath
    filepath = filedialog.askopenfilename(
        title='Select a file...',
        initialdir=last_dir,
        filetypes=filetypes
    )

    if not filepath:
        print("File selection cancelled.")
    else:
        directory = os.path.dirname(filepath)
        save_last_dir(directory)



def toggle_color():
    """Toggle the color flag for sketch effect."""
    global color
    color = not color

def toggle_save():
    """Toggle the save flag for output image."""
    global save
    save = not save

def proceed():
    """
    Validate inputs and close the GUI window to proceed with sketch generation.
    """
    global blur_kernel
    if filepath=="":
        error_label.config(text="No file selected. Please select a file first.")
        return
    try:
        if entry.get()!='':
            blur_kernel = int(entry.get())
            if blur_kernel%2==0 or blur_kernel<=0:
                error_label.config(text="Blur kernel must be a positive odd integer.")
                return
    except Exception as e:
        print(f"Error: {e}")
    root.destroy()



def gui_inititalize():
    """
    Initialize and display the GUI window with controls for file selection,
    blur kernel input, and sketch options.
    """
    global root, entry, color, error_label
    root = ttk.Window(themename="superhero")
    root.title("Pencil Sketch Effect")
    root.geometry("300x400")
    
    label = ttk.Label(root, text="Click the button to open the file dialog.")
    label.pack(pady=20)
    
    open_button = ttk.Button(root, text="Open File", command=select_file)
    open_button.pack(pady=10)

    ttk.Label(root, text="Enter value of blur kernel (Leave empty for default):").pack(pady=5)
    entry = ttk.Entry(root)
    entry.pack(pady=5)


    toggle_color_button = ttk.Checkbutton(
        root,
        bootstyle="success, round-toggle",
        text="  Do you want a Coloured Sketch",
        command=toggle_color,
    )
    toggle_color_button.pack(pady=20)

    toggle_save_button = ttk.Checkbutton(
        root,
        bootstyle="success, round-toggle",
        text="  Do you want to save the output?",
        command=toggle_save,
    )
    toggle_save_button.pack(pady=20)

    error_label = ttk.Label(root, text="", foreground="red")
    error_label.pack(pady=1)

    proceed_button = ttk.Button(root, text="Proceed", command=proceed)
    proceed_button.pack(pady=1)
    
    root.mainloop()



def main():
    """
    Main entry point: initialize GUI, process user selections, and generate pencil sketch.
    """
    global filepath, color, blur_kernel, save
    filepath = ""
    blur_kernel = 21
    color = False
    save = False
    gui_inititalize()
    if filepath!="":
        sketch, original = pencil_sketch(filepath, color=color, blur_kernel=blur_kernel)
        if sketch is None:
            pass
        else:
            display_result(original, sketch, color=color, save_path= f'./output_sketches/{filepath.split("/")[-1].split(".")[0]}_sketch.png' if save else None)
    else:
        print("No file selected. Exiting program.")



if __name__=="__main__":
    main()