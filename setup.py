import mysql.connector as ms

try:
    mydb = ms.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Junebug05_",
        database = "db4710_proj",
    )
    if mydb.is_connected():
        print("Sucess!")
        mycur=mydb.cursor()
        #mycur.execute("Create Table testUser(MemID int primary key auto_increment, fName VarChar(100), lName VarChar(100), gender VarChar(10), DOB date, height float, activity VarChar(100), weight float, goal VarChar(100))")
        mycur.execute("show tables")
        for x in mycur:
            print(x)    
    
except ms.connector.Error as e:
    print("Error", e)


    
