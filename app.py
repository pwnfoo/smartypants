import time
import json
import telegram
import logging
import ConfigParser
from utils.replyhandler import Cleverbot, CleverbotAPIError
from utils.profanity_check import ProfanityFilter
from telegram.chat import Chat
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

####################### INIT VARIABLES GO HERE  ##################################
cb = Cleverbot()
name = 'Guest'
database = dict()
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)
####################### END INIT VARIABLES ########################################

# Handle the initial start command.
def start(bot, update):
    username = str(update.message.from_user.first_name)
    bot.sendMessage(chat_id=update.message.chat_id, text="Hi, %s. I'm Smartypants. Talk to me." %(username))


# Handle replies.
def reply(bot, update):
    global cb
    profobj = ProfanityFilter()
    cleanmsg = profobj.check_message(update.message.text)

    if cleanmsg:
        logging.info("User %s just sweared!" %(update.message.from_user.first_name))
        bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id, text=cleanmsg)
    else:
        logging.info("%s : %s" %(update.message.from_user.first_name, update.message.text))
        bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        bot.sendMessage(chat_id=update.message.chat_id, text=cb.ask(update.message.text))

def parse_secret_token():
    config = ConfigParser.RawConfigParser()
    try:
        config.read('config.cfg')
        token = config.get('token', 'token').strip('\'')

        if token == 'Your_token_here':
            print "\n[!] Please set your bot token to proceed."
            return False
        else:
            return token
    except IOError as e:
        print "\n[!] Config File Missing!"


def main():
    try:
        updater = Updater(parse_secret_token())
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)
        echo_handler = MessageHandler(Filters.text, reply)
        dispatcher.add_handler(echo_handler)
        updater.start_polling()
        updater.idle()
    except KeyboardInterrupt:
        updater.stop()
        return False
'''
    msg_obj = MessageCounter()
    msg_count = msg_obj.get_messages(token)
    send_list = list()

    if msg_count:
        messagetext =  "\n\nMessage Statistics : \n~~~~~~~~~~~~~~~~~~"
        for username, count in msg_count.items():
            messagetext += "\n[*] %s has sent %i messages" %(msg_obj.namemap[username], count)
            messagetext += "\t -  Last message : %s" %(msg_obj.messagemap[username])

    for user,lastmessage in msg_obj.messagemap.items():
        if lastmessage == '/stats' and msg_obj.updatemap[user]:
            send_list.append(user)

        elif lastmessage == '/dota' and msg_obj.updatemap[user]:
            send_list.append(user)
            messagetext = "Too Easy fo;r Provin"

    send_list = set(send_list)
    for user in send_list:
        print msg_obj.idmap[user]
        send_obj = MessageSender(msg_obj.idmap[user])
        send_obj.SendMessage(token, messagetext)
'''

if __name__ == '__main__':
    print "[*] Running Server.."
    main()
