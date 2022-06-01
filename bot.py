from asyncore import dispatcher
from gc import callbacks
import logging
from pathlib import Path
from dbfunction import cekaplikasi, ceklogin, ceknim, cekrating, daftaruser, getAplikasi, getKodeKelompok, getNamaapk, getProfile, getRating, getpekan, inputpr, getProfile, inputratingdb, uploadlaporan, uploadposter, uploadpresentasi
from telegram import Bot, Document, ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Callback Data
NIM, INPUTPROGRESS, INPUTRATING, INPUTPOSTER, INPUTPRESENTASI, INPUTLAPORAN= range(6)

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    # /start
    id = str(update.effective_user.id)

    login = ceklogin(str(update.effective_user.id))

    #string
    namadepan = str(update.effective_user.first_name) 

    if login == 1:
        await update.message.reply_text(f'Halo {namadepan}\nSelamat datang di Konro BOT')
        await update.message.reply_text(f'Berikut ini kode untuk setor tugas :\n\n'
        '/myapp : Untuk melihat data aplikasi Anda\n\n'
        '/progress : Untuk setor progress report\n\n'
        '/rating : Untuk rating aplikasi\n\n '
        'Upload Dokumen :\n'
        '/poster : Untuk upload poster (Format: .png/.jpg/.jpeg. Size: 842 x 1191 pixels)\n'
        '/presentasi : Slide Presentasi (PDF)\n'
        '/laporan : Laporan Akhir (PDF)')
    else:
        await update.message.reply_text(f'Halo {namadepan}\nSelamat datang di Konro BOT')      
        await update.message.reply_text("💡 Karena Anda baru pertama kali menggunakan chatbot, silakan DAFTAR akun terlebih dahulu dengan cara ketik /daftar")

