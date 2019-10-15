import cv2
import math
import numpy as np


def DarkC(im, sz):
    b, g, r = cv2.split(im)  # R G B 三通道分离
    dc = cv2.min(cv2.min(r, g), b)  # 取三者最小值
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (sz, sz))  # 构造运算核心
    # 这个核也叫结构元素，因为形态学操作其实也是应用卷积来实现的。
    # 结构元素可以是矩形/椭圆/十字形，可以用cv2.getStructuringElement()来生成不同形状的结构元素，比如
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # 矩形结构
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 椭圆结构
    # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))  # 十字形结构

    dark = cv2.erode(dc, kernel)  # 腐蚀操作 腐蚀的效果是把图片"变瘦"，
    # 其原理是在原图的小区域内取局部最小值。因为是二值化图，只有0和255，所以小区域内有一个是0该像素点就为0：
    # 就是求领域最小值为自身值
    return dark  # 返回暗通道图


def ALight(im, dark):
    # 1.求取大气光强，在dark图中取前0.1%的亮点，一般雾大的地方在灰度图中数值高，
    # 2.取输入图像里面这些像素对应的像素里面最亮的作为大气光
    [h, w] = im.shape[:2]  # 取得长宽数据
    imgsize = h * w  # 像素数等于长宽乘
    highpoint = int(max(math.floor(imgsize / 1000), 1))  # 通过int型除以1000，计算出应该取出的点的个数，向下取整math.floor,若小于1则取1，虽然不太可能出现
    darkvec = dark.reshape(imgsize, 1)  # 把传入的暗通道图像素矩阵变成一维矩阵，2->1
    imgvec = im.reshape(imgsize, 3)  # 把传入的原图像像素矩阵各通道变成一维，共R,G,B三条通道，三行组成一个二维数组
    indices = np.argsort(darkvec, axis=0)  # 对处理的暗通道矩阵进行升序排序后输出排序后各元素的索引，就映射为输出中的值代表在原输入中的位置
    indices = indices[imgsize - highpoint::]  # 从排序索引输出中截取末尾的highpoint(最亮点)个数(在dark图中取前0.1%的亮点)
    atmsum = np.zeros((1, 3))  # 构造一个一行三列全为0的数组,默认float64
    for ind in range(1, highpoint):  # 循环遍历所有高亮点
        atmsum = atmsum + imgvec[indices[ind]]  # 把所有暗通道图中选取为高亮的点对应的原图点的值相加
    A = atmsum / highpoint  # 求和后求平均
    return A


def TransmissionEstimate(im, A, sz):
    # t(x) = 1 - omega * min_y∈Ω(x) [ min_c (Ic(y)/Ac) c值R,G,B三色
    omega = 0.95  # 用来保留部分景深信息，使用omega调节，设定范围在0->1
    im3 = np.empty(im.shape, im.dtype)  # 构建空图
    for ind in range(0, 3):  # 在三个通道遍历
        im3[:, :, ind] = im[:, :, ind] / A[0, ind]  # 计算公式中的 Ic(y)/Ac  雾图/大气光强
    transmission = 1 - omega * DarkC(im3, sz)  # 在三通道中取最小值，后取周围最小（腐蚀）
    return transmission  # 求得投射图t返回


def Guidedfilter(im, p, r, eps):  # 导向滤波，输入原图像  #均值滤波实现算法中的窗口平均
    mean_I = cv2.boxFilter(im, cv2.CV_64F, (r, r))  # 对原图均值滤波，导向图为自身
    # cv2.imshow("mean_i", mean_I)
    mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r))  # 对投射图均值滤波，作为输入的p图
    # cv2.imshow("mean_p", mean_p)
    mean_Ip = cv2.boxFilter(im * p, cv2.CV_64F, (r, r))  # 输入图像与投射图自乘后均值滤波
    cov_Ip = mean_Ip - mean_I * mean_p  # i，p联乘后均值滤波减去 ，i中对应位置均值滤波结果乘p中均值滤波结果，融合后结果

    mean_II = cv2.boxFilter(im * im, cv2.CV_64F, (r, r))  # 输入图像自乘后均值滤波
    var_I = mean_II - mean_I * mean_I  # I中窗口的方差

    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I

    mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))  # 一个像素会被多个窗口包含，也就是说，每个像素都由多个线性函数所描述，
    mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))  # 要具体求某一点的输出值时，只需将所有包含该点的线性函数值平均
    # 用均值滤波完成
    q = mean_a * im + mean_b
    return q


def TransmissionRefine(im, te):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # 把原图转化为灰度图
    gray = np.float64(gray) / 255  # 浮点化后以与255的比值计算
    # cv2.imshow("imgray", gray)
    r = 60
    eps = 0.0001
    t = Guidedfilter(gray, te, r, eps)  # 导向滤波

    return t


def Recover(im, t, A, tx=0.1):
    res = np.empty(im.shape, im.dtype)  # 先构建黑图
    t = cv2.max(t, tx)  # 取大值，用来排除t小于0.1的点位情况

    for ind in range(0, 3):
        res[:, :, ind] = (im[:, :, ind] - A[0, ind]) / t + A[0, ind]

    return res


def start_to_calculate(imgPath):
    src = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)  # 读入图像
    I = src.astype('float64') / 255  # 按与255的比率运算
    dark = DarkC(I, 15)  # 传入原图与核心大小为15*15
    # cv2.imshow("dark", dark)
    A = ALight(I, dark)  # 求取平均大气光强
    te = TransmissionEstimate(I, A, 15)  # 计算透射率
    # cv2.imshow("t", te)  # 输出投射图
    t = TransmissionRefine(src, te)  # 导向滤波完成
    # cv2.imshow('tt', t)  # 使用导向滤波细化投射图
    J = Recover(I, t, A, 0.1)  # t值过小会导致J值偏大，图像整体向白场迁移，设定阈值t0=0.1，若t小于0.1，按0.1计算
    # arr = np.hstack((I, J))
    # arr1 = np.hstack((dark, t))
    # cv2.imshow("out", arr)  # 输出去雾处理效果图
    # cv2.imshow("out0", arr1)  # 输出导向滤波前后透射图
    # cv2.waitKey()
    imgPath_pre = imgPath.split('.')[0]
    imgPath_pre += "_out."
    imgPath_pre_change = imgPath_pre.split('image')[0] + "image/image_processed" + imgPath_pre.split('image')[1]
    imgPath_out = imgPath_pre_change + imgPath.split('.')[1]
    print(imgPath_out)
    cv2.imwrite(imgPath_out, J * 255)
    return imgPath_out
