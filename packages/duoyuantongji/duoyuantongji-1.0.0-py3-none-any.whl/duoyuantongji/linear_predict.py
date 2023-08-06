# import numpy as np
# from sklearn.linear_model import LinearRegression


# def fun(a, b, c):
#     # a = input()
#     # b = input()
#     # c = input()
#     X1 = list(map(int, a.split(' ')))
#     y1 = list(map(float, b.split(' ')))
#     n = int(c)
#     X = np.mat(X1).reshape(5, 1)
#     y = np.mat(y1).reshape(5, 1)
#     model = LinearRegression()
#     model.fit(X, y)
#     return ("Predict 12 inch cost:$%.2f" % model.predict([[n]]))


# # str = '''6 8 10 14 18
# # 7 9 13 17.5 18
# # 12
# # '''
# # a = str.split('\n')[0]
# # b = str.split('\n')[1]
# # c = str.split('\n')[2]
# # print(fun(a, b, c))


import numpy as np
from sklearn.linear_model import LinearRegression


def fun():
    a = input()
    b = input()
    c = input()
    X1 = list(map(int, a.split(' ')))
    y1 = list(map(float, b.split(' ')))
    n = int(c)
    X = np.mat(X1).reshape(5, 1)
    y = np.mat(y1).reshape(5, 1)
    model = LinearRegression()
    model.fit(X, y)
    print("Predict 12 inch cost:$%.2f" % model.predict([[n]]), end="")
