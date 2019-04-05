#Use este comando na janela de comando do windows
#pip install python-telegram-bot --upgrade

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
import logging
from random import shuffle
from time import sleep

@run_async
def start(i):
    classes = ["Detetive", "Vidente", "Mafioso", "Médico", "Prefeito"]
    shuffle(classes)
    for username in room_list['room_'+str(i)]:
        classe = classes.pop()
        id_list[username][2]= classe
        bot.send_message(chat_id=id_list[username][0], text= "O jogo está para começar!")
        bot.send_message(chat_id=id_list[username][0], text= "Sua classe é " + classe + "!")

@run_async    
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

@run_async
def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

@run_async
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

@run_async
def register(bot, update):
    ID = update.message.chat_id
    user = update.message.from_user
    username = '@'+user['username']
    id_list[username] = [ID, 0, '']
    bot.send_message(chat_id=ID, text='Registrado com sucesso!\nSeu nome de usuário é: ' + username)

@run_async                     
def whisper(bot, update, args):
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
    bot.send_message(chat_id=id_list[room_list['room_' + i][index]][0], text= username + ' sussurrou ' + ' '.join(args[1:]))

@run_async
def talk(bot, update, args):
    user = update.message.from_user
    username = '@' + user['username']
    i = id_list[username][1]
    if i == 0:
        bot.send_message(chat_id=id_list[username][0], text= 'Você não está em uma sala!')
        return
    for reciever_username in room_list['room_'+str(i)]:
        if reciever_username != username:
            bot.send_message(chat_id=id_list[reciever_username][0], text= username + ' falou ' + ' '.join(args[:]))

@run_async        
def uList(bot, update):
    ID = update.message.chat_id
    bot.send_message(chat_id=ID, text='\n'.join(id_list))

@run_async
def join(bot, update):
    ID = update.message.chat_id
    user = update.message.from_user
    username = '@' + user['username']
    if id_list[username][1] != 0:
        bot.send_message(chat_id=ID, text= 'Você já está em uma sala!')
        return
    if len(room_list) == 0:
        room_list['room_1'] = [username]
        id_list[username][1] = 1
        bot.send_message(chat_id=ID, text= 'Você entrou na sala 1')
    else:
        i = 1
        find = False
        for room in room_list:
            if len(room_list[room]) < 2:
                room_list[room].append(username)
                id_list[username][1] = i
                find = True
                bot.send_message(chat_id=ID, text= 'Você entrou na sala ' + str(i))
                if len(room_list[room]) == 2:
                    start(i)
                break
            i+=1
        if not find:
            room_list['room_'+str(i)] = [username]
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
id_list = {}
room_list = {}
bot = telegram.Bot(token='708915796:AAGIF52GUer37NoPI7NJEl1_GyDyZwfFaGw')
updater = (Updater(token= '708915796:AAGIF52GUer37NoPI7NJEl1_GyDyZwfFaGw'))
dispatcher = updater.dispatcher
    
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text, echo)
caps_handler = CommandHandler('caps', caps, pass_args=True)
unknown_handler = MessageHandler(Filters.command, unknown)
register_handler = CommandHandler('register', register)
whisper_handler = CommandHandler('w', whisper, pass_args=True)
talk_handler = CommandHandler('talk', talk, pass_args=True)
uList_handler = CommandHandler('uList', uList)
join_handler = CommandHandler('join', join)
quit_handler = CommandHandler('quit', quit)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(register_handler)
dispatcher.add_handler(whisper_handler)
dispatcher.add_handler(talk_handler)
dispatcher.add_handler(uList_handler)
dispatcher.add_handler(join_handler)
dispatcher.add_handler(quit_handler)
dispatcher.add_handler(unknown_handler)




updater.start_polling()






