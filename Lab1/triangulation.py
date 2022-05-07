from random import random, seed
from math import *

EPS = 0.1
EPS_LINE = 1e-3
EPS_RAD = 0.1
MAX_TRY = 300

# 返回[_min, _max)区间内的随机数
def randomf(_min, _max):
    return random() * (_max - _min) + _min

# 检查三角形各边是否均不平行于坐标轴
def check_constraints(a, b, c):
    if (fabs(a[0] - b[0]) < EPS) or (fabs(a[1] - b[1]) < EPS):
        return False
    if (fabs(b[0] - c[0]) < EPS) or (fabs(b[1] - c[1]) < EPS):
        return False
    if (fabs(c[0] - a[0]) < EPS) or (fabs(c[1] - a[1]) < EPS):
        return False
    return True

# 将点p绕原点旋转theta度
def rotate(p, theta):
    cos_theta = cos(theta)
    sin_theta = sin(theta)
    return [
        p[0] * cos_theta + p[1] * sin_theta, 
        -p[0] * sin_theta + p[1] * cos_theta
    ]

# 若三角形不满足约束条件（各边均不平行于坐标轴）
# 则将三角形绕原点旋转随机角度，直到满足约束条件
def random_rotate(a, b, c):
    if check_constraints(a, b, c):
        return a, b, c, 0
    ntry = 0
    while ntry < MAX_TRY:
        ntry += 1
        theta = randomf(0.0, 2 * pi)
        new_a = rotate(a, theta)
        new_b = rotate(b, theta)
        new_c = rotate(c, theta)
        if check_constraints(new_a, new_b, new_c):
            return new_a, new_b, new_c, theta
    return a, b, c, nan

# rssi平面三点定位算法的子过程，
# ref: https://www.cnblogs.com/ikaros-521/p/15346443.html#gallery-25
def calc_pos_sub(a, b, c, da, db, dc):
    div_ba = (b[0] - a[0]) / (b[1] - a[1])
    div_ca = (c[0] - a[0]) / (c[1] - a[1])
    long_1 = da ** 2 - db ** 2 - a[0] ** 2 - a[1] ** 2 + b[0] ** 2 + b[1] ** 2
    long_2 = da ** 2 - dc ** 2 - a[0] ** 2 - a[1] ** 2 + c[0] ** 2 + c[1] ** 2
    x = ((long_1 / (2 * (b[1] - a[1]))) - (long_2 / (2 * (c[1] - a[1])))) / (div_ba - div_ca)
    y = ((long_1 / (2 * (b[0] - a[0]))) - (long_2 / (2 * (c[0] - a[0])))) / ((1 / div_ba) - (1 / div_ca))
    return [x, y]

# rssi平面三点定位算法
def calc_pos(a, b, c, da, db, dc):
    if da < 0 or db < 0 or dc < 0: 
        print("Error: Got negative distance")
        return [-1, -1]

    # 若三角形不满足约束条件，则将三角形绕原点旋转随机角度，直到满足约束条件
    a, b, c, theta = random_rotate(a, b, c)
    if isnan(theta):
        print("Error: Failed to rotate points")
        return [-1, -1]

    # 判断是否存在三点共线，若存在则算法无法求解
    div_ba = (b[0] - a[0]) / (b[1] - a[1])
    div_ca = (c[0] - a[0]) / (c[1] - a[1])
    if fabs(div_ba - div_ca) < EPS_LINE or fabs((1 / div_ba) - (1 / div_ca)) < EPS_LINE:
        print("Error: Points on a same line")
        return [-1, -1]

    # 以三个点的不同排列调用三次子过程，计算出三个预测点
    p1 = calc_pos_sub(a, b, c, da, db, dc)
    p2 = calc_pos_sub(b, c, a, db, dc, da)
    p3 = calc_pos_sub(c, a, b, dc, da, db)
    
    # 计算三个预测点围成的三角形的内心，作为最终的预测点
    if p1[0] == p2[0] and p2[0] == p3[0] and p1[1] == p2[1] and p2[1] == p3[1]:
        return p1
    d12 = sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    d23 = sqrt((p2[0] - p3[0]) ** 2 + (p2[1] - p3[1]) ** 2)
    d31 = sqrt((p3[0] - p1[0]) ** 2 + (p3[1] - p1[1]) ** 2)
    x = (d23 * p1[0] + d31 * p2[0] + d12 * p3[0]) / (d23 + d31 + d12)
    y = (d23 * p1[1] + d31 * p2[1] + d12 * p3[1]) / (d23 + d31 + d12)
    
    # 将之前对三角形进行的旋转复原
    p = rotate([x, y], -theta)
    return p

# 测试代码
def test_calc_pos(n):
    for i in range(n):
        a = [randomf(0.0, 3.0), randomf(0.0, 3.0)]
        b = [randomf(0.0, 3.0), randomf(0.0, 3.0)]
        c = [randomf(0.0, 3.0), randomf(0.0, 3.0)]
        pos = [randomf(-1.0, 4.0), randomf(-1.0, 4.0)]
        da = sqrt((a[0] - pos[0]) ** 2 + (a[1] - pos[1]) ** 2)
        db = sqrt((b[0] - pos[0]) ** 2 + (b[1] - pos[1]) ** 2)
        dc = sqrt((c[0] - pos[0]) ** 2 + (c[1] - pos[1]) ** 2)
        pred = calc_pos(a, b, c, da, db, dc)
        #if fabs(pred[0] - pos[0]) >= 1e-4 or fabs(pred[1] - pos[1]) >= 1e-4:
        print('Test #%d: A(%.3f, %.3f), B(%.3f, %.3f), C(%.3f, %.3f), d(%.3f, %.3f, %.3f), real(%.3f, %.3f), pred(%.3f, %.3f)' \
                % (i, a[0], a[1], b[0], b[1], c[0], c[1], da, db, dc, pos[0], pos[1], pred[0], pred[1]))

if __name__ == '__main__':
    seed()
    test_calc_pos(20)