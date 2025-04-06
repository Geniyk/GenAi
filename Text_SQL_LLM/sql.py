import sqlite3

## connect to sqlite
connection=sqlite3.connect("student.db")

## Create s cursor  object to insert record, create table, retrieve
cursor=connection.cursor()

## Create  table
table_info= """
Create  table STUDENT(NAME, CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT);

"""
cursor.execute(table_info)

## Insert Some more records

cursor.execute('''Insert Into STUDENT values('Saurabh','Ece(IoT)','B',90)''')
cursor.execute('''Insert Into STUDENT values('Ayushi','Zoology','A',95)''')
cursor.execute('''Insert Into STUDENT values('Rahul','Mechanical','C',78)''')
cursor.execute('''Insert Into STUDENT values('Neha','Electrical','B',92)''')
cursor.execute('''Insert Into STUDENT values('Amit','Civil','A',88)''')


## Display all records
print("The inserted records are")

data=cursor.execute('''Select * from STUDENT ''')

for row in data:
    print(row)


## close the connection

connection.commit()
connection.close()