async def help(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:    

    login = ceklogin(str(update.effective_user.id))

    #string
    namadepan = str(update.effective_user.first_name) 

    if login == 1:
        await update.message.reply_text(f'Berikut ini kode untuk setor tugas :\n\n'
        '/myapp : Untuk melihat data aplikasi Anda\n\n'
        '/progress : Untuk setor progress report\n\n'
        '/rating : Untuk rating aplikasi\n\n '
        'Upload Dokumen :\n'
        '/poster : Untuk upload poster (Format: .png/.jpg/.jpeg. Size: 842 x 1191 pixels)\n'
        '/presentasi : Slide Presentasi (PDF)\n'
        '/laporan : Laporan Akhir (PDF)')
    else:        
        await update.message.reply_text("Maaf, akun telegram Anda belum terdaftar di sistem kami. Silahkan klik /daftar untuk melanjutkan.")

async def myapp(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:    
    idtelegram = str(update.effective_user.id)
    login = ceklogin(idtelegram)

    id        = str(getAplikasi(idtelegram)[0])
    nama      = str(getAplikasi(idtelegram)[1])
    deskripsi = str(getAplikasi(idtelegram)[2])
    rating    = str(getRating(id))

    if login == 1:
        
        await update.message.reply_text(f'Aplikasi Anda :\n\n'
        'ID Aplikasi : '+id+'\n'
        'Nama : '+nama+'\n'
        'Deskripsi : '+deskripsi+'\n'
        'Jumlah Rating : '+rating+'\n')
    else:
        await update.message.reply_text("Maaf, akun telegram Anda belum terdaftar di sistem kami. Silahkan klik /daftar untuk melanjutkan.")

async def daftar(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    login = ceklogin(str(update.effective_user.id))
    if login == 1:
        await update.message.reply_text("Akun Anda sudah terdaftar.")
    else:
        await update.message.reply_text(f'Masukkan NIM dan Email Anda dengan format : NIM\#Email\n\n'
        '_Contoh : 181080200000\#nama@gmail\.com_', parse_mode='MarkdownV2')
        return NIM

async def nim(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    
    data = str(update.message.text)
    format = '#'    

    if data.find(format) == -1:
        await update.message.reply_text("Format salah, silahkan ulangi lagi")
    else:
        value = data.split('#')
        nim = value[0]
        email = value[1]

    namadepan = str(update.effective_user.first_name)     

    if ceknim(nim,email) == 1:        
        idtelegram = str(update.effective_user.id)        
        daftaruser(idtelegram,nim)        
        logger.info(f'Data dari {namadepan} ditemukan dan berhasil terdaftar')        
        await update.message.reply_text("Selamat. Anda berhasil mendaftar. Klik /help untuk melanjutkan")
        return ConversationHandler.END
    else:
        await update.message.reply_text(f'Data tidak ditemukan, pastikan sudah memasukkan data dengan benar.')
        # logger.info(f'NIM {nim} dan Kode Kelompok {email} dari {namadepan} tidak ditemukan')                

async def progress(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)
    pekan = getpekan(idtelegram)
    
    if pekan <= 14:
        await update.message.reply_text(f'Silahkan masukkan progress apa saja yang kelompok Anda lakukan dalam pekan ke {pekan} :\n\n'
        'Klik /batal jika tidak jadi memasukkan progress.')
        return INPUTPROGRESS
    else:
        await update.message.reply_text(f'Anda sudah memasukkan semua progress report.')    

async def inputprogress(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:

    idtelegram = str(update.effective_user.id)
    data = str(update.message.text)
    pekan = getpekan(idtelegram)
    
    inputpr(idtelegram,data)
    
    await update.message.reply_text(f'Input progress pekan ke {pekan} berhasil')
    return ConversationHandler.END
            
async def rating(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)
        
    await update.message.reply_text(f'Silahkan masukkan rating (1-10) dengan format : rating#idaplikasi \n\n'
    'Contoh : 9#12345\n\n'
    'idaplikasi bisa Anda ambil dari website konro\n\n'
    'Klik /batal jika tidak jadi memasukkan progress.')

    return INPUTRATING    

async def inputrating(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)
    data = str(update.message.text)
    format = '#'    

    if data.find(format) == -1:
        await update.message.reply_text("Format salah, silahkan ulangi lagi")
    else:
        value = data.split('#')
        rating = int(value[0])
        idaplikasi = value[1]

        if (rating >= 1) and (rating <= 10):
            if cekaplikasi(idaplikasi) == 1:
                if cekrating(idtelegram,idaplikasi) == 0:
                    namaapk = getNamaapk(idaplikasi)
                    inputratingdb(idtelegram,rating,idaplikasi)
                    await update.message.reply_text(f'Input rating untuk aplikasi {namaapk} berhasil')
                    return ConversationHandler.END
                else:            
                    await update.message.reply_text("Anda sudah memberi rating aplikasi ini. Silahkan masukkan ulang dengan idaplikasi yang lain atau klik /batal untuk kembali ke menu awal.")                
            else:
                await update.message.reply_text("Aplikasi tidak ditemukan, pastikan memasukkan idaplikasi dengan benar")                
        else:
            await update.message.reply_text("Masukkan nilai rating 1-10")

async def poster(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)
        
    await update.message.reply_text(f'Silahkan upload poster dengan format .png/.jpg/.jpeg dan ukuran 842x1191 pixels \n\n'
    'Contoh : FilePoster.jpg\n\n'
    'Klik /batal jika tidak jadi memasukkan progress.')

    return INPUTPOSTER   

async def inputposter(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)    

    photo_file = await update.message.photo[-1].get_file()   
    extension = '.'+(photo_file.file_path).split(".")[-1]
    filename = (photo_file.file_path).split("/")[-1]
    kodekelompok = getKodeKelompok(idtelegram)
    folder = 'photos/poster'+'-'+kodekelompok+extension

    await photo_file.download(folder)
    uploadposter(idtelegram,folder)

    await update.message.reply_text(f'Poster telah berhasil disimpan')

    return ConversationHandler.END

async def presentasi(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)
        
    await update.message.reply_text(f'Silahkan upload file presentasi dengan format PDF\n\n'
    'Contoh : FilePresentasi.pdf\n\n'
    'Klik /batal jika tidak jadi memasukkan file.')

    return INPUTPRESENTASI   

async def inputpresentasi(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)    

    filepresentasi = await update.message.effective_attachment.get_file()
    
    extension = '.'+(filepresentasi.file_path).split(".")[-1]
    # filename = (filepresentasi.file_path).split("/")[-1]
    kodekelompok = getKodeKelompok(idtelegram)
    folder = 'file/presentasi-'+kodekelompok+extension
    
    if extension == '.pdf':
        await filepresentasi.download(folder)    
        uploadpresentasi(idtelegram,folder)
        await update.message.reply_text(f'File presentasi telah berhasil diperbarui')
        return ConversationHandler.END
    else:
        await update.message.reply_text(f'Format salah, pastikan file presentasi dalam format PDF')

async def laporan(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)
        
    await update.message.reply_text(f'Silahkan upload file laporan TAMK dengan format PDF\n\n'
    'Contoh : FileLaporan.pdf\n\n'
    'Klik /batal jika tidak jadi memasukkan file.')

    return INPUTLAPORAN

async def inputlaporan(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:
    idtelegram = str(update.effective_user.id)    

    filelaporan = await update.message.effective_attachment.get_file()
    
    extension = '.'+(filelaporan.file_path).split(".")[-1]
    # filename = (filelaporan.file_path).split("/")[-1]
    kodekelompok = getKodeKelompok(idtelegram)
    folder = 'file/laporan-'+kodekelompok+extension
    
    if extension == '.pdf':
        await filelaporan.download(folder)            
        uploadlaporan(idtelegram,folder)
        await update.message.reply_text(f'File laporan telah berhasil diperbarui')
        return ConversationHandler.END
    else:
        await update.message.reply_text(f'Format salah, pastikan file filelaporan dalam format PDF')

async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
    logging.info(update)
    nama = update.effective_user.first_name
    pesan = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Maaf, kode yang Anda kirim tidak terdeteksi di sistem kami.\n\nKetik /help untuk melihat kode dari sistem kami.")

async def batal(update: Update, context: CallbackContext.DEFAULT_TYPE) -> int:    
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Berhasil dibatalkan, klik /help untuk melihat kode setor tugas."
    )

    return ConversationHandler.END

if __name__ == '__main__':
    # Token Telegram    
    application = ApplicationBuilder().token("YOUR TOKEN HERE").read_timeout(7).get_updates_read_timeout(42).build()        
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.add_handler(CommandHandler('help', help))

    application.add_handler(CommandHandler('myapp', myapp))

    conv_daftar = ConversationHandler(
        entry_points=[CommandHandler("daftar", daftar)],
        states={
            NIM: [MessageHandler(filters.TEXT & ~filters.COMMAND, nim)],
        },
        fallbacks=[CommandHandler("batal", batal)],
    )
    application.add_handler(conv_daftar)

    conv_progress = ConversationHandler(
        entry_points=[CommandHandler("progress", progress)],
        states={
            INPUTPROGRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, inputprogress)],            
        },
        fallbacks=[CommandHandler("batal", batal)],
    )    
    application.add_handler(conv_progress)

    conv_rating = ConversationHandler(
        entry_points=[CommandHandler("rating", rating)],
        states={
            INPUTRATING: [MessageHandler(filters.TEXT & ~filters.COMMAND, inputrating)],            
        },
        fallbacks=[CommandHandler("batal", batal)],
    )    
    application.add_handler(conv_rating)

    conv_poster = ConversationHandler(
        entry_points=[CommandHandler("poster", poster)],
        states={
            INPUTPOSTER: [MessageHandler(filters.PHOTO & ~filters.COMMAND, inputposter)],            
        },
        fallbacks=[CommandHandler("batal", batal)],
    )    
    application.add_handler(conv_poster)

    conv_presentasi = ConversationHandler(
        entry_points=[CommandHandler("presentasi", presentasi)],
        states={
            INPUTPRESENTASI: [MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, inputpresentasi)],            
        },
        fallbacks=[CommandHandler("batal", batal)],
    )    
    application.add_handler(conv_presentasi)

    conv_laporan = ConversationHandler(
        entry_points=[CommandHandler("laporan", laporan)],
        states={
            INPUTLAPORAN: [MessageHandler(filters.ATTACHMENT & ~filters.COMMAND, inputlaporan)],            
        },
        fallbacks=[CommandHandler("batal", batal)],
    )    
    application.add_handler(conv_laporan)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)    
    

    application.run_polling()
