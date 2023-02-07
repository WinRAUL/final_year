import mysql.connector, hashlib
conn = mysql.connector.connect(
    host = "localhost",
    user ="root",
    password = "",
    database = "ProjectDB"
)

def putComplain(complainString):
    myCursor = conn.cursor()
    myCursor.execute("insert into complaints values(%s)",(complainString,))  #2nd param is a tuple
    conn.commit()
    conn.close()

def verifyLogin(email, password):
    hash_object = hashlib.md5(password.encode())
    password = hash_object.hexdigest()
    myCursor = conn.cursor()
    myCursor.execute("select * from users where Email=%s AND Pass=%s",(email,password,))
    res = myCursor.fetchall()
    conn.close()
    if(bool(res)):
        return True
    else:
        return False

########################
# def putComplain(complainString):
#     myCursor = conn.cursor()
#     myCursor.execute("select * from complaints")
#     res = myCursor.fetchall()
#     for x in res:
#         print(x[0])

#     conn.close()

#to retrieve & print complains from database