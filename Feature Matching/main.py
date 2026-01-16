import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

def main():

    img1 = cv.imread('test_images/image1.jpg')
    img2 = cv.imread('test_images/image2.jpg')

    if img1 is None or img2 is None:
        print(f"Error loading images!")
        return

    img1_bw = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    img2_bw = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

    orb = cv.ORB_create()
    img1_keypoints, img1_descriptors = orb.detectAndCompute(img1_bw, None)
    img2_keypoints, img2_descriptors = orb.detectAndCompute(img2_bw, None)

    if img1_descriptors is None or img2_descriptors is None:
        print("No descriptors found!")
        return

    matcher = cv.BFMatcher()
    matches = matcher.match(img1_descriptors, img2_descriptors)
    matches = sorted(matches, key=lambda x: x.distance)

    good_matches = matches[:50]

    print(f"Found {len(matches)} total matches.")

    output_img = cv.drawMatches(img1, img1_keypoints, img2, img2_keypoints, good_matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    plt.figure(figsize=(12, 6))
    plt.imshow(cv.cvtColor(output_img, cv.COLOR_BGR2RGB))
    plt.title('ORB Feature Matching')
    plt.annotate('Image 1', xy=(0.25, 0.95), xycoords='axes fraction', fontsize=12, ha='center')
    plt.annotate('Image 2', xy=(0.75, 0.95), xycoords='axes fraction', fontsize=12, ha='center')
    plt.annotate(f"Total Matches: {len(matches)}", xy=(0.5, 0.05), xycoords='axes fraction', fontsize=12, ha='center')
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()