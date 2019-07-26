import mysql.connector
from mysql.connector import Error


connection = mysql.connector.connect(host='172.20.0.3',
                             port='3306',
                             database='compair',
                             user='root',
                             password='randompassword')
import numpy as np

def svar(X):
    n = float(len(X))
    svar=(sum([(x-np.mean(X))**2 for x in X]) / n)* n/(n-1.)
    return svar

def CronbachAlpha(itemscores):
    itemvars = [svar(item) for item in itemscores]
    tscores = [0] * len(itemscores[0])
    for item in itemscores:
       for i in range(len(item)):
          tscores[i]+= item[i]
    nitems = len(itemscores)
    print("total scores=", tscores, 'number of items=', nitems)

    Calpha=nitems/(nitems-1.) * (1-sum(itemvars)/ svar(tscores))

    return Calpha

itemscores = [[ 1200, 1190, 1210, 1200, 1200,  1200, 1210, 1190, 1190.28, 1220, 1229.86, 1210.14, 1219.72, 1209.71,1180,],
              [ 1200, 1190, 1210, 1200, 1200, 1200, 1210, 1170.29, 1190, 1199.71, 1210, 1180.29, 1190, 1210, 1180]]
print("Cronbach alpha = ", CronbachAlpha(itemscores))





