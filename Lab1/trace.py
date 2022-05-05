from numpy import dtype
from triangulation import calc_pos
from math import *
import pandas as pd
import matplotlib.pyplot as plt
from sys import argv
import numpy as np
import turtle

WINDOWSIZE = 5
FIGSIZE = 500

def get_group_data():
    if len(argv) < 2:
        print("Wrong input format!")
        exit()
    df = pd.read_csv(argv[1])
    ids = list(set(df['id']))
    ids.sort()
    if len(ids) != 3:
        print('!!!')
        exit()
    dic = {ids[0]: [], ids[1]: [], ids[2]: []}
    for i in range(df.shape[0]):
        line = list(df.iloc[i])
        time_split = line[1].split(':')
        line[1] = 3600 * int(time_split[0]) + 60 * int(time_split[1]) + int(time_split[2])
        dic[line[0]].append([line[1], line[3]])
    data_a, data_b, data_c = dic[ids[0]], dic[ids[1]], dic[ids[2]]
    data_a.sort(key=lambda x: x[0])
    data_b.sort(key=lambda x: x[0])
    data_c.sort(key=lambda x: x[0])
    return data_a, data_b, data_c

def get_dist(data, t):
    pos = 0
    while t > data[pos][0]:
        pos += 1
    if t == data[pos][0]:
        return data[pos][1]
    else:
        if (pos == 0):
            print('Starttime error!')
            return -1
        dist1 = data[pos - 1][1]
        dist2 = data[pos][1]
        d1 = t - data[pos - 1][0]
        d2 = data[pos][0] - t
        return (dist1 * d2 + dist2 * d1) / (d1 + d2)

def smooth_data(rawdata):
    data = []
    for i in range(len(rawdata) - WINDOWSIZE + 1):
        s1 = 0.0
        s2 = 0.0
        s3 = 0.0
        for j in range(WINDOWSIZE):
            s1 += rawdata[i + j][0]
            s2 += rawdata[i + j][1]
            s3 += rawdata[i + j][2]
        data.append([s1 / WINDOWSIZE, s2 / WINDOWSIZE, s3 / WINDOWSIZE])
    return data

def export_smoothdata(alldata):
    df = pd.DataFrame(alldata, columns=['dist1', 'dist2', 'dist3'])
    df.to_csv('smoothdata.csv', float_format='%.3f', index=False)
    arr = np.array(alldata, dtype=float)
    plt.figure()
    plt.scatter(range(len(arr)), arr[:,0], color='red')
    plt.scatter(range(len(arr)), arr[:,1], color='yellow')
    plt.scatter(range(len(arr)), arr[:,2], color='blue')
    plt.tight_layout()
    plt.savefig('smoothdata.pdf')

def show_trace(allpos):
    df = pd.DataFrame(allpos, columns=['x', 'y'])
    df.to_csv('pos.csv', float_format='%.3f', index=False)
    arr = np.array(allpos, dtype=float)
    plt.figure()
    plt.plot(arr[:,0], arr[:,1])
    plt.tight_layout()
    plt.savefig('trace.pdf')

def show_turtle(allpos):
    turtle.screensize(500, 500)
    turtle.pensize(5)
    turtle.pencolor('blue')
    turtle.penup()
    turtle.hideturtle()
    turtle.goto((allpos[0][0] - 5) * 50, (allpos[0][1] - 5) * 50)
    turtle.pendown()
    for line in allpos[1:]:
        turtle.goto((line[0] - 5) * 50, (line[1] - 5) * 50)
    turtle.done()

if __name__ == '__main__':
    data_a, data_b, data_c = get_group_data()
    starttime = max(data_a[0][0], data_b[0][0], data_c[0][0])
    endtime = min(data_a[-1][0], data_b[-1][0], data_c[-1][0])
    alldata = []
    for t in range(starttime, endtime + 1):
        alldata.append([get_dist(data_a, t), get_dist(data_b, t), get_dist(data_c, t)])
    alldata = smooth_data(alldata)
    #export_smoothdata(alldata)
    allpos = []
    for line in alldata:
        allpos.append(calc_pos([2.4, 1.2], [6, 5.4], [0, 10.8], line[0], line[1], line[2]))
    #show_trace(allpos)
    show_turtle(allpos)
    