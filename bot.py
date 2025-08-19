from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "tokkenni kiriting"
ADMIN_ID = 309227759   # bu yerga o'z Telegram ID raqamingizni yozing

# Bosqichlar
I_FO, YASHASH_JOYI, TUGILGAN, TEL, MUROJAAT = range(5)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Keling, murojaatingizni yozib olamiz.\n\n1️⃣ Iltimos, I.F.O (to‘liq ism sharifingizni) yozing:")
    return I_FO

async def i_fo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["I_FO"] = update.message.text
    await update.message.reply_text("2️⃣ Yashash joyingizni yozing (tuman, MFY):")
    return YASHASH_JOYI

async def yashash_joyi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["YASHASH_JOYI"] = update.message.text
    await update.message.reply_text("3️⃣ Tug‘ilgan yil, oy, kuningizni yozing:")
    return TUGILGAN

async def tugilgan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["TUGILGAN"] = update.message.text
    await update.message.reply_text("4️⃣ Telefon raqamingizni yozing:")
    return TEL

async def tel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["TEL"] = update.message.text
    await update.message.reply_text("5️⃣ Murojaatingizning qisqacha mazmunini yozing:")
    return MUROJAAT

async def murojaat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["MUROJAAT"] = update.message.text

    # Hamma ma'lumotni yig‘amiz
    text = (
        "✅ Yangi murojaat qabul qilindi!\n\n"
        f"👤 I.F.O: {context.user_data['I_FO']}\n"
        f"🏠 Yashash joyi: {context.user_data['YASHASH_JOYI']}\n"
        f"🎂 Tug‘ilgan sana: {context.user_data['TUGILGAN']}\n"
        f"📞 Telefon: {context.user_data['TEL']}\n"
        f"📝 Murojaat: {context.user_data['MUROJAAT']}"
    )

    # Foydalanuvchiga javob
    await update.message.reply_text("✅ Murojaatingiz qabul qilindi. Rahmat!", reply_markup=ReplyKeyboardRemove())

    # Admin (sizga) yuborish
    await context.bot.send_message(chat_id=ADMIN_ID, text=text)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Murojaat bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = Application.builder().token("8337402008:AAGHF-MLbEH-ZHOqXMEA0smXfcmTk5tvbiE").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            I_FO: [MessageHandler(filters.TEXT & ~filters.COMMAND, i_fo)],
            YASHASH_JOYI: [MessageHandler(filters.TEXT & ~filters.COMMAND, yashash_joyi)],
            TUGILGAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, tugilgan)],
            TEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, tel)],
            MUROJAAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, murojaat)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()

