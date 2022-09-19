import os
from decimal import Underflow
import logging
from nis import cat

from telegram import __version__ as TG_VER
from qbittorrent import Client
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

if "TOKEN" in os.environ:
    token =  os.environ["TOKEN"]
    print(token)
else:
    raise ValueError("Por favor introduce un Token.")
user = "admin"
if "USER" in os.environ:
    user = os.environ["USER"]
password = "adminadmin"
if "PASSWORD" in os.environ:
    password = os.environ["PASSWORD"]
portq = "8080"
if "PORTQ" in os.environ:
    portq = os.environ["PORTQ"]

qb = Client("http://host.docker.internal:" + portq + "/")
qb.login(user, password)

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)




async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hola {user.mention_html()}! Enviame torrents para que los descargue automaticamente.",
        reply_markup=ForceReply(selective=True),
    )


async def downloadTorrent(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.document and ".torrent" in update.message.document.file_name:
        try:
            #print("Descargando torrent " + update.message.document.file_name)
            pathTorrent = "torrents/" + update.message.document.file_name
            torrent_file = await update.message.document.get_file()
            await torrent_file.download(pathTorrent)
            #print("Añadiendo torrent " + update.message.document.file_name + " a qBitorrent")
            qb.download_from_file(open(pathTorrent, "rb"))
            await update.message.reply_text("Torrent añadido correctamente")
        except Exception as e:
            print("Ha surgido un error descargando el archivo.")
            print(e)
            await update.message.reply_text("Ha surgido un error, por favor intentalo de nuevo mas tarde.")
    


def main() -> None:
    """Start the bot."""    
    
    application = Application.builder().token(token).build()

    
    application.add_handler(CommandHandler("help", help))

    
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, downloadTorrent))

    
    application.run_polling()


if __name__ == "__main__":
    main()