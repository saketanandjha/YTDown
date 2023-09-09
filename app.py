from telegram.constants import ParseMode
import os
from telegram import Update
#from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters
#from telegram import ParseMode

from pytube import YouTube

# Define conversation states (if needed)
START, DOWNLOAD = range(2)

# Define a function to start the bot
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Send me a YouTube video URL, and I'll download it for you.")
    return DOWNLOAD

# Define a function to handle video download
def download(update: Update, context: CallbackContext) -> int:
    url = update.message.text
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_stream.download()
        update.message.reply_text("Video downloaded successfully!")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {str(e)}")
    
    return ConversationHandler.END

# Define the main function
def main():
    updater = Updater(token="6085430116:AAFR6IlwVJFQmMe0iEbFGELg9ICDRnzKlOc", use_context=True)
    dp = updater.dispatcher

    # Define conversation handler (if needed)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            DOWNLOAD: [MessageHandler(Filters.text & ~Filters.command, download)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

