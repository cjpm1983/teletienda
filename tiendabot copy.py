import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teletienda.settings")
import django
django.setup()

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton, WebAppInfo
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from tienda_app.models import Tienda, Producto
# Este es el token del bot de Telegram, reemplázalo con tu propio token
TOKEN = "6605496580:AAFJ49gJa8XOJY9Ozl403eNzKGzTyJRDxY4"

URL = "282e-152-207-30-52.ngrok-free.app"

# El siguiente código es una plantilla básica para empezar, puedes personalizarlo según tus necesidades.



def start(update: Update, context: CallbackContext) -> None:
    options = []
    tiendas = Tienda.objects.all()  # Obtén todas las tiendas desde tu base de datos
    options = [tienda.nombre for tienda in tiendas]
    '''
    update.message.reply_text(
        "Selecciona una tienda:",
        reply_markup=ReplyKeyboardMarkup([options], one_time_keyboard=True)
        
    )
    '''
    kb = [
        [KeyboardButton("Show me Google!", web_app=WebAppInfo("https://28d2-152-207-30-52.ngrok-free.app/tienda/listar_producto/"))]
    ]
    update.message.reply_text("Let's do this...", reply_markup=ReplyKeyboardMarkup(kb))

def show_products(update: Update, context: CallbackContext) -> None:
    selected_tienda = update.message.text
    

    tienda = Tienda.objects.get(nombre=selected_tienda)  # Obtiene la tienda seleccionada desde tu base de datos
    
    productos = Producto.objects.filter(tienda=tienda)  # Obtiene los productos de la tienda
    
    for producto in productos:
        message = f"{producto.nombre}\n\n"
        message += f"Precio: {producto.precio}\n"
        message += f"Descripción: {producto.descripcion}\n\n"
        message += "Mostrar imagen: /mostrar_imagen_" + str(producto.id)
        
        update.message.reply_text(message)
     

def show_image(update: Update, context: CallbackContext) -> None:
    product_id = int(context.args[0])
    
    product = Producto.objects.get(id=product_id)  # Obtiene el producto seleccionado desde tu base de datos
    
    # Asegúrate de tener la URL correcta de la imagen del producto según tu modelo y configuración de almacenamiento
    image_url = product.foto.url
    
    update.message.reply_photo(image_url)


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^/mostrar_productos_'), show_products))
    dispatcher.add_handler(CommandHandler("mostrar_imagen", show_image))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

def show_image(update: Update, context: CallbackContext) -> None:
    """Envía al usuario un mensaje con la imagen del producto seleccionado."""
    # Obtiene el ID del producto desde el comando en el mensaje
    product_id = int(context.args[0])
    
    # Este es solo un ejemplo, asegúrate de tener la URL correcta de la imagen del producto
    image_url = f"http://{URL}/media/productos/{product_id}.jpg"
    
    # Envía la imagen al usuario
    update.message.reply_photo(image_url)

def main() -> None:
    """Función principal para ejecutar el bot de Telegram."""
    # Crea el objeto Updater con el token del bot
    updater = Updater(TOKEN)
    
    # Obtén el objeto de despachador para registrar los controladores de eventos
    dispatcher = updater.dispatcher
    
    # Agrega controladores de comandos y mensajes
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^/mostrar_productos_'), show_products))
    dispatcher.add_handler(CommandHandler("mostrar_imagen", show_image))
    
    # Inicia el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
