import cv2 as cv
import sys
import numpy as np
import os

def showImage(windowTitle, newImage):
    cv.imshow(windowTitle, newImage)
    cv.waitKey(0)
    cv.destroyAllWindows()

def main():
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
        userChoice = input("What type of image processing would you like to do (just enter the number)?\n1. Gaussian Blur\n2. Speckle Noise\n3. Adjust Contrast/Brightness\n4. Sharpen Image\n5. Adjust Saturation\n6. Placeholder\n7. Reverse Last Step (only works for 1 step)\n8. Exit\n9. Save Image to File\nEnter choice: ")
        match userChoice:
            case "1":
                blurScale = int(input("Enter the blur scale (must be an odd number): "))
                while (blurScale % 2 == 0):
                    blurScale = input("Please enter a valid blur scale (must be an odd number): ")
                prevImage = newImage.copy()
                newImage = cv.GaussianBlur(newImage, (blurScale, blurScale), 0)
                windowTitle = "Gaussian Blur"
            case "2":
                print("Adding speckle noise to the image...")
            case "3":
                try:
                    alpha = float(input("Enter the alpha value [0-3] (0-1 lowers contrast, 1-3 brightens it): "))
                    beta = int(input("Enter the beta value [-100-100] (below 0 lowers brightness, positive increase brightness): "))
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
                print("z")
            case "7":
                newImage = prevImage.copy()
            case "8":
                break
            case "9":
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