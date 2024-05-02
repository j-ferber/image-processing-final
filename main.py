import cv2 as cv
import sys

def main():
    if (len(sys.argv) != 2):
        print("Usage: python main.py <input_image>")
        exit()
    input_image = sys.argv[1]

    image = cv.imread(input_image)
    image = cv.resize(image, (800, 600))
    newImage = image.copy()
    windowTitle = "Input Image"

    userChoice = input("What type of image processing would you like to do (just enter the number)?\n1. Gaussian Blur\n2. Speckle Noise\n3. Adjust Contrast/Brightness\n")
    match userChoice:
        case "1":
            blurScale = int(input("Enter the blur scale (must be an odd number): "))
            while (blurScale % 2 == 0):
                blurScale = input("Please enter a valid blur scale (must be an odd number): ")
            newImage = cv.GaussianBlur(image, (blurScale, blurScale), 0)
            windowTitle = "Gaussian Blur"
        case "2":
            print("Adding speckle noise to the image...")
        case "3":
            try:
                alpha = float(input("Enter the alpha value [0-3] (0-1 lowers contrast, 1-3 brightens it): "))
                beta = int(input("Enter the beta value [-100-100] (below 0 lowers brightness, positive increase brightness): "))
                newImage = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
                windowTitle = "Contrast/Brightness Adjustment"
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    cv.imshow(windowTitle, newImage)
    cv.waitKey(0)

if __name__ == '__main__':
    main()