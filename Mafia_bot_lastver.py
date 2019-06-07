#Use este comando na janela de comando do windows
#pip install python-telegram-bot --upgrade

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters, run_async
import logging
from random import shuffle
from time import sleep

def make_keyboardE(users, username):
    buttons = [[telegram.InlineKeyboardButton(text = i+' '+str(id_list[i][4]),callback_data=id_list[i][4]-1) for i in users if i != username]]
    reply = telegram.InlineKeyboardMarkup(inline_keyboard = buttons)
    return reply

def make_keyboardM(users, username):
    buttons = [[telegram.InlineKeyboardButton(text = i+' '+str(id_list[i][4]),callback_data=id_list[i][4]-1) for i in users if id_list[i][2] != "Mafioso"]]
    reply = telegram.InlineKeyboardMarkup(inline_keyboard = buttons)
    return reply
    

@run_async
def startG(i,users):
    player_list = []
    for name in users:
        player_list.append(name)
    classes = ["Detetive",  "Mafioso", "Médico", "Prefeito"]
    shuffle(classes)
    j=0
    ded = -1
    not_ded = -1
    votes = [0]*len(users)
    for username in users:
        j+=1
        print(j)
        classe = classes.pop()
        id_list[username][2]= classe
        id_list[username][4]= j
        bot.send_message(chat_id=id_list[username][0], text= "O jogo está para começar!")
        bot.send_message(chat_id=id_list[username][0], text= "Sua classe é " + classe + "!")
    while (True):
        for username in users:
            bot.send_message(chat_id=id_list[username][0], text= "A noite se aproxima.", disable_notification=True)
            if id_list[username][2] != "Mafioso" and id_list[username][2] != "Prefeito" and id_list[username][2] != "Cidadão":
                reply = make_keyboardE(users, username)
                bot.send_message(chat_id=id_list[username][0], text= "Escolha quem irá visitar.", reply_markup=reply)
            elif id_list[username][2] == "Mafioso":
                reply = make_keyboardM(users, username)
                bot.send_message(chat_id=id_list[username][0], text= "Vote no próximo alvo.", reply_markup=reply)
        wait = timer(i,15)
        ded = -1
        not_ded = -1
        for username in users:
            print(id_list)
            vote = id_list[username][3]
            if vote != -1:
                user_class = id_list[username][2]
                if user_class == "Mafioso":
                    ded = id_list[username][3]
                if user_class == "Médico":
                    not_ded = id_list[username][3]
                if user_class == "Detetive":
                    bot.send_message(chat_id=id_list[username][0], text= "Você descobriu a classe deste cidadão: "+ id_list[users[id_list[username][3]]][2], disable_notification=True)
                id_list[username][3] = -1
        print(ded,not_ded)
        if ded != not_ded and ded != -1:
            ded_name = player_list[ded]
            users.remove(player_list[ded])
            id_list[ded_name][1] = 0
            user_class = id_list[ded_name][2]
            bot.send_message(chat_id=id_list[ded_name][0], text= "Você foi morto durante a noite.", disable_notification=True)
            if len(users) == 1:
                if users[0][2] == "Mafioso":
                    v = "Mafiosos"
                    break
                else:
                    v = "Cidadões"
                    break
            
            for username in users:
                bot.send_message(chat_id=id_list[username][0], text= user_class + ' ' + ded_name + ' (' + str(ded+1) +")foi morto durante a noite.", disable_notification=True)
                bot.send_message(chat_id=id_list[username][0], text= "Um novo dia começa.", disable_notification=True)
        else:
            for username in users:
                bot.send_message(chat_id=id_list[username][0], text= "Ninguém foi morto durante a noite.", disable_notification=True)
                bot.send_message(chat_id=id_list[username][0], text= "Um novo dia começa.", disable_notification=True)

        wait = timer(i,30)
        for username in users:
            bot.send_message(chat_id=id_list[username][0], text= "A votação começa.", disable_notification=True)
            reply = make_keyboardE(users, username)
            bot.send_message(chat_id=id_list[username][0], text= 'Vote quem será executado!', reply_markup=reply)

        wait = timer(i,10)

        for username in users:
            print(id_list)
            vote = id_list[username][3]
            if vote != -1:
                if id_list[username][2] == 'Prefeito':
                    votes[vote]+=2
                else:
                    votes[vote] += 1
            id_list[username][3] = -1
        high = max(votes)
        ded = votes.index(high)
        try:
            votes.index(high, ded+1)
            for username in users:
                bot.send_message(chat_id=id_list[username][0], text= "A votação empatou. Ninguém foi executado.", disable_notification=True)
        except:
            ded_name = player_list[ded]
            users.remove(player_list[ded])
            id_list[ded_name][1] = 0
            user_class = id_list[ded_name][2]
            if user_class == "Mafioso":
                v = "Cidadões"
                break
            bot.send_message(chat_id=id_list[ded_name][0], text= "Você foi executado.", disable_notification=True)
            for username in users:
                bot.send_message(chat_id=id_list[username][0], text= user_class + ' ' + ded_name +' (' + str(ded+1) +")foi executado.", disable_notification=True)
        print(users)
        if len(users) == 1:
            if users[0][2] == "Mafioso":
                v = "Mafiosos"
                break
            else:
                v = "Cidadões"
                break
        for n in range(len(votes)):
            votes[n] = 0
    for username in users:
        id_list[username][1] = 0
        bot.send_message(chat_id=id_list[username][0], text= "O jogo acabou. Os " + v + " venceram", disable_notification=True)
    room_list['room_'+i] = []
    started[i]=False
        
