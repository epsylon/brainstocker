#!/usr/bin/env python3
# -*- coding: utf-8 -*-"
"""
BrAInStocker - 2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with BrAInStocker; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import random, time, os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn import linear_model

print(75*"=")
print(" ____        _    ___       ____  _             _             ")
print("| __ ) _ __ / \  |_ _|_ __ / ___|| |_ ___   ___| | _____ _ __ ")
print("|  _ \| '__/ _ \  | || '_ \\___ \| __/ _ \ / __| |/ / _ \ '__|")
print("| |_) | | / ___ \ | || | | |___) | || (_) | (__|   <  __/ |   ")
print("|____/|_|/_/   \_\___|_| |_|____/ \__\___/ \___|_|\_\___|_|   ")
print("                                                              ")
print(75*"=","\n")
print("Can you 'predict' the next random number?\n")
print(75*"=")

print ("\n[Info] Starting prediction...\n")
store_dataset = "dataset/"
if not os.path.exists(store_dataset):
    os.mkdir(store_dataset)
r = 0
match = False
numrange = input(" -Set the maximum number for a random number (PRESS ENTER = 100): ")
if not numrange:
    numrange = 100
try:
    numrange = int(numrange)
except:
    numrange = 100
maxrange = input(" -Set the maximum number of random numbers to be generate (PRESS ENTER = 1000) (STOP = CTRL+z): ")
if not maxrange:
    maxrange = 1000
try:
    maxrange = int(maxrange)
except:
    maxrange = 1000
print("\n[Info] Generating "+ str(maxrange)+ " random numbers...\n")
with open('dataset/dataset.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["ROUND", "Time", "Number"])
f.close()
def advance_round(r):
    r = r + 1
    return r
def generate_random_number():
    for x in range(numrange):
        n = random.randint(0,numrange)
    return n
def check_current_time():
    t = int(round(time.time() * 1000))
    return t
def format_digits(num):
    nr = int(len(str(numrange)))
    num = num.zfill(nr)
    return num
print("="*40)
print("ROUND:          TIME:          NUMBER:")
print("-"*40)
for a in range(0, maxrange):
    r = advance_round(r)
    t = str(check_current_time())
    n = str(generate_random_number())
    with open('dataset/dataset.csv', 'a', newline='') as f:
        w = csv.writer(f)
        w.writerow([r, t, n])
    print ("[", str(r).zfill(5), "] [", t, "] -> [", str(format_digits(str(n))),"]")
df = pd.read_csv('dataset/dataset.csv') 
x = df['Number']
y = df['Time']
X, y = make_regression(n_samples=maxrange, n_features=2, noise=0.0)
model = linear_model.LinearRegression()
try:
    model.fit(X, y)
    Xnew = [[check_current_time(), generate_random_number()]]
    ynew = model.predict(Xnew)
    prediction = str(Xnew[0][1])
    prediction = format_digits(prediction)
    nextnum = str(generate_random_number())
    nextnum = format_digits(nextnum)
    print("\n"+"="*40)
    print("[AI] PREDICTION : [ %s ]" % prediction)
    print("="*40)
    print("[AI] NEXT NUMBER: [ %s ] " % nextnum)
    print("="*40+"\n")
    if prediction == nextnum:
        print("[Info] MATCH !!! ;-)\n")
        match = True
    else:
        print("[Info] NOT MATCH ...\n")
        match = False
    fig = plt.figure()
    x_values=np.array(x,dtype=np.float64).reshape(1,-1)
    y_values=np.array(y,dtype=np.float64).reshape(1,-1)
    ax = fig.add_subplot(111)
    ax.axes.get_yaxis().set_visible(False)
    xy_prediction=(prediction, prediction)
    xy_nextnum=(nextnum, nextnum)
    ax.scatter(xy_prediction, xy_prediction, 20, c = 'red')
    ax.scatter(xy_nextnum, xy_nextnum, 20, c = 'green')
    ax.scatter(x_values, y_values, 5, c = 'blue')
    ax.set_xlabel("DATETIME: ["+str(t)+ " ]")
    ax.set_ylabel("")
    if match == False:
        header = "PREDICTION: [ "+prediction+" ] -> [ "+str(nextnum)+ " ] [NOT MATCH]\n"
    else:
        header = "PREDICTION: [ "+prediction+" ] -> [ "+str(nextnum)+ " ] [MATCH !!!]\n"
    plt.title(header)
    print("="*40+"\n")
    if not os.path.exists("dataset/"+str(t)+'_'+str(prediction)+'_'+str(nextnum)+"-prediction.png"):
        fig.savefig("dataset/"+str(t)+'_'+str(prediction)+'_'+str(nextnum)+"-prediction.png")
        print("[Info] Generated 'prediction' image at: dataset/"+str(t)+'_'+str(prediction)+'_'+str(nextnum)+"-prediction.png\n")
    else:
        print("[Info] You have previously saved this 'prediction'...\n")
    fig.canvas.set_window_title("BrAInStocker | Linear Regression Predictor | by psy (https://03c8.net)")
    plt.show()

except:
    print("="*40+"\n")
    print("[Info] This cannot be considered a valid collection for [AI] Linear Regression. Exiting...\n")
