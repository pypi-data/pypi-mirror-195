import numpy as np
from sklearn.cluster import KMeans


def fun():

    a = input()
    b = input()
    c = input()
    t1 = np.array([float(i) for i in a.split(' ')])
    t2, t3 = np.array([int(i) for i in b.split(' ')])
    t4 = int(c)
    n = np.array(t1).reshape(t2, t3)
    kmeans = KMeans(n_clusters=t4)
    kmeans.fit(n)
    m = kmeans.labels_[0]
    print("A公司所在类的中心为：{:.2f},{:.2f}。".format(kmeans.cluster_centers_[m, 0], kmeans.cluster_centers_[m,
                                                                                                    1]))
