def putComplain(complainString):
    import mysql.connector
    conn = mysql.connector.connect(
        host = "localhost",
        user ="root",
        password = "",
        database = "ProjectDB"
    )
    myCursor = conn.cursor()
    myCursor.execute("insert into complaints values(%s)",(complainString,))  #2nd param is a tuple
    conn.commit()
    conn.close()
########################
# def putComplain(complainString):
#     import mysql.connector
#     conn = mysql.connector.connect(
#         host = "localhost",
#         user ="root",
#         password = "",
#         database = "ProjectDB"
#     )
#     myCursor = conn.cursor()
#     myCursor.execute("select * from complaints")
#     res = myCursor.fetchall()
#     for x in res:
#         print(x[0])

#     conn.close()

#to retrieve & print complains from database