import sqlite3 as sql
import pickle
import datetime
import os

import students

kitapMevcutErr = {"msg":"Bu Kodla Bir Kitap Zaten Mevcut", "code":-1, "success":False}
kitapYokErr = {"msg":"Bu Kodla Bir Kitap Yok.", "code":-2, "success":False}
KayitliKitapYokErr = {"msg":"Sistemde Kayıtlı Kitap Yok.", "code":-3, "success":False}
OgrenciKayitliDegilErr = {"msg":"Bu Öğrenci Numarasında Bir Öğrenci Kayıtlı Değil.", "code":-4, "success":False}
OgrencininKitabiVarErr = {"msg":"Bu Öğrenci Numarasına Kayıtlı Öğrencinin Zaten Bir Kitabı Var.", "code":-5, "success":False}
OgrencininKitabiYokErr = {"msg":"Bu Öğrenci Numarasına Kayıtlı Öğrencinin Kitabı Yok.", "code":-6, "success":False}

IslemBasarili = {"msg":"Başarılı", "code":1, "success":True}

def getNextCode(dbName):
    if not os.path.isfile(dbName):
        return 0

    conn = sql.connect(dbName)
    db = conn.cursor()

    # Kontrol İçin Doğru Yol Değil
    try:
        db.execute("SELECT bookCode FROM books ORDER BY bookCode DESC")
    except:
        return 0

    books = db.fetchall()

    if books is None or len(books) <= 0:
        return 0

    return (books[0][0]) + 1

def getBookTypes(dbName):
    conn = sql.connect(dbName)
    db = conn.cursor()

    # Kontrol İçin Doğru Yol Değil
    try:
        db.execute("SELECT DISTINCT bookType FROM books")
    except:
        return KayitliKitapYokErr

    result = db.fetchall()

    result = [x for y in range(len(result)) for x in result[y]]

    return {"msg":result, "code":1, "success":True}

def checkBook(db, bookCode):
    db.execute("""CREATE TABLE IF NOT EXISTS books (bookCode, bookName, bookPage, bookType,
                    bookAuthor, studentNo, takedDate, dateToBeReturn, Date, isAvailable)""")

    db.execute("SELECT bookCode FROM books WHERE bookCode=?", (bookCode,))
    result = db.fetchone()

    return True if result else False

def saveBook(dbName, bookCode, bookName, bookPage, bookType, bookAuthor, studentNo, takedDate=0, dateToBeReturn=0, Date=0):
    """
    :param int bookCode: kitabın kodu
    :param str bookName: kitabın ismi
    :param int bookPage: kitabın sayfa sayısı
    :param str bookType: kitabın türü
    :param str bookAuthor: kitap yazarı
    :param array studentNo: kitabı almış öğrencilerin numaraları. 0. eleman kitabı okul kütüphanesi vermiş olan öğrencinin numarasıdır.
    sonuncu eleman ise kitabı en son almış olan öğrencinin numarasıdır.
    :param datetime takedDate: kitap öğrencideyse kitabı aldığı tarih. Değilse 0.
    :param datetime dateToBeReturn: kitap öğrencideyse kitabı teslim etmesi gereken tarih. Değilse 0.
    :param datetime Date: kitabın okul kütüphanesine verildiği tarih.
    :param bool isAvailable: kitap mevcut mu?
    :return:
    """
    conn = sql.connect(dbName)
    db = conn.cursor()

    db.execute("""CREATE TABLE IF NOT EXISTS books (bookCode, bookName, bookPage, bookType,
                bookAuthor, studentNo, takedDate, dateToBeReturn, Date, isAvailable)""")

    if checkBook(db, bookCode):
        conn.close()
        return kitapMevcutErr

    addBook = "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    db.execute(addBook, (bookCode, bookName,
                         bookPage, bookType,
                         bookAuthor, pickle.dumps(studentNo,
                                                  protocol=5),
                         takedDate,
                         dateToBeReturn, Date, True))

    conn.commit()
    conn.close()

    return IslemBasarili

