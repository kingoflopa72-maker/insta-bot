import os
import glob
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8749070023:AAHJnl1Vu96EHg2EueGfuFmBV--x7HgCHTw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل رابط ريلز إنستغرام لتحميله مباشرة.")

async def download_reels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    
    if "instagram.com" not in url:
        return

    msg = await update.message.reply_text("⏳ جاري التحميل، انتظر ثواني...")
    
    file_id = update.message.message_id
    out_tmpl = f"video_{file_id}.%(ext)s"
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': out_tmpl,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        files = glob.glob(f"video_{file_id}.*")
        if files:
            video_path = files[0]
            with open(video_path, 'rb') as video_file:
                await update.message.reply_video(video=video_file)
            
            os.remove(video_path)
            await msg.delete()
        else:
            await msg.edit_text("❌ تعذر العثور على الفيديو.")

    except Exception as e:
        await msg.edit_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_reels))
    app.run_polling()

if __name__ == "__main__":
    main()
