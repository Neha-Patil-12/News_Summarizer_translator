import sqlite3 as sl

conn=sl.connect("NewsProject.db")
cur=conn.cursor()
#cur.execute("CREATE TABLE favourite (id int PRIMARY KEY,name TEXT NOT NULL,content TEXT NOT NULL)")
res=cur.execute("SELECT name FROM favourite")
for row in res:
    print(row[0])
conn.commit()