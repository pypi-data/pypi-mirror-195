# import numpy as np


# def fun(a):

#     a = a.split(" ")

#     if len(a) != 25:
#         print("输入有错！")

#     else:
#         try:
#             a = [int(i) for i in a]
#             a = [a[i:i + 5] for i in range(0, len(a), 5)]
#         except:
#             print("输入有错！")
#         eig_vals, eig_vectors = np.linalg.eig(a)
#         # return ''.join(str(eig_vals) + '\n'+str(eig_vectors))
#         return (eig_vals, eig_vectors)


# # str = '''1 2 3 4 5 6 7 8 9 10 1 2 1 3 14 12 12 14 1 4 5 7 8 9 23'''
# # a = fun(str)
# # print(a[0], '\n', a[1])

import numpy as np


def fun():
    a = input().split(" ")

    if len(a) != 25:
        print("输入有错！")

    else:
        try:
            a = [int(i) for i in a]
            a = [a[i:i + 5] for i in range(0, len(a), 5)]
        except:
            print("输入有错！")
        eig_vals, eig_vectors = np.linalg.eig(a)
        print(eig_vals, '\n', eig_vectors)
