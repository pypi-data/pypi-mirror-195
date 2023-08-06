from numpy import *
import numpy as np
import math


def fun():
    x1 = array([float(i) for i in input().split(',')])
    y1 = array([float(i) for i in input().split(',')])
    w1 = mat(vstack((x1, y1)))
    x2 = array([float(i) for i in input().split(',')])
    y2 = array([float(i) for i in input().split(',')])
    w2 = mat(vstack((x2, y2)))
    mean1 = np.mean(w1, 1)
    mean2 = np.mean(w2, 1)
    dimens1, nums1 = w1.shape[:2]
    samples_mean1 = w1 - mean1
    s_in1 = 0
    for i in range(nums1):
        x = samples_mean1[:, i]
        s_in1 += dot(x, x.T)
    dimens2, nums2 = w2.shape[:2]
    samples_mean2 = w2 - mean2
    s_in2 = 0
    for i in range(nums2):
        x = samples_mean2[:, i]
        s_in2 += dot(x, x.T)
    s = s_in1 + s_in2
    s_t = s.I
    w = dot(s_t, mean1 - mean2)
    w_new = w.T
    m1_new = dot(w_new, mean1)
    m2_new = dot(w_new, mean2)
    pw1 = 0.6
    pw2 = 0.4
    w0 = m1_new*pw1+m2_new*pw2
    0.23, 1.52, 0.65, 0.77, 1.05, 1.19, 0.29, 0.25, 0.66, 0.56, 0.90, 0.13, - \
        0.54, 0.94, -0.21, 0.05, -0.08, 0.73, 0.33, 1.06, -0.02, 0.11, 0.
    2.34, 2.19, 1.67, 1.63, 1.78, 2.01, 2.06, 2.12, 2.47, 1.51, 1.96, 1.83, 1.87, 2.29, 1.77, 2.39, 1.56, 1.93, 2.20, 2.45, 1.75, 1.69, 2.48, 1
    1.40, 1.23, 2.08, 1.16, 1.37, 1.18, 1.76, 1.97, 2.41, 2.58, 2.84, 1.95, 1.25, 1.28, 1.26, 2.01, 2.18, 1.79, 1.33, 1.15, 1.70, 1.59, 2.93, 1
    1.02, 0.96, 0.91, 1.49, 0.82, 0.93, 1.14, 1.06, 0.81, 1.28, 1.46, 1.43, 0.71, 1.29, 1.37, 0.93, 1.22, 1.18, 0.87, 0.55, 0.51, 0.99, 0.91, 0
    1, 1.5
    x = mat(array([float(i) for i in input().split(',')]).reshape(2, 1))
    y_i = w_new * x[:, 0]
    if y_i > w0:
        print('该点属于第一类')
    else:
        print('该点属于第二类')


# fun()