def updateBook(dbName, bookCode, bookName, bookPage, bookType, bookAuthor, studentNo, takedDate, dateToBeReturn, Date, isAvailable):
    """
    :param int bookCode: kitabın kodu
    :param str bookName: kitabın ismi
    :param int bookPage: kitabın sayfa sayısı
    :param str bookType: kitabın türü
    :param str bookAuthor: kitap yazarı
    :param array studentNo: kitabı almış öğrencilerin numaraları. 0. eleman kitabı okul kütüphanesi vermiş olan öğrencinin numarasıdır.
    sonuncu eleman ise kitabı en son almış olan öğrencinin numarasıdır.
    :param float takedDate: kitap öğrencideyse kitabı aldığı tarih. Değilse 0.
    :param float dateToBeReturn: kitap öğrencideyse kitabı teslim etmesi gereken tarih. Değilse 0.
    :param float Date: kitabın okul kütüphanesine verildiği tarih.
    :param bool isAvailable: kitap mevcut mu?
    :return:
    """
    conn = sql.connect(dbName)
    db = conn.cursor()

    if not checkBook(db, bookCode):
        conn.close()
        return kitapYokErr

    db.execute("""UPDATE books set bookName=?, bookPage=?, bookType=?,
                bookAuthor=?, studentNo=?, takedDate=?,
                dateToBeReturn=?, Date=?,
                isAvailable=? WHERE bookCode=?""", (bookName, bookPage, bookType,
                                                    bookAuthor,
                                                    pickle.dumps(studentNo,
                                                                 protocol=5),
                                                    takedDate, dateToBeReturn,
                                                    Date, isAvailable, bookCode))

    conn.commit()
    conn.close()

    return IslemBasarili

def RemoveBook(dbName, sdb, bookCode):
    conn = sql.connect(dbName)
    db = conn.cursor()

    if not checkBook(db, bookCode):
        conn.close()
        return kitapYokErr

    bk = getBook(dbName, bookCode)

    if not bk[8]:
        takeBook(sdb, dbName, bookCode)

    db.execute("DELETE FROM books WHERE bookCode=?", (bookCode,))

    conn.commit()
    conn.close()

    return IslemBasarili

def giveBook(sdb, dbName, bookCode, studentNo, howManyDays):
    student = students.getStudent(sdb, studentNo)
    book = getBook(dbName, bookCode)

    if not book:
        return kitapYokErr

    if not student:
        return OgrenciKayitliDegilErr

    if student[-1]:
        return OgrencininKitabiVarErr

    now = datetime.datetime.now().timestamp()
    mustGive = (datetime.datetime.now() + datetime.timedelta(days=howManyDays)).timestamp()

    book[4].append(student[0])
    student[4].append(bookCode)

    students.updateStudent(sdb, student[0], student[1], student[2], student[3], student[4], True)
    updateBook(dbName, bookCode, book[0], book[1], book[2], book[3], book[4],
               now, mustGive, book[7], False)

    return IslemBasarili

def takeBook(sdb, dbName, bookCode):
    book = getBook(dbName, bookCode)

    if not book:
        return kitapYokErr

    studentNo = book[4][-1]
    student = students.getStudent(sdb, studentNo)

    if not student:
        return OgrenciKayitliDegilErr

    if not student[5]:
        return OgrencininKitabiVarErr

    students.updateStudent(sdb, student[0], student[1], student[2], student[3], student[4], False)
    updateBook(dbName, bookCode, book[0], book[1], book[2], book[3], book[4],
               0.0, 0.0, book[7], True)

    return IslemBasarili

def getBook(dbName, bookCode):
    conn = sql.connect(dbName)
    db = conn.cursor()

    if not checkBook(db, bookCode):
        conn.close()
        return False

    db.execute("""SELECT bookName, bookPage, bookType, bookAuthor,
                         studentNo, takedDate, dateToBeReturn, Date,
                         isAvailable FROM books WHERE bookCode=?""", (bookCode,))

    result = db.fetchall()

    result = [x for x in result[0]]
    result[4] = pickle.loads(result[4])

    conn.close()

    return result
