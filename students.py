import sqlite3 as sql
import pickle

import books


def checkStudent(dbName, db, studentNo):
    db.execute("CREATE TABLE IF NOT EXISTS students (studentNo, studentName, studentClass, savedDate, books, haveBook)")

    db.execute("SELECT studentNo FROM students WHERE studentNo=?", (studentNo,))
    result = db.fetchone()

    if result is None and studentNo == -1:
        saveStudent(dbName, -1, "OKUL", 0, 0, control=False)
        return True

    return True if result else False

def saveStudent(dbName, studentNo, studentName, studentClass, savedDate, books=[], haveBook=False, control=True):
    conn = sql.connect(dbName)
    db = conn.cursor()

    if control:
        if checkStudent(dbName, db, studentNo):
            return {"msg":"Bu Öğrenci Numarasıyla Bir Öğrenci Zaten Kayıtlı.", "code":-1, "success":False}

    addStudent = "INSERT INTO students VALUES (?, ?, ?, ?, ?, ?)"

    db.execute(addStudent, (studentNo, studentName, studentClass, savedDate, pickle.dumps(books, protocol=5), haveBook))

    conn.commit()
    conn.close()

    return {"msg":"", "code":1, "success":True}

def updateStudent(dbName, studentNo, studentName, studentClass, savedDate, books, haveBook):
    conn = sql.connect(dbName)
    db = conn.cursor()

    if not checkStudent(dbName, db, studentNo):
        conn.close()
        return False

    db.execute("""UPDATE students set studentName=?, studentClass=?, books=?,
                haveBook=? WHERE studentNo=?""", (studentName, studentClass, pickle.dumps(books, protocol=5),
                                                  haveBook, studentNo))

    conn.commit()

    conn.close()

    return True

def RemoveStudent(dbName, bdb, studentNo):
    conn = sql.connect(dbName)
    db = conn.cursor()

    if not checkStudent(dbName, db, studentNo):
        conn.close()
        return False

    st = getStudent(dbName, studentNo)

    if st[5]:
        books.takeBook(dbName, bdb, st[4][-1])

    db.execute("DELETE FROM students WHERE studentNo=?", (studentNo,))

    conn.commit()
    conn.close()

    return True

def getStudent(dbName, studentNo):
    conn = sql.connect(dbName)
    db = conn.cursor()

    if not checkStudent(dbName, db, studentNo):
        conn.close()
        return False

    db.execute("SELECT studentNo, studentName, studentClass, savedDate, books, haveBook FROM students WHERE studentNo=?",
               (studentNo,))
    result = db.fetchall()

    result = [x for x in result[0]]
    result[4] = pickle.loads(result[4])

    conn.close()

    return result
