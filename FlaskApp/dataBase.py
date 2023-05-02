import sqlite3 as sl

conn=sl.connect("NewsProject.db")
cur=conn.cursor()

#cur.execute('''CREATE TABLE Page (id INTEGER PRIMARY KEY,title TEXT NOT NULL, description TEXT ,transTitle TEXT,transPara TEXT,created_date DATE  DEFAULT (datetime('now', 'localtime')),user_id INTEGER NOT NULL)''')
#cur.execute('''CREATE TABLE register(id INTEGER PRIMARY KEY,username TEXT NOT NULL,password TEXT NOT NULL)''')
#cur.execute('''INSERT INTO register(username,password) VALUES('Disha','disha')''' )

res=cur.execute('''SELECT * FROM Page''' )
for row in res:
    print(row[0])
    print(row[1])
    print(row[3])
    print(row[6])

conn.commit()
conn.close()
