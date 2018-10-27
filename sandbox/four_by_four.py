from math import cos, sin, radians
import numpy as np


def vec_4(vec_3):
    return np.append(vec_3, 0)


def point_4(point_3):
    return np.append(point_3, 1)


def point_3(point_4):
    return point_4[0:3]


def transform(point, matrix):
    pt = point_4(point)
    # print(pt)
    tr_pt = matrix.dot(pt)
    # print(tr_pt)
    return point_3(tr_pt)


def matrix_translate(tx, ty, tz):
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])


def matrix_rotate(angle, axis):
    angle = radians(angle)

    return np.array([[ cos(angle) if axis != "x" else 1, -sin(angle) if axis == "z" else 0,  sin(angle) if axis == "y" else 0, 0],
                     [ sin(angle) if axis == "z" else 0,  cos(angle) if axis != "y" else 1, -sin(angle) if axis == "x" else 0, 0],
                     [-sin(angle) if axis == "y" else 0,  sin(angle) if axis == "x" else 0,  cos(angle) if axis != "z" else 1, 0],
                     [                                0,                                 0,                                 0, 1]])


def matrix_rotate_arbitray_point(angle, axis, point):
    return (matrix_translate(-point[0], -point[1], -point[2]).dot(matrix_rotate(angle, axis))).dot(matrix_translate(point[0], point[1], point[2]))

m1 = matrix_rotate_arbitray_point(10, "z", [10, 0, 0])
m2 = matrix_rotate(10, "z")

point = np.array([1, 0, 0])

# print(transform(point, m1))
# print(transform(point, m2))


def affine(X, Y):
    """ find affine transformation

    Parameters
    ----------

    X  : np.array
        3xN
    Y
        3xN

    Returns
    -------

    A : np.array
        3x3
    B : np.array
        3x1

    Notes
    -----

    Given X and Y find the affine transformation

    Y = A X + B

    """
    from numpy.linalg import pinv

    B = Y[:, 0][:, np.newaxis]
    Yc = Y - B
    pX = pinv(X)
    A = np.dot(Yc, pX)

    print(A[1])
    print(B[1][0])
    # print(B[0][0])
    #
    C = np.array([[A[0][0], A[0][1], A[0][2], B[0][0]],
                  [A[1][0], A[1][1], A[1][2], B[1][0]],
                  [A[2][0], A[2][1], A[2][2], B[2][0]],
                  [0, 0, 0, 1]])

    return C

X = np.array([[0, 0, 0],
              [1, 0, 0],
              [0, 1, 0]])

Y = np.array([[1, 0, 0],
              [2, 0, 0],
              [1, 1, 0]])

# ???? -> Wrong result

print(affine(X, Y))

