import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Fetch the service account key JSON file contents
cred = credentials.Certificate('Google Firebase JSON Key Directory')

# Initialize the Firebase app with the service account credentials
try:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'URL of Google Firebase Dataset'
    })
except ValueError:
    pass  # App is already initialized

# Define a reference to the inventory items node
inventory_ref = db.reference('inventory_items')

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text('Welcome to Ajay General Store! Here are our inventory items:\n Name - Price, Brand, Type, Weight, Remaining_Quantity')

    # Get the inventory items from the database
    inventory_items = inventory_ref.get()

    # Display the inventory items
    for item_key, item_value in inventory_items.items():
        item_info = f"{item_value['name']} - ₹ {item_value['price']}, {item_value['brand']}, {item_value['type']}, {item_value['weight']}, {item_value['remaining_quantity']} left"
        update.message.reply_text(item_info)

# Define a function to handle the /hi command
def hi(update, context):
    update.message.reply_text('Hello! Welcome to Ajay General Store. You can use the following commands:\n/start - View inventory items\n/hi - Say hi to the bot')


from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

# Define the states of the conversation
PRODUCT_NAME, QUANTITY, ADDRESS, CONFIRMATION = range(4)

# Define a function to start the conversation
def start(update, context):
    # Ask the user for the product name
    update.message.reply_text("Please enter the product name:")
    return PRODUCT_NAME

# Define a function to get the product name from the user
def get_product_name(update, context):
    # Store the product name in the context
    context.user_data['product_name'] = update.message.text
    
    # Ask the user for the quantity
    update.message.reply_text("Please enter the quantity:")
    return QUANTITY

# Define a function to get the quantity from the user
def get_quantity(update, context):
    # Store the quantity in the context
    context.user_data['quantity'] = update.message.text
    
    # Ask the user for the delivery address
    update.message.reply_text("Please enter the delivery address:")
    return ADDRESS

# Define a function to get the address from the user
def get_address(update, context):
    # Store the address in the context
    context.user_data['address'] = update.message.text
    
    # Get the inventory items from the database
    inventory_items = inventory_ref.get()
    
    # Check if the product exists in the inventory
    if context.user_data['product_name'] not in inventory_items:
        update.message.reply_text(f"Sorry, {context.user_data['product_name']} is not available in our inventory.")
        return ConversationHandler.END
    
    # Check if the requested quantity is available in the inventory
    if int(context.user_data['quantity']) > inventory_items[context.user_data['product_name']]['remaining_quantity']:
        update.message.reply_text(f"Sorry, we only have {inventory_items[context.user_data['product_name']]['remaining_quantity']} {context.user_data['product_name']} left in stock.")
        return ConversationHandler.END
    
    # Display the total cost of the order and ask for confirmation
    total_cost = float(inventory_items[context.user_data['product_name']]['price']) * int(context.user_data['quantity'])
    update.message.reply_text(f"The total cost of your order is ₹ {total_cost}. Do you want to confirm your order? Please type 'yes' to confirm.", reply_markup=ReplyKeyboardMarkup([['yes', 'no']], one_time_keyboard=True))
    
    return CONFIRMATION

# Define a function to confirm the order
def confirm_order(update, context):
    # Get the user's confirmation
    confirmation = update.message.text.lower()
    
    if confirmation == 'yes':
        # Place the order and send a confirmation message
        update.message.reply_text(f"Thank you for your order of {context.user_data['quantity']} {context.user_data['product_name']}. Your order will be delivered to {context.user_data['address']}.")
    else:
        # Cancel the order and send a message indicating that the order has been cancelled
        update.message.reply_text("Your order has been cancelled.")
    
    # End the conversation
    return ConversationHandler.END

# Define a function to cancel the conversation
def cancel(update, context):
    update.message.reply_text("Order cancelled.", reply_markup=ReplyKeyboardRemove())
    return Conversation

    

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
updater = Updater('6140839635:AAH_x9eoanvgFSWwlKFvMBiyRUQ672A7ZkE', use_context=True)


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


# Start the bot
updater.start_polling()
updater.idle()
