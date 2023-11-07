import os
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teletienda.settings")
import django
django.setup()

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ContextTypes,
    Application,
)

from asgiref.sync import sync_to_async
import asyncio

from tienda_app.models import Tienda, Producto

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(0)
logger = logging.getLogger(__name__)


# Este es el token del bot de Telegram, reemplázalo con tu propio token
TOKEN = "6605496580:AAFJ49gJa8XOJY9Ozl403eNzKGzTyJRDxY4"
URL = "https://ce2a-152-206-235-164.ngrok-free.app"

'''
async def start(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    options = []
    tiendas = await sync_to_async(list)(Tienda.objects.all())  # Obtén todas las tiendas desde tu base de datos
    
    options = [tienda.nombre for tienda in tiendas]
    
    await update.message.reply_text(
        "Selecciona una tienda:",
        reply_markup=ReplyKeyboardMarkup([options], one_time_keyboard=True)
        
    )'''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    options = []
    tiendas = await sync_to_async(list)(Tienda.objects.all())  # Obtén todas las tiendas desde tu base de datos
    options = [tienda.nombre for tienda in tiendas]
    
    # Crea una lista de botones en línea para cada tienda
    buttons = [InlineKeyboardButton(tienda, callback_data="shop_"+tienda) for tienda in options]
    
    # Divide los botones en filas
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    
    # Crea el objeto InlineKeyboardMarkup con los botones en línea
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Selecciona una tienda:",
        reply_markup=reply_markup
    )
'''
async def show_products(selected_tienda, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #selected_tienda = update.message.text
    tienda = await sync_to_async(Tienda.objects.get)(nombre=selected_tienda)  # Obtiene la tienda seleccionada desde tu base de datos
    productos = await sync_to_async(Producto.objects.filter)(tienda=tienda)  # Obtiene los productos de la tienda


    options = [producto.nombreProducto for producto in productos]
    
    # Crea una lista de botones en línea para cada producto
    buttons = [InlineKeyboardButton(producto, callback_data="shop_"+producto) for producto in options]
    
    # Divide los botones en filas
    keyboard = buttons #[buttons[i:i+2] for i in range(0, len(buttons), 2)]
    
    # Crea el objeto InlineKeyboardMarkup con los botones en línea
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Selecciona una producto:",
        reply_markup=reply_markup
    )
'''

'''
    async for producto in productos:

        keyboard = [
                      [InlineKeyboardButton("concentrado de Tomate Precio: 130.00 \n Descripción: Concentrado de Tomate de la mini Industria la Almendra Sancti Spiritus", web_app=WebAppInfo(f"{URL}/tienda/detalle_producto/{producto.id}/"))]  
                    ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = f"{producto.nombreProducto}\n\n"
        message += f"Precio: {producto.precio}\n"
        message += f"Descripción: {producto.descripcion}\n\n"
        message = "-"
        #message += "Mostrar imagen: /mostrar_imagen_" + str(producto.id)
        await update.callback_query.message.reply_text(message, reply_markup=reply_markup)
'''




