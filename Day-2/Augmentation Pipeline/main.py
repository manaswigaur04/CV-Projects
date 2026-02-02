import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def load_images(folder_path):
    images = []
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            img_path = folder_path + '/' + filename
            if os.path.isfile(img_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img = cv2.imread(img_path)
                if img is not None:
                    images.append((filename, img))
    return images

def apply_augmentations(image):
    augmentations = {}
    height, width = image.shape[:2]
    
    augmentations['Flipped Horizontally'] = cv2.flip(image, 1)
    augmentations['Flipped Vertically'] = cv2.flip(image, 0)
    augmentations['Flipped Horizontally and Vertically'] = cv2.flip(image, -1)
    
    augmentations['Rotated 45 Degrees'] = cv2.warpAffine(image, cv2.getRotationMatrix2D((width // 2, height // 2), 45, 1.0), (width, height))
    augmentations['Rotated 90 Degrees'] = cv2.warpAffine(image, cv2.getRotationMatrix2D((width // 2, height // 2), 90, 1.0), (width, height))
    
    scale_factor = 1.7
    scaled = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    start_y, start_x = (scaled.shape[0] - height) // 2, (scaled.shape[1] - width) // 2
    augmentations['Zoomed In'] = scaled[start_y:start_y+height, start_x:start_x+width]
    
    scale_factor = 0.7
    scaled_down = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    pad_y, pad_x = (height - scaled_down.shape[0]) // 2, (width - scaled_down.shape[1]) // 2
    augmentations['Zoomed Out'] = cv2.copyMakeBorder(scaled_down, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    tx, ty = 50, 30
    augmentations['Translated'] = cv2.warpAffine(image, np.float32([[1, 0, tx], [0, 1, ty]]), (width, height))
    
    shear_matrix = np.float32([[1, 0.2, 0], [0, 1, 0]])
    augmentations['Sheared'] = cv2.warpAffine(image, shear_matrix, (width, height))
    
    augmentations['Brighter'] = np.clip(image.astype(np.int16) + 50, 0, 255).astype(np.uint8)
    
    augmentations['High Contrast'] = np.clip(image.astype(np.float32) * 1.5, 0, 255).astype(np.uint8)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv_sat = hsv.copy()
    hsv_sat[:, :, 1] = np.clip(hsv_sat[:, :, 1] * 1.5, 0, 255)
    augmentations['More Saturated'] = cv2.cvtColor(hsv_sat.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    hsv_hue = hsv.copy()
    hsv_hue[:, :, 0] = (hsv_hue[:, :, 0] + 30) % 180
    augmentations['Hue Shifted'] = cv2.cvtColor(hsv_hue.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    return augmentations

def main():
    input_folder = "test_images"
    images = load_images(input_folder)
    
    if len(images) == 0:
        print("No images found.")
        return

    for filename, img in images:
        print(f"Starting augmentations for {filename}.")
        results = apply_augmentations(img)
        
        fig, ax = plt.subplots(3, 5, figsize=(20, 10))
        fig.suptitle(f"Augmentations")
        ax = ax.ravel()
        
        ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax[0].set_title("Original")
        
        names = list(results.keys())
        
        for i in range(len(names)):
            if i + 1 < len(ax):
                aug_img = results[names[i]]
                ax[i + 1].imshow(cv2.cvtColor(aug_img, cv2.COLOR_BGR2RGB))
                ax[i + 1].set_title(names[i])
        
        for j in range(len(ax)):
            ax[j].axis('off')

        plt.savefig(f"output_images/augmented_{filename}")
        plt.close(fig)
        print(f"Finished augmentations for {filename}.")


if __name__ == "__main__":
    main()
