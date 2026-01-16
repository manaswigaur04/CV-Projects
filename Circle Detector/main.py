import cv2
import numpy as np
import os
import glob


def load_files(input_directory):
    
    image_extensions = ['*.jpg', '*.jpeg', '*.png']
    image_files_paths = []
    for ext in image_extensions:
        image_files_paths.extend(glob.glob(os.path.join(input_directory, ext)))
    
    return image_files_paths


def detect_circles():
    input_directory = "test_images"
    output_directory = "output_images"
    image_files_paths = load_files(input_directory)

    if len(image_files_paths) == 0:
        print(f"No images found in the given directory \"{input_directory}\"")
        return

    print(f"Found {len(image_files_paths)} images in the given image directory.")

    for image_paths in image_files_paths:
        filename = os.path.basename(image_paths)
        print(f"\nProcessing: {filename}")
        
        img = cv2.imread(image_paths)

        if img is None:
            print(f"Error: Could not read the image {image_paths}")
            continue

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_blurred_img = cv2.medianBlur(gray_img, 5)


        rows = gray_blurred_img.shape[0]
        circles = cv2.HoughCircles(
            gray_blurred_img, 
            cv2.HOUGH_GRADIENT, 
            dp=1, 
            minDist=rows / 8, 
            param1=100, 
            param2=30, 
            minRadius=20, 
            maxRadius=100
        )

        circle_count = len(circles)
        total_radius = sum(circles[0, :][2])
        
        output_img = img.copy()

        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            for i in circles[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                
                cv2.circle(output_img, center, radius, (0, 255, 0), 2)
                cv2.circle(output_img, center, 2, (0, 0, 255), 3)
    
                label = f"R={radius}"
                cv2.putText(output_img, label, (i[0] - 20, i[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        
        print(f"  Circles detected: {circle_count}")
        if circle_count > 0:
            avg_radius = total_radius / circle_count
            print(f"  Average radius: {avg_radius:.2f} pixels")

        output_path = os.path.join(output_directory, f"detected_{filename}")
        cv2.imwrite(output_path, output_img)

if __name__ == "__main__":
    detect_circles()
