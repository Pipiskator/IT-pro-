from PIL import Image, ImageEnhance
import telebot
import os
import time


def add_watermark_imp(image, watermark): # создание водяного знака
    layer = Image.new('RGBA', image.size, (0,0,0,0)) #координаты  лого
    
    layer.paste(watermark, (0, 0)) #расположение
    return Image.composite(layer,  image,  layer)


def add_watermark(image_path, watermark_path):
    img = Image.open(image_path) 
    watermark = Image.open(watermark_path)
    
    length = watermark.size[0] 
    width = watermark.size[1] 
    
    watermark = watermark.resize((int(length / 16), int(width / 9)), Image.ANTIALIAS) #задаем размер логопо размеру
    result = add_watermark_imp(img, watermark)
    
    new_path = image_path + '_' + '.jpg' #даем новое имя готовому фото
    result.save(new_path) #сохраняем готовое фото
    return new_path

def clear_content(chat_id): #отчистка 
    try:
        for img in images[chat_id]:
            os.remove(img)
    except Exception as e:
        time.sleep(3)
        clear_content(chat_id)
    images[chat_id] = []

    
bot = telebot.TeleBot('5948733666:AAFYFs-OVn0E89KyW2IM0DLKSgfrNIaqdAs')
images = dict() #глобальный список


@bot.message_handler(commands = ['start'])
def start(message):
    bot.reply_to(message, "Приветствую, этот бот создан для добавления водяного знака на фото\n" + "Чтобы начать, напиши /go")

    
@bot.message_handler(content_types=['text']) #обоработка текста
def go(message):
    if message.text == '/go':
        bot.send_message(message.from_user.id, "Чтобы добавить водяной знак, отправьте два фото.\n" + "1) само изображение\n" + "2) водяной знак")
        bot.register_next_step_handler(message, handle_docs_photo)
    else:
        bot.send_message(message.from_user.id, 'Напиши /go')

        
@bot.message_handler(content_types=['photo']) #обоработка фота
def handle_docs_photo(message):
    print(message.photo[:-2])
    images[str(message.chat.id)] = [] #заполнение словаря
    try:
        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id) #id последней картинки
        downloaded_file = bot.download_file(file_info.file_path) 
        source = 'tmp/' + file_info.file_path 

        
        with open(source, 'wb') as new_file:
           new_file.write(downloaded_file)
        
        
        bot.reply_to(message,"Фото добавлено") #ответ на фотографии пользователю
        images[str(message.chat.id)].append(source)
    except Exception as error: 
        bot.reply_to(message, error ) #сообщение об ошибки

        
    time.sleep(3) #ждем 3 сек, ждем второе фото
    print('img: ', images)
    reply_img = ''    
    if (len(images[str(message.chat.id)]) == 2): #если бот увидел две фотографии
        reply_img = add_watermark(images[str(message.chat.id)][1], images[str(message.chat.id)][0]) #добавляем водяной знак
        images[str(message.chat.id)].append(reply_img) #отправка пользователю
        bot.send_photo(message.chat.id, open(reply_img, 'rb'))
        clear_content(str(message.chat.id))
    
    
bot.polling(none_stop=True, interval=0)   
