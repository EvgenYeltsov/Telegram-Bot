import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from app import my_app, Config, db
from app.models import trafo_list, users_list
from app.buttons import button_menu
from app.msg_send import EmailService


SERIAL_NUMBER_ID, NAME, EMAIL = range(3)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hi, {update.effective_user.username} !'
                                                                    f' 🚩 I am STV_Bot for quick searching info about transformers produced at the factory '
                                                                    f' Siemens STV.  Please tap 👉 /help to get info, and make your choice ', reply_markup=button_menu())


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'please use next command:\n'
                                                                    f'/help - some info \n'
                                                                    f'/search - for searching info in STV database\n'
                                                                    f'/authorization - receive access STV database\n'
                                                                    f'/registration - registration in STV_Bot\n', reply_markup=button_menu())


def sn_request_handler(update: Update, context: CallbackContext):
    """Search by serial number"""
    try:
        user_l =update.callback_query.from_user.id
    except AttributeError:
        user_l =update.message.from_user.id
    users = users_list.query.filter(users_list.user_telegram_id == user_l).first()
    if not users:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f" {update.effective_user.username} you have not access 🚫 to STV database\n"
                                  f" please type /registration first")
        return ConversationHandler.END
    elif users.user_name and users.user_name and users.permission_status == True and users.verifying_status == False:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Ok, you want check info about TR ')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Type the serial number please in format Y100XXX,'
                                                                        f' where is XXX numbers from 003-250:')
        return SERIAL_NUMBER_ID
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.effective_user.username} you have not access 🚫 to STV database\n"
                                  f" please type 🚧 /authorization first")
        return ConversationHandler.END


def search_number_sn(update: Update, context: CallbackContext):
    number = update.effective_message.text
    serial_number = trafo_list.query.filter(trafo_list.serial_number == number).first()

    if not serial_number:
        context.bot.send_message(chat_id=update.effective_chat.id, text='I cannot find any information for such serial number. Try again please or /cancel ')
        return SERIAL_NUMBER_ID

    found_sn = f"""Info page ⚡ <u>{number}</u> ▼:
     <b>⦁<u>Substation Name:</u></b>
     ➜{serial_number.name_substation}
     <b>⦁<u>Custormer Name:</u></b>
     ➜{serial_number.customer_name}
     <b>⦁<u>Country:</u></b>
     ➜{serial_number.country}
     <b>⦁<u>Transformer Type:</u></b>
     ➜{serial_number.transformer_type}
     <b>⦁<u>Asset Group:</u></b>
     ➜{serial_number.asset_group}
     <b>⦁<u>Manufacturing_year:</u></b>
     ➜{serial_number.manufacturing_year}
     <b>⦁<u>Brand:</u></b>
     ➜{serial_number.brand}
     <b>⦁<u>Insulation:</u></b>
     ➜{serial_number.insulation_type}
     <b>⦁<u>Type of oil:</u></b>
     ➜{serial_number.type_oil}
     <b>⦁<u>Cooling system:</u></b>
     ➜{serial_number.type_cooling_equipment}
     <b>⦁<u>Type of Tapchanger:</u></b>
     ➜{serial_number.type_tapchanger}
     <b>⦁<u>Rated voltage HV, kV:</u></b>
     ➜{serial_number.rated_voltage_hv}
     <b>⦁<u>Rated voltage MV, kV:</u></b>
     ➜{serial_number.rated_voltage_mv}
     <b>⦁<u>Rated voltage LV, kV:</u></b>
     ➜{serial_number.rated_voltage_lv}
     <b>⦁<u>Rated power, MVA:</u></b>
     ➜{serial_number.rated_voltage_lv}
     <b>⦁<u>Vector_group:</u></b>
     ➜{serial_number.vector_group}    
     <b>⦁<u>Type cooling :</u></b>
     ➜{serial_number.type_cooling }  
    """
    context.bot.send_message(chat_id=update.effective_chat.id, parse_mode="HTML", text=found_sn)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Something else? /search or /start', reply_markup=button_menu())

    return ConversationHandler.END


def registration_handler(update: Update, context: CallbackContext):
    """Registration new users"""
    users = users_list.query.filter(users_list.user_telegram_id == update.message.from_user.id).first()
    if not users:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Welcome {update.effective_user.username} to Registration form\n'
                                                                    f'Type your Name')
        return NAME
    else:
        update.message.reply_text(f"{update.effective_user.username} you have already create your account")
        if users.permission_status==True:
            update.message.reply_text(f"{update.effective_user.username} type /search or /start")
        if users.verifying_status==True:
            update.message.reply_text(f"{update.effective_user.username} authorization in process\n"
                                      f", you will receive message when your account will be approved")
        return ConversationHandler.END


