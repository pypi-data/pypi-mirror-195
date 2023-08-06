import numpy as np


def fun():
    a = input()
    b = input()
    b1 = np.array([int(i) for i in b.split(',')])
    num = np.array([float(i) for i in a.split(',')]).reshape(b1[0], b1[1])
    # 均值标准化
    x = (num-np.mean(num))/np.std(num)
    x1 = np.cov(x.T)
    # 特征值、特征向量
    u, v = np.linalg.eig(x1)
    # 比较特征值，得出最大的特征值
    if u[0] > u[1]:
        index = 0
    else:
        index = 1
    print('第1主成分={:.5f}*(x1-{:.2f}){:+.5f}*(x2-{:.2f})'.format(
        v[0][index], np.mean(num, axis=0)[0], v[1][index], np.mean(num, axis=0)[1]))
