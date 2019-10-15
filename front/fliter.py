import cv2
import numpy as np


def start_to_calculate(imgPath, ins):
    src = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)  # 读入图像
    print(123)
    print(ins)
    if ins == "Gus":
        out = cv2.GaussianBlur(src, (3, 3), 0)  # 输入处理图像，取大小为3*3的核，0表示默认权值
    elif ins == "avg":
        out = cv2.blur(src, (2, 2))
    elif ins == "rec":
        out = cv2.boxFilter(src, -1, (3, 3), normalize=0)  # 归一化条件，若为0则求和，为1为均值滤波
        # 原始图像，目标图像深度，核大小，normalize属性
    elif ins == "rev":
        out = cv2.flip(src, 1)  # 左右翻转
    elif ins == "rod":
        k = np.ones((5, 5), np.uint8)
        out = cv2.erode(src, k, iterations=10)
    elif ins == "add":
        k = np.ones((5, 5), np.uint8)  # 使用numpy二值化
        # r = cv2.erode(src, k, iterations=2)  # 腐蚀
        out = cv2.dilate(src, k, iterations=1)  # 膨胀

    imgPath_pre = imgPath.split('.')[0]
    imgPath_pre += "_out."
    imgPath_pre_change = imgPath_pre.split('image')[0] + "/image/image_processed" + imgPath_pre.split('image')[1]
    imgPath_out = imgPath_pre_change + imgPath.split('.')[1]
    cv2.imwrite(imgPath_out, out)
    return imgPath_out
