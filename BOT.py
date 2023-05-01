import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Fetch the service account key JSON file contents
cred = credentials.Certificate('Firebase databse json key path')

# Initialize the Firebase app with the service account credentials
try:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'Firebase database URL'
    })
except ValueError:
    pass  # App is already initialized

# Define a reference to the inventory items node
inventory_ref = db.reference('inventory_items')


def help_command(update, context):
    command_list = [
        "/start - View inventory items",
        "/hi - Say hi to the bot",
        "/order - Order a product",
        "/about - Learn about Ajay General Store",
        "/profilepic - Show bot profile picture",
        "/healthyfood - Show picture of healthy groceries",
        "/gl - Show picture of grocery list",
        "/veg - Show picture of vegetables list",
        "/help_command - Show list of available commands",
        "/besafe - A message from us to our customers"
    ]
    update.message.reply_text("Here are the available commands:\n" + "\n".join(command_list))


# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text('Welcome to Ajay General Store! Here are our inventory items:\nType /help_command to see all the commands\n\n\nBelow is the list of Items availabe for Delivery\n\n\n Name - Price, Brand, Type, Weight, Remaining_Quantity')

    # Get the inventory items from the database
    inventory_items = inventory_ref.get()

    # Display the inventory items
    for item_key, item_value in inventory_items.items():
        item_info = f"{item_value['name']} - ₹ {item_value['price']}, {item_value['brand']}, {item_value['type']}, {item_value['weight']}, {item_value['remaining_quantity']} left"
        update.message.reply_text(item_info)

# Define a function to handle the /hi command
def hi(update, context):
    update.message.reply_text('Hello! Welcome to Ajay General Store. You can use the following commands:\n/start - View inventory items\n/hi - Say hi to the bot')


orders_ref = db.reference('orders')

# Define a function to handle user orders
def order(update, context):
    # Ask the user for the product name, quantity, and address
    update.message.reply_text("Please enter your order details in the following format:\n\nProduct Name, Quantity, Address\n\nFor example, type:\n\nT-Shirt, 2, 123 Main St.")

    # Wait for the user's response and split it into the product name, quantity, and address
    order_details = context.bot.wait_for_message(chat_id=update.message.chat_id).text.split(",")
    product_name = order_details[0].strip()
    quantity = order_details[1].strip()
    address = order_details[2].strip()

    # Create a new order object and write it to the database
    new_order = {
        'product_name': product_name,
        'quantity': quantity,
        'address': address
    }
    order_id = orders_ref.push(new_order).key

    # Print a message indicating that the order has been accepted
    update.message.reply_text(f"Thank you for your order of {quantity} {product_name}. Your order will be delivered to {address}. Your order ID is {order_id}.")


# Define a function to handle the /about command
def about(update, context):
    update.message.reply_text('Welcome to Ajay General Store - your one-stop-shop for all your daily needs! Our store is committed to providing our customers with high-quality products at affordable prices, making everyday shopping convenient and hassle-free.We take pride in our wide range of products, carefully selected from the best brands to ensure that we have something for everyone. From groceries to household essentials, from health and beauty products to electronics, weve got it allOur team of knowledgeable and friendly staff is always available to help you find what you need and answer any questions you may have.At Ajay General Store, we believe that shopping should be a fun and enjoyable experience, and thats why were constantly updating our inventory to keep up with the latest trends and meet our customers needs. We are committed to providing you with exceptional customer service, and were always looking for new ways to improve your shopping experience.So come visit us today, and discover the best shopping experience you have ever had. We cant wait to see you!')




# Define a function to handle the /profilepic command
def profilepic(update, context):
    # Send the profile picture as a photo
    chat_id = update.message.chat_id
    photo_url = 'https://images.app.goo.gl/feGQ7HicAmS21jDJ8'  # Replace with your profile picture URL
    context.bot.send_photo(chat_id=chat_id, photo=photo_url)


#healthy grocery pic
def healthyfood(update, context):
    # Send the profile picture as a photo
    chat_id = update.message.chat_id
    photo_url = 'https://images.app.goo.gl/ZbhrU1LgyfNBHAQm6'
    context.bot.send_photo(chat_id=chat_id, photo=photo_url)

#grocerylist
def gl(update, context):
    # Send the profile picture as a photo
    chat_id = update.message.chat_id
    photo_url = 'https://images.app.goo.gl/1U7wyiSr2fKYKPzMA'
    context.bot.send_photo(chat_id=chat_id, photo=photo_url)


#vegetableslist
def veg(update, context):
    # Send the profile picture as a photo
    chat_id = update.message.chat_id
    photo_url = 'https://images.app.goo.gl/wx4t8xdJEzWAyJjT7'
    context.bot.send_photo(chat_id=chat_id, photo=photo_url)




#msg
def besafe(update, context):
    # Send the profile picture as a photo
    chat_id = update.message.chat_id
    photo_url = 'https://images.app.goo.gl/Rqb6etESKHLS4MCw9'
    message = """Dear customers,
Your health and safety are our top priorities. As we navigate through these challenging times, we kindly ask you to take necessary precautions when visiting our store. Please:
- Wear a mask
- Maintain social distancing
- Sanitize your hands before entering.

We want to assure you that we are doing everything we can to keep our store clean and safe. Our staff is regularly sanitizing high-touch surfaces and wearing masks to protect themselves and our customers. We are also limiting the number of people allowed in the store at one time to maintain social distancing.

We appreciate your cooperation and understanding during these uncertain times. Let's work together to keep ourselves and our community healthy. Thank you for your continued support."""

    context.bot.send_photo(chat_id=chat_id, photo=photo_url, caption=message, parse_mode='Markdown')




# Create a Telegram bot using the bot token provided by BotFather
updater = Updater('Telegram BOT api key', use_context=True)


# Set up CommandHandlers to handle the /start, /hi, /about, and /order commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hi', hi))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('order', order))
updater.dispatcher.add_handler(CommandHandler('profilepic', profilepic))
updater.dispatcher.add_handler(CommandHandler('healthyfood', healthyfood))
updater.dispatcher.add_handler(CommandHandler('gl', gl))
updater.dispatcher.add_handler(CommandHandler('veg', veg))
updater.dispatcher.add_handler(CommandHandler('besafe', besafe))
updater.dispatcher.add_handler(CommandHandler('help_command', help_command))




# Start the bot
updater.start_polling()
updater.idle()
