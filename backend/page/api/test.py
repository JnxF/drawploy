import numpy as np
import cv2


im = cv2.imread('draw.jpeg', 0)
thresh_img = cv2.adaptiveThreshold(im,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,3)

_, contours, _ = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
result = []
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    cv2.drawContours("res", [approx], -1, (0, 0, 255), 2, lineType=8)
    if 3 < len(approx) < 15:
        _, _, w, h = cv2.boundingRect(approx)
        hull = cv2.convexHull(cnt)
        approx2 = cv2.approxPolyDP(hull, 0.01 * cv2.arcLength(hull, True), True)
        cv2.drawContours("res", [approx2], -1, (0, 255), 2, lineType=8)
    result.append(approx2)
return result