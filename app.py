import ConfigParser
from utils.getMe import GetBotDetails
from utils.getUpdates import MessageCounter
from utils.sendMessage import MessageSender


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
    token = parse_secret_token()

    bot = GetBotDetails()
    if bot.get_server_response(token) :
        print "Bot Name \t: %s" % bot.name
        print "Bot username \t: %s" % bot.username
        print "Bot id \t\t: %s" %bot.id

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
            messagetext = "Too Easy for Provin"

    send_list = set(send_list)
    for user in send_list:
        print msg_obj.idmap[user]
        send_obj = MessageSender(msg_obj.idmap[user])
        send_obj.SendMessage(token, messagetext)

if __name__ == '__main__':
    print "[*] Running Server.."
    while True:
        main()
