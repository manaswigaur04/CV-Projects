import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog



def pencil_sketch(image_path, color, blur_kernel=21):
    img = cv.imread(image_path)

    if img is None:
        print("An error occurred regarding file path! \n Returning None")
        return(None, None)
    if blur_kernel%2==0:
        print("Value of blur_kernel should be an odd integer!")
        return (None, None)
    
    if color:
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
    else:
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        inverted_gray_img = 255-gray_img
        blurred_gray_img = cv.GaussianBlur(inverted_gray_img, (blur_kernel, blur_kernel), 0)
        inverted_blurred_img = 255-blurred_gray_img

        sketched_img = cv.divide(gray_img, inverted_blurred_img, scale=255)
        sketched_img = np.clip(sketched_img, 0, 255)
        sketched_img = cv.convertScaleAbs(sketched_img)

        return sketched_img, img




def display_result(original, sketch, color, save_path=None):
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



def select_file():    
    filetypes = (
        ('Images', '*.jpg'),
        ('All files', '*.*')
    )

    global filepath
    filepath = filedialog.askopenfilename(
        title='Select a file...',
        initialdir='/',
        filetypes=filetypes
    )

    if not filepath:
        print("File selection cancelled.")




def colored_sketch_button():
    try:
        global blur_kernel, color
        color = True
        if entry.get()!='':
            blur_kernel = int(entry.get())
        root.destroy()
    except Exception as e:
        print(f"Error: {e}")
def grayscale_sketch_button():
    try:
        global blur_kernel, color
        color = False
        if entry.get()!='':
            blur_kernel = int(entry.get())
        
        root.destroy()
    except Exception as e:
        print(f"Error: {e}")




def gui_inititalize():
    global root, entry
    root = tk.Tk()
    root.title("File Picker GUI")
    root.geometry("300x400")
    
    label = tk.Label(root, text="Click the button to open the file dialog.")
    label.pack(pady=20)
    
    open_button = tk.Button(root, text="Open File", command=select_file)
    open_button.pack(pady=10)

    label = tk.Label(root, text="Do you want a coloured sketch or a greyscale sketch?")
    label.pack(pady=20)

    tk.Label(root, text="Enter value of blur kernel (Leave empty for default):").pack(pady=5)
    entry = tk.Entry(root)
    entry.pack(pady=5)

    tk.Label(root, text="Do you want a coloured sketch?").pack(pady=20)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    yes_button = tk.Button(button_frame, text="Yes", command=colored_sketch_button)
    
    yes_button.pack(side=tk.LEFT, padx=5)

    no_button = tk.Button(button_frame, text="No", command=grayscale_sketch_button)
    
    no_button.pack(side=tk.LEFT, padx=5)
    root.mainloop()



def main():
    global filepath, color, blur_kernel
    filepath = ""
    blur_kernel = 21
    color = False
    gui_inititalize()
    if filepath!="":
        sketch, original = pencil_sketch(filepath, color=color, blur_kernel=blur_kernel)
        if sketch is None:
            pass
        else:
            display_result(original, sketch, color=color, save_path=f'./output_sketches/{filepath.split("/")[-1].split(".")[0]}_sketch.png')
    else:
        print("No file selected. Exiting program.")

if __name__=="__main__":
    main()