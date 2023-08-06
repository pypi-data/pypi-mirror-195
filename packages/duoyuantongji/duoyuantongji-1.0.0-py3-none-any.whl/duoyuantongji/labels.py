import numpy as np
from sklearn.cluster import AgglomerativeClustering


def fun():

    temp = np.array([float(i) for i in input().split(' ')])
    n_samplesj, n_features = np.array([int(i) for i in input().split(' ')])
    X = np.array(temp).reshape(n_samplesj, n_features)
    n_clusters = int(input())
    hc = AgglomerativeClustering(
        n_clusters=n_clusters, affinity='correlation', linkage='complete')
    hc.fit(X.T)
    hcl = hc.labels_
    if hcl[0] == hcl[2]:
        print("香气和酸质属于一类。")
    else:
        print("香气和酸质不属于一类。")