async def show_products(selected_tienda, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #selected_tienda = update.message.text
    tienda = await sync_to_async(Tienda.objects.get)(nombre=selected_tienda)  # Obtiene la tienda seleccionada desde tu base de datos
    productos = await sync_to_async(Producto.objects.filter)(tienda=tienda)  # Obtiene los productos de la tienda

    async for producto in productos:
        
        '''
        [

            InlineKeyboardButton("Detalles en Navegador externo", url="https://dac9-152-207-30-52.ngrok-free.app/tienda/detalle_producto/2/"),
            InlineKeyboardButton("Detalles en mensaje de Telegram", callback_data="2"),

        ],
             '''
        keyboard = [
                      [InlineKeyboardButton("concentrado de Tomate Precio: 130.00 \n Descripción: Concentrado de Tomate de la mini Industria la Almendra Sancti Spiritus", web_app=WebAppInfo(f"{URL}/tienda/detalle_producto/{producto.id}/"))]  
                    ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = f"{producto.nombreProducto}\n\n"
        message += f"Precio: {producto.precio}\n"
        message += f"Descripción: {producto.descripcion}\n\n"
        message = "-"
        #message += "Mostrar imagen: /mostrar_imagen_" + str(producto.id)
        await update.callback_query.message.reply_text(message,reply_markup=reply_markup)

    
async def show_image(update: Update, context:ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        # Si hay argumentos, accede al primer elemento
        greeting = "Hola " #+ context.args[0]
        await update.message.reply_text(greeting)
    else:
        # Si no hay argumentos, envía un mensaje de error o un mensaje predeterminado
        await update.message.reply_text("No se proporcionó ningún nombre.")

    product_id = int(context.args[0])
    
    product = Producto.objects.get(id=product_id)  # Obtiene el producto seleccionado desde tu base de datos
    
    # Asegúrate de tener la URL correcta de la imagen del producto según tu modelo y configuración de almacenamiento
    image_url = product.foto.url
    
    
    #await update.message.reply_text(image_url)
    #await update.message.reply_photo(image_url)

async def show_imagen(update: Update, product_id) -> None:
    
    product = await sync_to_async(Producto.objects.get)(id=product_id)  # Obtiene el producto seleccionado desde tu base de datos
    
    # Asegúrate de tener la URL correcta de la imagen del producto según tu modelo y configuración de almacenamiento
    image_url = product.foto.url
    
    
    #await update.callback_query.reply_text(image_url)
    await update.callback_query.reply_photo(image_url)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    
    cbdata = query.data
    if cbdata.startswith("shop_"):
        # Acción para el caso de que la cbdata comience con "shop_"
        tienda = cbdata[len("shop_"):]
        #await query.message.reply_text(text=f"******* MOSTRANDO PRODUCTOS EN: <b>{tienda}</b> *******", parse_mode='HTML')
        await query.message.reply_text(text=f"****************************\n****************************\n MOSTRANDO PRODUCTOS EN: <b>{tienda}</b> \n****************************\n****************************\n", parse_mode='HTML')
        await show_products(tienda,update,context)
        # Código adicional para esta acción
    elif cbdata.startswith("prod_"):
        # Acción para el caso de que la cbdata comience con "prod_"
        producto = cbdata[len("prod_"):]
        await query.message.reply_text(text=f"Selected option: {producto}")
        # Código adicional para esta acción
    else:
        # Acción por defecto si no se cumple ninguna de las condiciones anteriores
        await query.message.reply_text(text=f"No hay accion asignada Selected option: {query.data}")


    #await query.edit_message_text(text=f"Selected option: {query.data}")
    #await query.message.reply_text(text=f"Selected option: {query.data}")
    #await show_imagen(update,query.data)

    #product = await sync_to_async(Producto.objects.get)(id=int(query.data))  # Obtiene el producto seleccionado desde tu base de datos
    
    
    #image_url = "https://dac9-152-207-30-52.ngrok-free.app/media/productos/in2.jpeg"
    
    # Obtén el objeto bot de la instancia de Dispatcher
    #bot = context.bot
    
    # Envía la foto utilizando el método send_photo()
    #await bot.send_photo(chat_id=query.message.chat_id, photo=image_url)
    #await update.callback_query.reply_text(image_url)
    #await update.callback_query.send_photo(image_url)

def main() -> None:

    """Start the bot."""
    # Create the Application and pass it your bot's token.

    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    #application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.Regex(r'^/mostrar_productos_'), show_products))
    application.add_handler(MessageHandler(filters.Regex(r'^/mostrar_imagen_'), show_image))
    application.add_handler(MessageHandler(filters.Regex(r'^Demo'), show_products))


    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C

    application.run_polling(allowed_updates=Update.ALL_TYPES)

 
if __name__ == '__main__':
    main()

