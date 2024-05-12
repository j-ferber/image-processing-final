# Authors: Justin Chen, Justin Ferber, Joseph Stefanoni
# CPE 462 Final Project
# Description: This program allows users to make various image enhancements to an image they input

import cv2 as cv
import sys
import numpy as np
import os

def showImage(windowTitle, newImage):
    cv.imshow(windowTitle, newImage)
    cv.waitKey(0)
    cv.destroyAllWindows()

def main(): # Run with "python main.py imageName"
    if (len(sys.argv) != 2):
        print("Usage: python main.py <input_image>")
        exit()
    input_image = sys.argv[1]

    image = cv.imread(input_image)
    image = cv.resize(image, (800, 600))
    newImage = image.copy()
    prevImage = image.copy()
    windowTitle = "Input Image"
    while True:
        showImage(windowTitle, newImage)
        userChoice = input("What type of image processing would you like to do (just enter the number)?\n1. Gaussian Blur\n2. Speckle Noise\n3. Adjust Contrast/Brightness\n4. Sharpen Image\n5. Adjust Saturation\n6. Apply Bilateral Filter (smoothes image & preserves edges)\n7. Adjust Hue\n8. Reverse Last Step (only works for 1 step)\n9. Exit\n10. Save Image to File\nEnter choice: ")
        match userChoice:
            case "1":
                blurScale = int(input("Enter the blur scale (must be an odd number): "))
                while (blurScale % 2 == 0):
                    blurScale = input("Please enter a valid blur scale (must be an odd number): ")
                prevImage = newImage.copy()
                newImage = cv.GaussianBlur(newImage, (blurScale, blurScale), 0)
                windowTitle = "Gaussian Blur"
            case "2":
                prevImage = newImage.copy()
                intensity = float(input("Enter intensity value (0-100): "))
                intensity /= 100
                img_array = np.array(newImage)
                spackle_noise = np.random.rand(*img_array.shape) < intensity
                noisy_image = np.copy(img_array)
                noisy_image[spackle_noise] = 255
                newImage = noisy_image
                print("Adding speckle noise to the image...")
            case "3":
                try:
                    alpha = float(input("Enter the alpha value [0-3] (0-1 lowers contrast, 1-3 brightens it): "))
                    beta = int(input("Enter the beta value [-100 - 100] (below 0 lowers brightness, positive increase brightness): "))
                    prevImage = newImage.copy()
                    newImage = cv.convertScaleAbs(newImage, alpha=alpha, beta=beta)
                    windowTitle = "Contrast/Brightness Adjustment"
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            case "4":
                kernel_sharpening = np.array([[-1,-1,-1],
                                            [-1, 9,-1],
                                            [-1,-1,-1]])
                prevImage = newImage.copy()
                newImage = cv.filter2D(newImage, -1, kernel_sharpening)
                windowTitle = "Sharpen Image"
            case "5":
                hsv_image = cv.cvtColor(newImage, cv.COLOR_BGR2HSV)
                saturation_channel = hsv_image[:,:,1].astype(np.float64)
                saturation_factor = float(input("Enter the saturation factor (0.0-2.0): "))
                saturation_channel *= saturation_factor
                saturation_channel = np.clip(saturation_channel, 0, 255)
                saturation_channel = saturation_channel.astype(np.uint8)
                hsv_image[:,:,1] = saturation_channel
                prevImage = newImage.copy()
                newImage = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
                windowTitle = "Adjust Saturation"
            case "6":
                prevImage = newImage.copy()
                print("The diameter of each pixel neighborhood. Larger values means further pixels will influence each other.")
                diameter = int(input("Enter diameter (1-10): "))
                print("The sigma space controls the filter strength based on color differences. Larger values means that colors further apart will be mixed together.")
                sigColor = int(input("Enter sigma color (10-150): "))
                print("The sigma space controls the filter strength based on spatial differences. Larger values means that colors further apart will influence each other more.")
                sigSpace = int(input("Enter sigma space (10-150): "))
                newImage = cv.bilateralFilter(newImage, d = diameter, sigmaColor = sigColor, sigmaSpace = sigSpace)
                windowTitle = "Bilateral Filter"
            case "7":
                hsv_image = cv.cvtColor(newImage, cv.COLOR_BGR2HSV)
                hue_shift = int(input("Enter the number of degrees of the hue shift (-179 - 179): "))
                hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_shift) % 180
                newImage = cv.cvtColor(hsv_image, cv.COLOR_HSV2BGR)
            case "8":
                newImage = prevImage.copy()
                windowTitle = "Previous Image"
                print("Reversed last step.")
            case "9":
                print("Exiting program...")
                break
            case "10":
                fileName = input("Enter the file name to save the image to (do not include extension): ")
                while os.path.exists(fileName + ".jpg"):
                    print("File already exists. Please enter a different file name.")
                    fileName = input("Enter the file name to save the image to (do not include extension): ")
                cv.imwrite(fileName + ".jpg", newImage)
                print("Image saved to " + fileName + ".jpg")
            case _:
                print("Invalid choice. Please enter a valid choice.")
    cv.imshow("Final Image", newImage)
    cv.waitKey(0)
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()