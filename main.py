import cv2 as cv

def main():
    camera = cv.VideoCapture(0)
    ret, image = camera.read()
    while True:
        if not ret:
            print('No camera detected')
            break
        cv.imshow('img1', image)
        cv.waitKey()
        break
    camera.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()