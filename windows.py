from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo

import datetime

import books
import students


def isEmpty(value: str):
    return True if not value else False


class windows:
    def __init__(self, sDB, bDB):
        """
        :param string sDB: öğrenci db sine verilecek ad
        :param bDB: kitap db sine verilecek ad
        """
        self.sdb = sDB
        self.bdb = bDB

    def main(self):
        def giveTakeBook():
            top.destroy()
            self.giveTake()

        def getInfo():
            top.destroy()
            self.getInfos()

        def save():
            top.destroy()
            self.save()

        def update():
            top.destroy()
            self.update()

        def remove():
            top.destroy()
            self.remove()

        top = Tk()
        top.geometry("300x80")
        top.title("Kütüphane")

        ttk.Button(top, text="Kitap AL - VER", command=giveTakeBook).place(x=0, y=0)
        ttk.Button(top, text="Veri Al", command=getInfo).place(x=100, y=0)
        ttk.Button(top, text="Kayıt", command=save).place(x=0, y=30)
        ttk.Button(top, text="Veri Güncelle", command=update).place(x=100, y=30)
        ttk.Button(top, text="Veri Sil", command=remove).place(x=200, y=30)

        top.mainloop()

    def update(self):
        def updateBook():
            value = [kitapKod, kitapIsim, kitapSayfa, kitapTur, kitapYazar, ogrenciNo]

            for i in value:
                if isEmpty(str(i.get())):
                    showerror("Değer Boş", "Kitabı Güncellemek İçin Herhangi Bir Değer Boş Olamaz")
                    return

            book = books.getBook(self.bdb, kitapKod.get())

            if not book:
                showerror("Kitap Yok", "Girmiş Olduğunuz Kodla Kitap Bulunmamaktadır.")
                return

            books.updateBook(self.bdb, kitapKod.get(), kitapIsim.get(), int(kitapSayfa.get()), kitapTur.get(),
                             kitapYazar.get(), [ogrenciNo.get()], book[5], book[6], book[7], book[8])

            for i in value:
                i.set("0")

            showinfo("Kitap Güncellendi", "Kodunu Girmiş Olduğunuz Kitap Başarıyla Güncellendi.")

        def updateStudent():
            value = [ogrenci_no, ogrenci_isim, ogrenci_sinif]

            for i in value:
                if isEmpty(str(i.get())):
                    showerror("Değer Boş", "Öğrenci Güncellemek İçin Herhangi Bir Değer Boş Olamaz")
                    return

            student = students.getStudent(self.sdb, ogrenci_no.get())

            if not student:
                showerror("Öğrenci Yok", "Bu Öğrenci Numarasıyla Kayıtlı Öğrenci Bulunamadı")
                return

            students.updateStudent(self.sdb, ogrenci_no.get(), ogrenci_isim.get(), ogrenci_sinif.get(),
                                   student[3], student[4], student[5])

            for i in value:
                i.set("0")

            showinfo("Öğrenci Güncellendi", "Numarasını Girmiş Olduğunuz Öğrenci Başarıyla Güncellendi.")

        def returnMain():
            top.destroy()
            self.main()

        top = Tk()
        top.geometry("600x250")
        top.title("Bilgi Güncelle")

        # book
        kitapKod = IntVar(value="")
        kitapIsim = StringVar()
        kitapSayfa = StringVar()
        kitapTur = StringVar()
        kitapYazar = StringVar()
        ogrenciNo = IntVar(value="")

        ttk.Label(text="Kitap Kodu: ").place(x=0, y=0)
        ttk.Label(text="Kitap İsmi: ").place(x=0, y=60)
        ttk.Label(text="Sayfa Sayısı: ").place(x=0, y=90)
        ttk.Label(text="Kitap Yazarı: ").place(x=0, y=120)
        ttk.Label(text="Öğrenci Numarası: ").place(x=0, y=150)
        ttk.Label(text="Kitap Türü Seç: ").place(x=0, y=180)

        ttk.Entry(top, textvariable=kitapKod, width=20).place(x=110, y=0)
        ttk.Entry(top, textvariable=kitapIsim, width=20).place(x=110, y=60)
        ttk.Entry(top, textvariable=kitapSayfa, width=20).place(x=110, y=90)
        ttk.Entry(top, textvariable=kitapYazar, width=20).place(x=110, y=120)
        ttk.Entry(top, textvariable=ogrenciNo, width=20).place(x=110, y=150)

        type = ttk.Combobox(top, textvariable=kitapTur, width=20)

        types = books.getBookTypes(self.bdb)

        if types["success"]: type["values"] = types["msg"]

        type.place(x=110, y=180)

        ttk.Button(top, text="Kitabı Güncelle", command=updateBook).place(x=55, y=220)

        # student
        ogrenci_no = IntVar(value="")
        ogrenci_isim = StringVar()
        ogrenci_sinif = StringVar()

        ttk.Label(text="Öğrenci No: ").place(x=320, y=0)
        ttk.Label(text="Öğrenci İsmi: ").place(x=320, y=60)
        ttk.Label(text="Öğrenci Sınıf: ").place(x=320, y=90)

        ttk.Entry(top, textvariable=ogrenci_no, width=20).place(x=430, y=0)
        ttk.Entry(top, textvariable=ogrenci_isim, width=20).place(x=430, y=60)
        ttk.Entry(top, textvariable=ogrenci_sinif, width=20).place(x=430, y=90)

        ttk.Button(top, text="Öğrenciyi Güncelle", command=updateStudent).place(x=395, y=130)

        ttk.Button(top, text="Ana Ekrana Dön", command=returnMain).place(x=400, y=220)

        top.mainloop()

    def remove(self):
        def removeBook():
            if isEmpty(str(kitapKod.get())):
                showerror("Değer Boş", "Silmek İstediğiniz Kitabın Kodunu Yazmanız Gerekmektedir.")
                return

            book = books.getBook(self.bdb, kitapKod.get())

            if not book:
                showerror("Kitap Yok", "Kodunu Girmiş Olduğunuz Kitap Zaten Sistemde Kayıtlı Değil.")
                return

            books.RemoveBook(self.bdb, self.sdb, kitapKod.get())

            kitapKod.set("0")

            showinfo("Kitap Silindi", "Kodunu Girmiş Olduğunuz Kitap Başarıyla Silindi.")

        def removeStudent():
            if isEmpty(str(ogrenciNo.get())):
                showerror("Değer Boş", "Silmek İstediğiniz Öğrencinin Numarasını Girmeniz Gerekmektedir.")
                return

            student = students.getStudent(self.sdb, ogrenciNo.get())

            if not student:
                showerror("Öğrenci Yok", "Girmiş Olduğunuz Öğrenci Numarasıyla Sisteme Kayıtlı Öğrenci Bulunamadı.")
                return

            students.RemoveStudent(self.sdb, self.bdb, ogrenciNo.get())

            ogrenciNo.set("0")

            showinfo("Öğrenci Silindi", "Numarasını Girmiş Olduğunuz Öğrenci Başarıyla Silindi.")

        def returnMain():
            top.destroy()
            self.main()

        top = Tk()
        top.geometry("450x100")
        top.title("Sil")

        kitapKod = IntVar()
        ogrenciNo = IntVar()

        ttk.Label(text="Kitap Kodu: ").place(x=0, y=0)
        ttk.Label(text="Oğrenci No: ").place(x=230, y=0)

        ttk.Entry(top, textvariable=kitapKod, width=20).place(x=80, y=0)
        ttk.Entry(top, textvariable=ogrenciNo, width=20).place(x=310, y=0)

        ttk.Button(top, text="Kitabı Sil", command=removeBook).place(x=40, y=35)
        ttk.Button(top, text="Öğrenciyi Sil", command=removeStudent).place(x=270, y=35)

        ttk.Button(top, text="Ana Ekrana Dön", command=returnMain).place(x=0, y=75)

        top.mainloop()

    def getInfos(self):
        def strToDate(t=None, diff=False, ts=[]):
            if diff:
              return (datetime.datetime.fromtimestamp(float(ts[0])) - datetime.datetime.fromtimestamp(float(ts[1]))).days

            d = datetime.datetime.fromtimestamp(float(t)).day
            m = datetime.datetime.fromtimestamp(float(t)).month
            y = datetime.datetime.fromtimestamp(float(t)).year
            return "{}/{}/{}".format(d, m, y)

        def secondScreen(book:bool, arr, txt):
            second = Tk()
            second.geometry("300x430")
            second.title("Kitap" if book else "Öğrenci")

            lBox = Listbox(second, height=20,
                           width=10, bg="white",
                           activestyle="dotbox",
                           font="Helvetica",
                           fg="black")

            for i, e in enumerate(arr):
                lBox.insert(i, str(e))

            ttk.Label(master=second, text=txt).place(x=100, y=0)

            lBox.place(x=0, y=0)

        def getBook():
            if isEmpty(str(kitapKod.get())):
                showerror("Değer Boş", "Kitap Bilgilerini Görmek İstediğiniz Kitabın Kodunu Yazın.")
                return

            book = books.getBook(self.bdb, kitapKod.get())

            if not book:
                showerror("Kitap Yok", "Kodunu Girmiş Olduğunuz Kitap Sistemde Kayıtlı Değil.")
                return

            # Kitap Mevcutsa
            if book[8]:
                text = "İsmi: {}\nSayfa Sayısı: {}\nKitap Türü: {}\nYazarı: {}\nGetiren Öğrenci: {}\nKitap MEVCUT".format(
                    book[0], book[1], book[2], book[3], book[4][0]
                )
            else:
                text = "İsmi: {}\nSayfa Sayısı: {}\nKitap Türü: {}\nYazarı: {}\nGetiren Öğrenci: {}\n" \
                       "Alınma Tarihi: {}\nTeslim Tarihi: {}\nKalan Gün: {}\nKitap MEVCUT DEĞİL".format(
                    book[0], book[1], book[2], book[3], book[4][0], strToDate(book[5]), strToDate(book[6]),
                    strToDate(diff=True, ts=[book[6], datetime.datetime.now().timestamp()])
                )

            stArr = book[4][::-1]
            secondScreen(book=True, arr=stArr, txt=text)

        def getStudent():
            if isEmpty(str(ogrenciNo.get())):
                showerror("Değer Boş", "Öğrenci Bilgilerini Alabilmek İçin Öğrenci Numarasını Giriniz.")
                return

            student = students.getStudent(self.sdb, ogrenciNo.get())

            if not student:
                showerror("Öğrenci Yok", "Girmiş Olduğunuz Numarada Sistemde Kayıtlı Öğrenci Yok")
                return

            text = "İsmi: {}\nSınıf: {}\nKayıt Tarihi: {}\nKitap {}".format(
                student[1], student[2], strToDate(t=student[3]), "ALABİLİR" if not student[5] else "ALAMAZ"
            )

            bookArr = student[4][::-1]
            secondScreen(book=False, arr=bookArr, txt=text)

        def returnMain():
            top.destroy()
            self.main()

        top = Tk()
        top.geometry("500x100")
        top.title("Bilgi Al")

        kitapKod = IntVar()
        ogrenciNo = IntVar()

        ttk.Label(text="Kitap Kodu: ").place(x=0, y=0)
        ttk.Label(text="Oğrenci No: ").place(x=230, y=0)

        ttk.Entry(top, textvariable=kitapKod, width=20).place(x=80, y=0)
        ttk.Entry(top, textvariable=ogrenciNo, width=20).place(x=310, y=0)

        ttk.Button(top, text="Kitabı Getir", command=getBook).place(x=40, y=35)
        ttk.Button(top, text="Öğrenciyi Getir", command=getStudent).place(x=270, y=35)

        ttk.Button(top, text="Ana Ekrana Dön", command=returnMain).place(x=0, y=70)

        top.mainloop()

    def giveTake(self):
        def Al(book, student):
            if isEmpty(str(kitapKod.get())):
                showerror("Değer Boş", "Kitabı Teslim Almak İçin Kitabın Kodunun Giriniz.")
                return

            check = books.getBook(self.bdb, kitapKod.get())

            if not check:
                showerror("Kitap Yok", "Bu Kodla Bir Kitap Sistemde Kayıtlı Değil")
                return

            values = [kitapKod, ogrenciNo, gun]

            books.takeBook(self.sdb, self.bdb, kitapKod.get())

            for i in values:
                if i is gun:
                    i.set("30")
                    continue

                i.set("0")

            showinfo("Kitap Alındı", "Kitap Öğrenciden Başarıyla Teslim Alındı.")

        def Ver(book, student):
            values = [kitapKod, ogrenciNo, gun]

            if isEmpty(str(gun.get())) or gun.get() <= 0:
                showerror("Gün sayısı",
                          "Gün sayısının girilmemesi, 0 veya 0'dan küçük değer girilmesinden kaynaklı hata")
                return

            books.giveBook(self.sdb, self.bdb, kitapKod.get(), ogrenciNo.get(), gun.get())

            for i in values:
                if i is gun:
                    i.set("30")
                    continue

                i.set("0")

            showinfo("Kitap Verildi", "Kitap Öğrenciye Başarıyla Teslim Edildi.")

        def alVerKarar():
            values = [kitapKod, ogrenciNo, gun]

            for i in values:
                if isEmpty(str(i.get())):
                    showerror("Değer Boş", "kitap alıp vermek için temel değer boş olamaz.")
                    return

            book = books.getBook(self.bdb, kitapKod.get())
            student = students.getStudent(self.sdb, ogrenciNo.get())

            if not book:
                showerror("Kitap Yok", "Sitemde Bu Kodla Kayıtlı Bir Kitap Yok.")
                return


            if not student:
                showerror("Öğrenci Yok", "Sitemde Bu numarayla Kayıtlı Bir Öğrenci Yok.")
                return

            # kitap alınabilir değil
            if not book[8]:
                # Öğrencinin kitabı yok
                if not student[5]:
                    showerror("Kitap Mevcut Değil", "Kitap şuanda başka bir öğrencide({}).".format(book[4][-1]))
                    return

                # Öğrencinin kitabı var
                if student[4][-1] == kitapKod.get():
                    return Al(book, student)

                showerror("Kitabı Var", "Öğrencinin elinde başka bir kitap({}) var.".format(student[4][-1]))
                return

            # Kitap Alınabilir
            # Öğrencinin kitabı var
            if student[5]:
                showerror("Kitabı Var", "Lütfen önce elinizdeki kitabı({}) teslim edin.".format(student[4][-1]))
                return

            # Öğrencinin kitabı yok
            return Ver(book, student)

        def returnMain():
            top.destroy()
            self.main()

        top = Tk()
        top.geometry("300x150")
        top.title("Kitap Al-Ver")

        kitapKod = IntVar()
        ogrenciNo = IntVar()
        gun = IntVar(value="30")

        ttk.Label(text="Kitap Kodu: ").place(x=0, y=0)
        ttk.Label(text="Oğrenci No: ").place(x=0, y=30)
        ttk.Label(text="Kaç Gün: ").place(x=0, y=60)

        ttk.Entry(top, textvariable=kitapKod, width=20).place(x=110, y=0)
        ttk.Entry(top, textvariable=ogrenciNo, width=20).place(x=110, y=30)
        ttk.Entry(top, textvariable=gun, width=20).place(x=110, y=60)

        ttk.Button(top, text="Kitabı Al-Ver", command=alVerKarar).place(x=55, y=100)

        ttk.Button(top, text="Ana Ekrana Dön", command=returnMain).place(x=200, y=120)

        top.mainloop()

    def save(self):
        def saveBook():
            values = [kitapKod, kitapIsim, kitapSayfa, kitapTur, kitapYazar, ogrenciNo]

            for i in values:
                if isEmpty(str(i.get())):
                    showerror("Değer Boş", "Kitap Kayıdındaki Herhangi Bir Yer Boş Bırakılamaz.")
                    return

            ogrenci = students.getStudent(self.sdb, int(ogrenciNo.get()))

            if books.getBook(self.bdb, kitapKod.get()):
                showerror("Mevcut", "Bu Kodla Zaten Bir Kitap Var. Kitabı Silmeyi veya Güncellemeyi deneyin.")
                return

            if not ogrenci:
                showerror("Öğrenci Yok", "Bu Öğrenci Numarasıyla Kayıtlı Bir Öğrenci Bulunamadı. Lütfen Önce Öğrenciyi Kaydedin.")
                return

            books.saveBook(self.bdb, kitapKod.get(), kitapIsim.get(), int(kitapSayfa.get()),
                           kitapTur.get(), kitapYazar.get(), [int(ogrenciNo.get())], Date=datetime.datetime.now().timestamp())

            ogrenci[4].append(kitapKod.get())
            students.updateStudent(self.sdb, ogrenci[0], ogrenci[1], ogrenci[2], ogrenci[3], ogrenci[4], ogrenci[5])

            for i in values:
                if i is kitapKod:
                    i.set(value=books.getNextCode(self.bdb))
                    continue

                if i is ogrenciNo:
                    i.set(value="-1")
                    continue

                if i is kitapTur:
                    type["values"] = books.getBookTypes(self.bdb)["msg"]

                i.set("")

            showinfo("Kayıt Başarılı", "Kitap Kaydı Başarıyla Oluşturuldu.")

        def saveStudent():
            values = [ogrenci_no, ogrenci_isim, ogrenci_sinif]

            for i in values:
                if isEmpty(str(i.get())):
                    showerror("Değer Boş", "Öğrenci Kayıdındaki Herhangi Bir Yer Boş Bırakılamaz.")
                    return

            now = datetime.datetime.now().timestamp()
            save = students.saveStudent(self.sdb, ogrenci_no.get(), ogrenci_isim.get(), ogrenci_sinif.get(), now)

            if not save["success"]:
                showerror("Öğrenci Kaydedilemedi", save["msg"])
                return

            for i in values:
                if i is ogrenci_no:
                    i.set(value="0")
                    continue

                i.set(value="")

            showinfo("Kayıt Başarılı", "Öğrenci Kaydı Başarıyla Oluşturuldu.")

        def returnMain():
            top.destroy()
            self.main()

        top = Tk()
        top.geometry("600x250")
        top.title("Kayıt")

        # book
        kitapKod = IntVar(value=books.getNextCode(self.bdb, ))
        kitapIsim = StringVar()
        kitapSayfa = StringVar()
        kitapTur = StringVar()
        kitapYazar = StringVar()
        ogrenciNo = IntVar(value=-1)

        ttk.Label(text="Kitap Kodu: ").place(x=0, y=0)
        ttk.Label(text="Kitap İsmi: ").place(x=0, y=30)
        ttk.Label(text="Sayfa Sayısı: ").place(x=0, y=60)
        ttk.Label(text="Kitap Yazarı: ").place(x=0, y=90)
        ttk.Label(text="Öğrenci Numarası: ").place(x=0, y=120)
        ttk.Label(text="Kitap Türü Seç: ").place(x=0, y=150)

        ttk.Entry(top, textvariable=kitapKod, width=20).place(x=110, y=0)
        ttk.Entry(top, textvariable=kitapIsim, width=20).place(x=110, y=30)
        ttk.Entry(top, textvariable=kitapSayfa, width=20).place(x=110, y=60)
        ttk.Entry(top, textvariable=kitapYazar, width=20).place(x=110, y=90)
        ttk.Entry(top, textvariable=ogrenciNo, width=20).place(x=110, y=120)

        type = ttk.Combobox(top, textvariable=kitapTur, width=20)

        types = books.getBookTypes(self.bdb)

        if types["success"]: type["values"] = types["msg"]

        type.place(x=110, y=150)

        ttk.Button(top, text="Kitabı Kaydet", command=saveBook).place(x=55, y=180)

        # student
        ogrenci_no = IntVar()
        ogrenci_isim = StringVar()
        ogrenci_sinif = StringVar()

        ttk.Label(text="Öğrenci No: ").place(x=320, y=0)
        ttk.Label(text="Öğrenci İsmi: ").place(x=320, y=30)
        ttk.Label(text="Öğrenci Sınıf: ").place(x=320, y=60)

        ttk.Entry(top, textvariable=ogrenci_no, width=20).place(x=430, y=0)
        ttk.Entry(top, textvariable=ogrenci_isim, width=20).place(x=430, y=30)
        ttk.Entry(top, textvariable=ogrenci_sinif, width=20).place(x=430, y=60)

        ttk.Button(top, text="Öğrenciyi Kaydet", command=saveStudent).place(x=395, y=100)

        ttk.Button(top, text="Ana Ekrana Dön", command=returnMain).place(x=500, y=220)

        top.mainloop()
