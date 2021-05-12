#### file detect
from imutils import contours
import numpy as np
import imutils
import cv2
import cv2 as cv
def Crush(image) :


    img = cv2.imread(image)

    #dst = cv2.fastNlMeansDenoisingColored(img, None, 15, 8, 5, 12)
    src = cv.GaussianBlur(img, (9 ,9 ), 0)

    # gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)


    gray = cv2.Canny(src, 35,188)
    edged = cv2.dilate(gray, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # sort the contours from left-to-right and initialize the
    (cnts, _) = contours.sort_contours(cnts)
    m = list(np.arange(len(cnts)))
    print(m)
    m_copy = m.copy()
    n = []
    listOI = []
    m3 = 0
    for c in m:
        if c in n:
            continue
        if cv2.contourArea(cnts[c]) < 100:
            if c in m_copy:
                m_copy.remove(c)
            continue
        mask_c = np.zeros(gray.shape, dtype="uint8")
        cv2.drawContours(mask_c, cnts, c, (255, 255, 255), -1)
        img_c = cv2.bitwise_and(img, img, mask=mask_c)
        for j in m:
            if (j is c) or (j in n):
                continue
            if cv2.contourArea(cnts[j]) < 100:
                if j in m_copy:
                    m_copy.remove(j)
                continue
            mask = np.zeros(gray.shape, dtype="uint8")
            cv2.drawContours(mask, cnts, j, 255, -1)
            (x, y, w, h) = cv2.boundingRect(cnts[j])
            imageROI = img[y:y + h, x:x + w]
            maskROI = mask[y:y + h, x:x + w]
            imageROI = cv2.bitwise_and(imageROI, imageROI, mask=maskROI)
            # compare imageROI_c  vs rotated
            for angle in np.arange(240, 360, 6):
                template = imutils.rotate_bound(imageROI, angle)
                # cv2.imshow('1', template)
                # cv2.imshow('2', img_c)
                # cv2.waitKey(100)
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                img_gray = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
                res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
                threshold = 0.92
                loc = np.where(res >= threshold)
                # Remove object
                k = np.array(loc)
                m1 = k.shape
                if m1 != (2, 0):
                    n.append(j)
                    if j in m_copy:
                        m_copy.remove(j)
                    break
  ### xóa thuốc giống nhau
    for a in n:
        for b in n:
            if b == a:
                n.remove(b)
    mask_orig = np.zeros(gray.shape, dtype="uint8")
    for k in m_copy:
        cv2.drawContours(mask_orig, cnts, k, (255, 255, 255), -1)
    img_orig = cv2.bitwise_and(img, img, mask=mask_orig)
    for i in m_copy :
        mask_orig = np.zeros(gray.shape, dtype="uint8")
        cv2.drawContours(mask_orig, cnts, i, 255, -1)
        (x2, y2, w2, h2) = cv2.boundingRect(cnts[i])
        imageROI_orig = img[y2:y2 + h2, x2:x2 + w2]
        maskROI_orig = mask_orig[y2:y2 + h2, x2:x2 + w2]
        imageROI_orig = cv2.bitwise_and(imageROI_orig, imageROI_orig, mask=maskROI_orig)
        listOI.append(imageROI_orig)
    return img_orig,listOI,cnts
