import numpy as np
import pandas as pd
import mysql.connector as mariadb
from mysql.connector import Error

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

mariadb_connection = mariadb.connect(host='127.0.0.1',
                             port='13306',
                             database='compair',
                             user='root',
                             password='randompassword')

df = pd.read_sql("SELECT distinct assignment_id FROM answer_score", con=mariadb_connection)

for index, row in df.iterrows():
     	aid=row['assignment_id']
	print(aid)

	dff = pd.read_sql('SELECT * FROM answer_score where assignment_id = %s', con=mariadb_connection, params=[aid])
	print('dff',dff) 
	dfscore = dff['score']

	print('dfscore', dfscore)

	lenscore = len(dfscore)/2

	print('lenscore', lenscore)

	firsthalf = np.array(dfscore[0:lenscore])
	secondhalf = np.array(dfscore[lenscore:len(dfscore)])

	#print('firsthalf', len(firsthalf))
	#print('secondhalf', len(secondhalf))
	itemscores = [firsthalf, secondhalf]
	print("Cronbach alpha = ", CronbachAlpha(itemscores))
	dfabs = abs(CronbachAlpha(itemscores))

	print('absolute value', dfabs) 

	mycursor = mariadb_connection.cursor()

	sql = 'UPDATE assignment SET assgnmt_reliab_score= %s	WHERE id = %s'
	val = (dfabs, aid)
	mycursor.execute(sql,val)
	mariadb_connection.commit()
	print("hello")
	print(mycursor.rowcount, "record(s) affected")














