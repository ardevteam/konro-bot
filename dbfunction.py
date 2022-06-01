import sys, mysql.connector
from unicodedata import decimal
from mysql.connector import errorcode
from datetime import datetime
from decimal import *

# Database
try:
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",      
      database="db_konro"
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    sys.exit()
  else:
    print(err)
    sys.exit()
sql = db.cursor()

def ceklogin(id):
    sql.execute("SELECT idtelegram FROM mahasiswa WHERE idtelegram = "+id+"")
    hasil_sql = sql.fetchall()

    return sql.rowcount

def ceknim(nim,email):
    sql.execute("SELECT nim FROM mahasiswa WHERE nim = '"+nim+"' AND email = '"+email+"'")
    hasil_sql = sql.fetchall()

    #jumlah baris
    return sql.rowcount

def daftaruser(idtelegram,nim):
    sql.execute("UPDATE mahasiswa SET idtelegram = '"+idtelegram+"' WHERE nim = '"+nim+"'")
    db.commit()

def getKodeKelompok(idtelegram):
    sql.execute("SELECT kodekelompok FROM mahasiswa WHERE idtelegram = '"+idtelegram+"'")
    hasil_sql = sql.fetchone()

    return hasil_sql[0]

def getpekan(idtelegram):

    kodekelompok = getKodeKelompok(idtelegram)

    sql.execute("SELECT kodekelompok FROM pr WHERE kodekelompok = '"+kodekelompok+"'")
    hasil_sql = sql.fetchall()

    hasil = int(sql.rowcount)

    if hasil == 0:
        hasil = 8
    else:
        hasil = hasil+8

    return hasil

def getProfile(idtelegram):
    sql.execute("SELECT idmahasiswa, nim, nama, username, kodekelompok FROM mahasiswa WHERE idtelegram = '"+idtelegram+"'")
    # 0 idmahasiswa
    # 1 nim
    # 2 nama
    # 3 username
    # 4 kodekelompok
    hasil_sql = sql.fetchone()

    return hasil_sql

def getAplikasi(idtelegram):
    kodekelompok = getKodeKelompok(idtelegram)
    sql.execute("SELECT idaplikasi, namaaplikasi, deskripsi FROM aplikasi WHERE kodekelompok  = '"+kodekelompok +"'")
    # 0 idaplikasi
    # 1 namaaplikasi 
    # 2 deskripsi
    hasil_sql = sql.fetchone()

    return hasil_sql

def getRating(idaplikasi):

    sql.execute("SELECT sum(rating) FROM rating WHERE idaplikasi = '"+str(idaplikasi)+"'")
    sumrating = sql.fetchone()[0]

    sql.execute("SELECT rating FROM rating WHERE idaplikasi = '"+str(idaplikasi)+"'")
    sql.fetchall()
    jumlahrating = int(sql.rowcount)    

    if jumlahrating > 0:
        ratarata = sumrating / jumlahrating
        hasil = str(round(ratarata,2))+" dari "+str(jumlahrating)
    else:
        hasil = '0 (Belum ada rating)'

    return hasil

def getNamaapk(idaplikasi):
    sql.execute("SELECT namaaplikasi FROM aplikasi WHERE idaplikasi  = '"+idaplikasi +"'")
    # 0 namaaplikasi 
    hasil_sql = sql.fetchone()

    return hasil_sql[0]

def inputpr(idtelegram,data):

    kodekelompok = getProfile(idtelegram)[4]
    pekan = getpekan(idtelegram)
    entryby = getProfile(idtelegram)[2]
    dateentry = datetime.today().strftime('%Y-%m-%d')
    detail = data
    username = getProfile(idtelegram)[3]
    entryfrom = 'Bot Telegram'

    insert = 'INSERT INTO pr (kodekelompok, pekan, entryby, dateentry, detail, username, entryfrom) VALUES (%s,%s,%s,%s,%s,%s,%s)'
    val = (kodekelompok, pekan, entryby, dateentry, detail, username, entryfrom)
    sql.execute(insert, val)    
    db.commit()

def cekaplikasi(idaplikasi):    

    sql.execute("SELECT idaplikasi FROM aplikasi WHERE idaplikasi = '"+idaplikasi+"'")
    hasil_sql = sql.fetchall()

    hasil = int(sql.rowcount)

    return hasil

def cekrating(idtelegram,idaplikasi):
    idmahasiswa = getProfile(idtelegram)[0]
    sql.execute("SELECT rating FROM rating WHERE idmahasiswa = '"+str(idmahasiswa)+"' AND idaplikasi = '"+idaplikasi+"'")
    hasil_sql = sql.fetchall()
    hasil = int(sql.rowcount)
    return hasil

def inputratingdb(idtelegram,rating,idaplikasi):
    
    idmahasiswa = getProfile(idtelegram)[0]
    waktu = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    insert = 'INSERT INTO rating (rating, idaplikasi, idmahasiswa, waktu) VALUES (%s,%s,%s,%s)'
    val = (rating, idaplikasi, idmahasiswa, waktu)
    sql.execute(insert, val)
    print("Berhasil")
    db.commit()

def uploadposter(idtelegram,poster):
    kodekelompok = getProfile(idtelegram)[4]
    sql.execute("UPDATE aplikasi SET poster = '"+poster+"' WHERE kodekelompok = '"+kodekelompok+"'")
    db.commit()

def uploadpresentasi(idtelegram,presentasi):
    kodekelompok = getProfile(idtelegram)[4]
    sql.execute("UPDATE aplikasi SET presentasi = '"+presentasi+"' WHERE kodekelompok = '"+kodekelompok+"'")
    db.commit()

def uploadlaporan(idtelegram,laporan):
    kodekelompok = getProfile(idtelegram)[4]
    sql.execute("UPDATE aplikasi SET laporan = '"+laporan+"' WHERE kodekelompok = '"+kodekelompok+"'")
    db.commit()
