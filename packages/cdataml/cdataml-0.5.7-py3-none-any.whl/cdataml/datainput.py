import cv2 as cv
import sys
import pandas as pd
import numpy as np

def _record_dims(path):
    img = cv.imread(cv.samples.findFile(path))
    meta_bar = np.full((200, img.shape[1],3), 255, dtype=np.uint8)
    with_meta = np.concatenate((meta_bar, img))
    meta_text = "enter the number of rows and columns"
    cv.putText(img = with_meta, text = meta_text, org = (50, 160), fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=8, color=(0, 0, 0),thickness=8)

    dim = (int(with_meta.shape[1]*0.25), int(with_meta.shape[0]*0.25))
    img_scaled = cv.resize(with_meta, dim)
    cv.imshow("Recording Image Dimensions", img_scaled)
    cv.setWindowProperty("Recording Image Dimensions", cv.WND_PROP_TOPMOST, 1)

    while True:
        try:
            print("""----------
Please enter the number of rows
----------""")
            row = chr(cv.waitKey(0))
            if ord(row) == 27:
                return None
            print(f"""----------
VALUE ENTERED
    Row Count: {row}
----------""")
            print("""----------
Please enter the number of columns
----------""")
            col = chr(cv.waitKey(0))
            if ord(col) == 27:
                return None
            print(f"""----------
VALUE ENTERED
    Column Count: {col}
----------""")
            row, col = int(row), int(col)
            if (row <= 0) or (col <= 0):
                print("please try again. maxrow and maxcol should a positive integer between 1 and 9")
                continue
            break
        except ValueError:
            print("please try again. maxrow and maxcol should be a positive integer between 1 and 9")

    cv.destroyAllWindows()
    return row, col


def _make_square_coords(coords):
    # Function to make coordinates selected in OpenCV tool square by increasing shorter length to match longer.
    hlen = coords[3] - coords[1] # Horizontal length
    vlen = coords[2] - coords[0] # Vertical length
    diff = abs(hlen-vlen) # Difference
    # Add half the difference between them to the greater of the shorter axis
    # Subtract half the difference between them to the lesser of the shorter axis
    if hlen == max(hlen, vlen): # If wider than tall
        coords[2] = coords[2] + (diff / 2)
        coords[0] = coords[0] - (diff / 2)
    else: # If taller than wide
        coords[3] = coords[3] + (diff / 2)
        coords[1] = coords[1] - (diff / 2)
    return coords

def _input_coords(img, scale_val):
    print("Input Coords")
    cv.imshow("Cell Death Area Coordinate and Scoring Tool", img)
    cv.setWindowProperty("Cell Death Area Coordinate and Scoring Tool", cv.WND_PROP_TOPMOST, 1)
    bounding_box = cv.selectROI("Cell Death Area Coordinate and Scoring Tool", img, fromCenter=False, showCrosshair=False)
    x1 = int(bounding_box[0])
    x2 = int(bounding_box[0] + bounding_box[2])
    y1 = int(bounding_box[1])
    y2 = int(bounding_box[1] + bounding_box[3])

    # Remove pixels from metadata and scale coords up
    y1 -= scale_val * 200 # 200 is height of metadata bar
    y2 -= scale_val * 200
    coords = [x1/scale_val, x2/scale_val, y1/scale_val, y2/scale_val]

    # Make selection square
    squarecoords = _make_square_coords(coords)
    print(squarecoords)
    return squarecoords[0], squarecoords[1], squarecoords[2], squarecoords[3] # order x1, x2, y1, y2

def _input_score(img):
    print("Input Score")
    while True:
        keypress = cv.waitKey(0)
        if keypress == 27:
            return None
        elif keypress == ord("l"):
            return "l"
        elif keypress == ord("s"):
            return "s"
        elif not chr(keypress) in ['0','1','2','3','4','5','6']:
            print(f"the entered value, {chr(keypress)}, is not valid. please enter a score from 0 to 6 or exit by pressing ESC")
        else:
            score = int(chr(keypress))
            print(score)
            break
    return score