def name_handler(update: Update, context: CallbackContext):
    if update.message.text:
        u = users_list(user_name=update.message.text, user_telegram_id=update.message.from_user.id)
        db.session.add(u)
        db.session.commit()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Type your name')
        return NAME
    context.bot.send_message(chat_id=update.effective_chat.id, text='Your email')
    return EMAIL


def email_handler(update: Update, context: CallbackContext):
    users = users_list.query.filter(users_list.user_telegram_id == update.message.from_user.id).first()
    email_validator = re.search(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',update.effective_message.text)
    if email_validator:
        users.user_email = update.effective_message.text.lower()
        db.session.commit()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Type correct email')
        return EMAIL

    context.bot.send_message(chat_id=update.effective_chat.id, text=f' Finishing,\n'
                                                                    f' Your name: {users.user_name} \n'
                                                                    f' Your email {users.user_email} \n')

    context.bot.send_message(chat_id=update.effective_chat.id, text=f'For access to STV_database please,\n'
                                                                    f' type /authorization')
    return ConversationHandler.END


def cancel_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Exit ?, type /start')
    return ConversationHandler.END


def update_permission_status(update: Update, context: CallbackContext):
    """Request for update permission status"""
    user_new = update.message.from_user.id
    users = users_list.query.filter(users_list.user_telegram_id == user_new).first()
    if not users:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Please type  /registration first ')
    elif users.permission_status == True and users.verifying_status == False:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.effective_user.username} you have already authorization\n"
                                  f" type /search")
    elif users.permission_status == True and users.verifying_status == True:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.effective_user.username}  authorization your account in process \n")

    elif users.permission_status == False and users.verifying_status == True:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.effective_user.username}  authorization your account in process \n")

    elif users.permission_status == False and users.permission_status == False:
        email = users.user_email
        body = f" Hi, {users.user_name} , {users.user_email}\n We got your request for access to STV database," \
               f" please wait e-mail confirmation or type /search for checking your status \n\n Regards Admin"
        body_to_admin = f"  {users.user_name} , {users.user_email}\n  send request for access to STV database"
        my_adr = "kanclerr@gmail.com"
        email_service = EmailService()
        try:
            email_service.send_email(my_adr, email, body) # email to user
            email_service.send_email(my_adr, my_adr, body_to_admin) # email to admin
            context.bot.send_message(chat_id=update.effective_chat.id, text="Message send. Please check your e-mail")
            users.verifying_status = True
            db.session.commit()
        except Exception:
            update.message.reply_text("ERROR, Try again")


def manage_text(update: Update, context: CallbackContext):
    msg = update.message.text.lower()

    if msg in ('hi', 'hello', 'hi bot', 'olla', 'holla'):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Hi, {update.effective_user.username} !'
                                    f' 🚩 I am STV_Bot for quick searching info about transformers produced at the factory '
                                    f' Siemens STV.  Please tap 👉 /help to get info, and make your choice ', reply_markup=button_menu())
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, I can't understand you.\n"
                                      "Press /help for more info.")


@my_app.route('/init-bot', methods=['GET', 'POST'])
def init_bot():

    updater = Updater(token=Config.TBOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

# Main bot commands:
    start_cmd = CommandHandler('start', start)
    help_cmd = CommandHandler('help', help)
    verifying_cmd = CommandHandler('authorization', update_permission_status)

# Handler for Registration

    conversation_handler = ConversationHandler(entry_points=[
        CommandHandler('registration', registration_handler)],
        states={
        NAME: [MessageHandler(Filters.text & (~Filters.command), name_handler, pass_user_data=True)],
        EMAIL: [MessageHandler(Filters.text & (~Filters.command), email_handler, pass_user_data=True)]},
        fallbacks=[CommandHandler('cancel', cancel_handler)])

# Handler for Search by serial number

    serial_number_handler = ConversationHandler(entry_points=[
        CommandHandler('search', sn_request_handler),
        CallbackQueryHandler(sn_request_handler, pattern='search'),
        ],
        states={
        SERIAL_NUMBER_ID: [
            MessageHandler(Filters.text & (~Filters.command), search_number_sn, pass_user_data=True)]},
        fallbacks=[CommandHandler('cancel', cancel_handler)])

    dispatcher.add_handler(CallbackQueryHandler(help, pattern='help'))
    dispatcher.add_handler(CallbackQueryHandler(cancel_handler, pattern='cancel'))

    dispatcher.add_handler(conversation_handler)
    dispatcher.add_handler(serial_number_handler)
    dispatcher.add_handler(start_cmd)
    dispatcher.add_handler(help_cmd)
    dispatcher.add_handler(verifying_cmd)

    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), manage_text))

    # Run bot
    updater.start_polling()

    return 'Bot started'
