from PIL import Image #Это надо

filename = "full-hd.jpg"
with Image.open(filename) as img: #Загрузка фото
    img.load()

logof = "logotip_media_tsentr.png" # Загрузка Лого Два способа загрузки
logo = Image.open(logof)

print(type(img)) # Тип изображения
print(type(logo)) # Тип изображения
print(isinstance(img, Image.Image)) #Совпадают типы? Понятия не имею зачем это

widht, height=img.size

a=img.size[0]
b=img.size[1]

s1=a/4
s2=b/3

size = (s1, s2) #Уменьшение размера лого
crop_image = logo.resize((int(512),int(256)))
# crop_image.resize(size)

a1=crop_image.size[0]
b1=crop_image.size[1]

a=a-a1
b=b-b1


print(img.size)# Вывод размеров фото
print(logo.size)
print(crop_image.size)


print(a,b)

img.paste(crop_image, (a, b), crop_image)# Вставвит лого в фото, расположение, второй раз для прозрачности (Не знаю почему так надо)


img.show() # показать готовое фото
# logo.show()