def timer(i,t):
    while t > 0:
        t-=1
        if t == 30 or t == 15 or t in [1,2,3,4,5]:
            for username in room_list['room_'+str(i)]:
                bot.send_message(chat_id=id_list[username][0], text= "Faltam " + str(t) + " segundos.", disable_notification=True)
        sleep(1)
    return False

@run_async
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Bem vindo ao Mafia-Bot")

@run_async
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

@run_async
def register(bot, update):
    ID = update.message.chat_id
    user = update.message.from_user
    username = '@'+user['username']
    id_list[username] = [ID, 0, '', -1, 0]
    bot.send_message(chat_id=ID, text='Registrado com sucesso!\nSeu nome de usuário é: ' + username)

@run_async                     
def w(bot, update, args):
    user = update.message.from_user
    username = '@' + user['username']
    index = int(args[0]) - 1
    i = str(id_list[username][1])
    if i == 0:
        bot.send_message(chat_id=id_list[username][0], text= 'Você não está em uma sala!')
        return
    if index >= len(room_list['room_' + i]):
        bot.send_message(chat_id=id_list[username][0], text= 'Essa pessoa não existe!')
        return
    bot.send_message(chat_id=id_list[room_list['room_' + i][index]][0], text= username + str(id_list[username][4]) + ' sussurrou: ' + ' '.join(args[1:]))

@run_async
def talk(bot, update):
    user = update.message.from_user
    username = '@' + user['username']
    try:
        i = id_list[username][1]
    except:
        bot.send_message(chat_id=id_list[username][0], text= 'Use /register para se registrar primeiro!')
    if i == 0:
        bot.send_message(chat_id=id_list[username][0], text= 'Você não está em uma sala!')
        return
    for reciever_username in room_list['room_'+str(i)]:
        if reciever_username != username:
            bot.send_message(chat_id=id_list[reciever_username][0], text= username + str(id_list[username][4]) + ' falou: ' + update.message.text)

@run_async        
def uList(bot, update):
    ID = update.message.chat_id
    bot.send_message(chat_id=ID, text='\n'.join(id_list))

@run_async
def join(bot, update):
    ID = update.message.chat_id
    user = update.message.from_user
    username = '@' + user['username']
    try:
        if id_list[username][1] != 0:
            bot.send_message(chat_id=ID, text= 'Você já está em uma sala!')
            return
    except:
        bot.send_message(chat_id=ID, text= 'Use /register para se registrar primeiro!')
        return
    if len(room_list) == 0:
        room_list['room_1'] = [username]
        started.append(False)
        id_list[username][1] = 1
        bot.send_message(chat_id=ID, text= 'Você entrou na sala 1', disable_notification=True)
    else:
        i = 1
        find = False
        for room in room_list:
            if len(room_list[room]) < 2 and not started[i]:
                for reciever_username in room_list[room]:
                    bot.send_message(chat_id=id_list[reciever_username][0], text= username + ' entrou na sala ' + str(i))
                room_list[room].append(username)
                id_list[username][1] = i
                find = True
                bot.send_message(chat_id=ID, text= 'Você entrou na sala ' + str(i))
                if len(room_list[room]) == 2:
                    print(id_list)
                    startG(i,room_list[room])
                    started[i] = True
                break
            i+=1
        if not find:
            room_list['room_'+str(i)] = [username]
            started.append(False)
            id_list[username][1] = i
            bot.send_message(chat_id=ID, text= 'Você entrou na sala ' + str(i))

@run_async
def quit(bot, update):
    ID = update.message.chat_id
    user = update.message.from_user
    username = '@' + user['username']
    i = id_list[username][1]
    id_list[username][1] = 0
    room_list['room_'+str(i)].remove(username)
    bot.send_message(chat_id=ID, text= 'Você saiu da sala')

@run_async
def queryy(bot,update):
    query = update.callback_query
    username = '@' + query.message['chat']['username']
    bot.delete_message(query.message["chat"]["id"], query.message["message_id"])
    id_list[username][3] = int(query.data)
    if id_list[username][3] == '':
        id_list[username][3] = -1
    
#{username:[ID,room,class,vote,position]}
id_list = {}
room_list = {}
started = [0]
bot = telegram.Bot(token='708915796:AAGIF52GUer37NoPI7NJEl1_GyDyZwfFaGw')
updater = (Updater(token= '708915796:AAGIF52GUer37NoPI7NJEl1_GyDyZwfFaGw'))
dispatcher = updater.dispatcher
#votes = [[telegram.InlineKeyboardButton(text = 'teste', callback_data = '3'),telegram.InlineKeyboardButton(text = '2', callback_data = '5')]]

    
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
unknown_handler = MessageHandler(Filters.command, unknown)
register_handler = CommandHandler('register', register)
w_handler = CommandHandler('w', w, pass_args=True)
talk_handler = MessageHandler(Filters.text, talk)
uList_handler = CommandHandler('uList', uList)
join_handler = CommandHandler('join', join)
quit_handler = CommandHandler('quit', quit)

dispatcher.add_handler(CallbackQueryHandler(queryy))
dispatcher.add_handler(start_handler)
dispatcher.add_handler(register_handler)
dispatcher.add_handler(w_handler)
dispatcher.add_handler(talk_handler)
dispatcher.add_handler(uList_handler)
dispatcher.add_handler(join_handler)
dispatcher.add_handler(quit_handler)
dispatcher.add_handler(unknown_handler)




updater.start_polling()
