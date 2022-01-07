from bs4 import BeautifulSoup
#import requests
#import schedule
import os
import random

import telegram
from telegram import message
from telegram.constants import PARSEMODE_MARKDOWN
from telegram.ext import Updater, dispatcher, CallbackContext, messagehandler
import logging #nos permite establecer la conexcion para inicar chat con algun usuario
from telegram import Update # la usamos para que el estado del chat se este actualizando y ver los nuevos mensajes
from telegram.ext import CommandHandler # este modulo nos permite manejar y realizar acciones con los comandos que el usuario ingrese
from telegram.ext import MessageHandler, Filters, MessageFilter
from telegram.files.file import File # distintos tipos de filtros para manejar los mensajes recibidos por los usuarios


# configurar Logging
logging.basicConfig(
    level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

telegram_token = "5041088112:AAEAwRHxdLJuvqM1SSj2ukFHnLb7nbqVOQM"
bot_chatID = '1310279131'


def start(update, context):
    print(update)
    logger.info(f"El usuario {update.message.chat['first_name']}, ha iniciado una conversacion")
    name = update.message.chat['first_name'] 
    update.message.reply_text(f"Hola {name} yo soy tu bot")

def random_number(update, context):
    user_id = update.message.chat['id']
    logger.info(f"El usuario {user_id} ha solicitado un numero aleatorio")
    number = random.randint(0,10)
    context.bot.sendMessage(chat_id = user_id, parse_mode = "HTML", text = f"<b>Número</b> aleatorio: \n{number}")



def Challenge_handler(update, context):
    user_id = update.message.chat['id']
    logger.info(f"\n El usuario {user_id} ha enviado evidencia del reto")
    evidence_file = MessageHandler(~Filters.text | Filters.video | Filters.audio | Filters.photo)

    context.bot.sendMessage(
        chat_id = user_id,
        parse_mode = "MarkdownV2",
        text = f"*Tu evidencia ha sido recibida* \n *_Genial Sigue adelante_*"
    )
    context.bot.sendMessage(
        chat_id = user_id,
        File = evidence_file
    )

class FilterAwesome(MessageFilter):
    def filter(self,message):
        return "/RETO" in message.text

filter_awesome = FilterAwesome()


def echo(update, context):
    user_id = update.message.chat['id']
    logger.info(f"\n El usuario {user_id} ha enviado un mensaje de texto")
    text = update.message.text
    context.bot.sendMessage(
        chat_id = user_id,
        parse_mode = "MarkdownV2",
        text = f"*Escribiste:* \n _{text}_"
    )


if __name__=='__main__':    # obtenemos informacion de nuestro bot
    my_bot = telegram.Bot(token = telegram_token)
    #print(my_bot.getMe())

# enlazamos nuestro updater con nuestro bot
updater = Updater(my_bot.token, use_context = True)

# cremos un despachador
dp = updater.dispatcher

# creamos los manjenadores
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("random", random_number))
dp.add_handler(CommandHandler("reto", Challenge_handler))  # el comando es "reto" y las instrucciones de lo que se hara al recibir el comando estan en la funncion "Challenge_handler"
dp.add_handler(MessageHandler(filter_awesome, Challenge_handler))
dp.add_handler(MessageHandler(Filters.text, echo))  # para filtrar y manejar los mensajes de texto, se puede usar otro filtro para manejar archivos.

updater.start_polling()
print("Bot Cargado")

updater.idle() # permite finaliar el bot con ctrl + c