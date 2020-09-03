import os
import zipfile


def Backup():
    # Путь до файла
    way = input("ВВедите расположение файла:")

    # Куда копировать
    target = input("Куда копировать:")

    # Проверка пути
    if not (os.path.isdir(way) and os.path.isabs(way)):
        print(way, "Данная директория не существует!")
        return
    if not (os.path.isdir(target) and os.path.isabs(target)):
        print(target, "Данная директория не существует!")
        return

    # Названия и создания файла
    zip_name = input("Введите названия файла:") + ".zip"
    zip_way = os.path.join(target, zip_name)
    while True:
        if not (os.path.isfile(zip_way)):
            break
        else:
            zip_name = input("ВВедите другое названия") + "zip"
            zip_way = os.path.join(target, zip_name)

    zip_file = zipfile.ZipFile(zip_way, 'w')

    # запись файлов
    for folders, folders1, files in os.walk(way):
        for file in files:
            zip_file.write(os.path.join(folders, file))

    print("Готово")
Backup()