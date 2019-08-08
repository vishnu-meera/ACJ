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

#########CALCULATES RELIABILITY SCORE AT ASSIGNMENT LEVEL AND UPDATES MARIADB#######################################
print('---------------------------ASSIGNMENT LEVEL RELIABILITY SCORES CALCULATIONS---------------------------------------')

df = pd.read_sql("SELECT distinct assignment_id FROM answer_score", con=mariadb_connection)

for index, row in df.iterrows():
     	aid=row['assignment_id']
	print('assignment_id', aid)

	dff = pd.read_sql('SELECT * FROM answer_score where assignment_id = %s', con=mariadb_connection, params=[aid])
	dfscore = dff['score']

	lenscore = len(dfscore)/2

	print('lenscore', lenscore)
	print('score len', len(dfscore))

	firsthalf = np.array(dfscore[0:lenscore])
	secondhalf = np.array(dfscore[lenscore:len(dfscore)])

	if len(firsthalf) == len(secondhalf):
	   firsthalf = np.array(dfscore[0:lenscore])
	   secondhalf = np.array(dfscore[lenscore:len(dfscore)])
	else:
	   firsthalf = np.array(dfscore[0:lenscore])
	   secondhalf = np.array(dfscore[lenscore:len(dfscore)-1])
	
	print('firsthalf', len(firsthalf))
	print('secondhalf', len(secondhalf))
	itemscores = [firsthalf, secondhalf]
	print("Cronbach alpha = ", CronbachAlpha(itemscores))
	dfabs = abs(CronbachAlpha(itemscores))

	print('absolute value', dfabs) 

	mycursor = mariadb_connection.cursor()

	sql = 'UPDATE assignment SET assgnmt_reliab_score= %s	WHERE id = %s'
	val = (dfabs, aid)
	mycursor.execute(sql,val)
	mariadb_connection.commit()
	print(mycursor.rowcount, "record(s) affected in assignment table")

#########CALCULATES RELIABILITY SCORE AT COURSE LEVEL AND UPDATES MARIADB#######################################
print('---------------------------COURSE LEVEL RELIABILITY SCORES CALCULATIONS---------------------------------------')

df2 = pd.read_sql("SELECT distinct course_id FROM assignment where assgnmt_reliab_score is NOT NULL", con=mariadb_connection)

for index, row in df2.iterrows():
     	course_id=row['course_id']
	#print(course_id)

	dff2 = pd.read_sql('SELECT * FROM assignment where course_id = %s', con=mariadb_connection, params=[course_id])
	course_score = dff2['assgnmt_reliab_score']

	print('course level scores', course_score)

	avg_course_score = np.mean(course_score)

	mycursor = mariadb_connection.cursor() 

	sql = 'UPDATE course SET course_reliab_score= %s  WHERE id = %s'
	val = (avg_course_score, course_id)
	mycursor.execute(sql,val)
	mariadb_connection.commit()
	print(mycursor.rowcount, "record(s) affected in course table")

#########CALCULATES RELIABILITY SCORE AT SYSTEM LEVEL AND UPDATES MARIADB#######################################
print('---------------------------SYSTEM LEVEL RELIABILITY SCORES CALCULATIONS---------------------------------------')
df3 = pd.read_sql("SELECT distinct id FROM course where course_reliab_score is NOT NULL", con=mariadb_connection) 

all_course_scores = []
for index, row in df3.iterrows():
     	system_id=row['id']	
	dff3 = pd.read_sql('SELECT * FROM course where id = %s', con=mariadb_connection, params=[system_id])
	system_score = dff3['course_reliab_score']	
	all_course_scores.append(system_score)
	print('all_scores_append', all_course_scores)
	avg_system_score = np.mean(all_course_scores)

df3 = pd.read_sql("SELECT distinct id FROM course where course_reliab_score is NOT NULL", con=mariadb_connection) 

for index, row in df3.iterrows():
     	system_id=row['id']	
	dff3 = pd.read_sql('SELECT * FROM course where id = %s', con=mariadb_connection, params=[system_id])
	mycursor = mariadb_connection.cursor() 
	sql = 'UPDATE course SET system_reliab_score= %s  WHERE id = %s'
	val = (avg_system_score, system_id)
	mycursor.execute(sql,val)
	mariadb_connection.commit()
	print(mycursor.rowcount, "record(s) updated in course table") 































