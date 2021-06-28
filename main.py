#!/usr/bin/python3

import cv2
import argparse
import math
import numpy as np
import csv

def save_csv(name,data):
    name = name[:-3] + "csv"
    with open(name,'w') as f:
        write = csv.writer(f)
        write.writerow(data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--image",required=True, help = "Path to image");
    args = vars(ap.parse_args())

    image = cv2.imread(args['image'],0)
    _,image = cv2.threshold(image,10,255,cv2.THRESH_BINARY)
    image = cv2.bitwise_not(image,image)
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(image)
    pts = np.asarray([[p.pt[0],p.pt[1]] for p in keypoints])

    Nucleii = pts
    Alignments = []

    for n in Nucleii:
        x1 = int(n[0])
        y1 = int(n[1])
        angles = [0,math.pi/2,math.pi,math.pi*3/2]

        y_vals = []
        x_vals = []

        for angle in angles:
            pixel = image[y1][x1]
            x2 = x1; y2=y1
            while pixel == image[y1][x1]:
                try:
                    pixel = image[int(y2)][int(x2)]
                    x2 = x2 + int(math.cos(angle))
                    y2 = y2 + int(math.sin(angle))
                except IndexError:
                    break
            y_vals.append(y2)
            x_vals.append(x2)

        length_x = abs(x_vals[0]-x_vals[2])
        length_y = abs(y_vals[1]-y_vals[3])

        Nuclear_Alignment = length_y/length_x
        Alignments.append(Nuclear_Alignment)

        cv2.putText(image,str(round(Nuclear_Alignment,2)),(x1,y1),cv2.FONT_HERSHEY_PLAIN,1,100)
    
    if len(Alignments) == 0:
        print("No nucleii found in image")
    else:
        print(str(len(Alignments))+" Nucleii Found... Saving CSV.")
        save_csv(args['image'],Alignments)
        cv2.imwrite("Output_Image.png",image)

if __name__ == "__main__":
    main()
