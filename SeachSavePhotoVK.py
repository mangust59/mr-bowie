import json
import requests
import urllib.request

print('Введите ID беседы')
chat = input()
print('Введите свой токен')
token = input()
next = None # Переменная в которую будем записывать ключ смещения

def searchurl():
    val = 1 # Переменная для счётчика
    global next
    Fin = open("input.txt","a") # Создаём файл для записи ссылок
    # Отправляем GET запрос на API и записываем ответ в response
    response = requests.get(f"https://api.vk.com/method/messages.getHistoryAttachments?peer_id={chat}&media_type=photo&start_from={next}&count=200&photo_size=1&preserve_order=1&max_forwards_level=44&v=5.103&access_token={token}")
    items = json.loads(response.text) # Считываем ответ от сервера в формате JSON
    if items['response']['items'] != []: # Проверка наличия данных в массиве
        for item in items['response']['items']: # Перебираем массив items
            link = item['attachment']['photo']['sizes'][-1]['url'] # Записываем самый последний элемент, так как он самого максимального расширения
            print(val,':',link) # Лог перебора фотографий
            val += 1 # Увеличиваем значение счётчика
            Fin.write(str(link)+"\n") # Записываем новую строку в файл
        next = items['response']['next_from'] # Записываем ключ для получения следующих фотографий
        print('dd',items['response']['next_from'])
        searchurl() # Вызываем функцию
    else: # В случае отсутствия данных
        print("Получили все фото")

def savephoto():
    f = open('input.txt') # Наш файл с ссылками

    val = 1 # Переменная для счётчика
    for line in f: # Перебираем файл построчно
        line = line.rstrip('\n')
        # Скачиваем изображение в папку "img"
        urllib.request.urlretrieve(line, f"img/{val}.jpg")
        print(val,':','файл скачан') # В логи выводим сообщение о загрузке
        val += 1 # Увеличиваем счётчик
    print("Готово")

searchurl()
savephoto()


    
