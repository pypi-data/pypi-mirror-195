# import numpy as np


# def fun(s1, s2):
#     # s1 = input()
#     # s2 = input()
#     n = []
#     num = [float(n) for n in s1.split()]
#     for i in range(0, len(num), 31):
#         x = num[i:i+31]
#         n.append(x)
#     n = np.matrix(n)
#     nn = np.corrcoef(n)
#     print(nn)
#     # return nn


# # str = '''15637.84 11467.16 7951.31 7902.86 8122.99 8007.56 7840.61 7470.71 16682.82 10481.93 14546.38 7511.43 11175.37 7559.64 9437.8 7704.9 8022.75 8617.48 13627.65 8689.99 7735.78 9220.96 7709.87 7322.05 8870.88 9106.07 7492.47 7376.74 7319.67 7217.87 7503.42 12200.4 8802.44 5819.18 5654.15 6219.26 6543.26 6068.99 5567.53 12631.03 7332.26 10636.14 5711.33 8161.15 5337.84 6673.75 5294.19 6398.52 6884.61 10694.79 6445.73 5802.4 7973.05 6371.14 5494.45 6837.01 8338.21 6233.07 5937.3 5758.95 5821.38 5773.62
# # 2 31
# # '''
# # s1 = str.split('\n')[0]
# # s2 = str.split('\n')[1]
# # print(fun(s1, s2))

import numpy as np


def fun():
    s1 = input()
    s2 = input()
    n = []
    num = [float(n) for n in s1.split()]
    for i in range(0, len(num), 31):
        x = num[i:i+31]
        n.append(x)
    n = np.matrix(n)
    nn = np.corrcoef(n)
    print(nn)
