import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def pencil_sketch(image_path, color=True, blur_kernel=21):
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

        # Combine channels with slight desaturation
        # Ensure all channels have the same size
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

    _, (orig_plot, sketch_plot) = plt.subplots(ncols=2)
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
    
    

def main():
    image_path = 'test_images/sample2.jpg'
    color = True
    sketch, original = pencil_sketch(image_path, color=color, blur_kernel=21)
    if sketch is None:
        pass
    else:
        display_result(original, sketch, color=color, save_path=f'./output_sketches/{image_path.split("/")[-1].split(".")[0]}_sketch.png')

if __name__=="__main__":
    main()