import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pygame
import datetime
import csv

pygame.init()
pygame.mixer.music.load("beep.wav")

# Open a CSV file for writing
csv_file = open('barcode_data.csv', mode='a', newline='')
csv_writer = csv.writer(csv_file)
id=int(input("Enter Customer ID"));
# Write the header row to the CSV file
csv_writer.writerow(['Customer ID','Barcode', 'Date', 'Month', 'Year', 'Time'])

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
myData = 0
lastdata = 0
while True:
    success, img = cap.read()
    for barcode in decode(img):
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x - 10, y - 10),
                      (x + w + 10, y + h + 10),
                      (255, 0, 0), 2)
        myData = barcode.data.decode('utf-8')
        if lastdata != myData:
            # Get the current date and time
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d")
            month = now.strftime("%B")
            year = now.year
            current_time = now.strftime("%H:%M:%S")

            # Print and save the data to the CSV file
            print(f"Barcode: {myData}")
            csv_writer.writerow([id,myData, date, month, year, current_time])

            pygame.mixer.music.play()
            duration = 5000
            pygame.time.delay(duration)
            pygame.mixer.music.stop()

        lastdata = myData
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

    cv2.imshow('Result', img)
    cv2.waitKey(1)

# Close the CSV file when done
csv_file.close()