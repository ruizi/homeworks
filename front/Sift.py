import cv2
import numpy as np


def drawMatchesKnn_cv2(img1_gray, kp1, img2_gray, kp2, goodMatch):  # 画线函数
    h1, w1 = img1_gray.shape[:2]
    h2, w2 = img2_gray.shape[:2]

    vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    vis[:h1, :w1] = img1_gray
    vis[:h2, w1:w1 + w2] = img2_gray

    p1 = [kpp.queryIdx for kpp in goodMatch]
    p2 = [kpp.trainIdx for kpp in goodMatch]

    post1 = np.int32([kp1[pp].pt for pp in p1])
    post2 = np.int32([kp2[pp].pt for pp in p2]) + (w1, 0)
    for (x1, y1), (x2, y2) in zip(post1, post2):
        cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255))
        cv2.circle(vis, (x1, y1), 10, (0, 255, 0))
        #cv2.putText(vis, "ttt", (x1, y1), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
    # cv2.namedWindow("match", cv2.WINDOW_NORMAL)
    # cv2.imshow("match", vis)
    return vis


def start_to_calculate(imgPath1, imgPath2):
    img1_gray = cv2.imread(imgPath1, cv2.IMREAD_UNCHANGED)

    img2_gray = cv2.imread(imgPath2, cv2.IMREAD_UNCHANGED)

    sift = cv2.xfeatures2d.SIFT_create()  # 构建sift对象
    # sift = cv2.SURF()

    kp1, des1 = sift.detectAndCompute(img1_gray, None)  # 特征点检测
    kp2, des2 = sift.detectAndCompute(img2_gray, None)

    # BFmatcher with default parms
    bf = cv2.BFMatcher(cv2.NORM_L2)  # 构建匹配对象
    matches = bf.knnMatch(des1, des2, k=2)

    goodMatch = []
    for m, n in matches:
        if m.distance < 0.5 * n.distance:
            goodMatch.append(m)

    outpicture = drawMatchesKnn_cv2(img1_gray, kp1, img2_gray, kp2, goodMatch[:])
    imgPath_pre = imgPath1.split('.')[0]
    imgPath_pre += "_out."
    imgPath_pre_change = imgPath_pre.split('image')[0] + "\image\image_processed" + imgPath_pre.split('image')[1]
    imgPath_out = imgPath_pre_change + imgPath1.split('.')[1]
    cv2.imwrite(imgPath_out, outpicture)
    return imgPath_out
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
