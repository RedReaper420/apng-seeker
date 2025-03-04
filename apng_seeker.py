# Код определения APNG:
# https://stackoverflow.com/a/62367135
# Код поиска файлов с нужным расширением:
# https://stackoverflow.com/a/3964691
# Код прогрессбара:
# https://stackoverflow.com/a/34482761
# Код для склонения слова "секунда":
# https://ru.stackoverflow.com/a/1106147
# Код мигания окна на панели задач:
# https://stackoverflow.com/a/42182714

import os
import sys
import time
import ctypes

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        percent = j / count * 100
        file.write("%s[%s%s] %i/%i (%.2f%%)\r" % (prefix, "█"*x, "."*(size-x), j, count, percent))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

def is_apng(a: bytes):
    acTL = a.find(b"\x61\x63\x54\x4C")
    if acTL > 0: # find returns -1 if it cant find anything
        iDAT = a.find(b"\x49\x44\x41\x54")
        if acTL < iDAT:
            return True
    return False

def check_path(path: str):
    if os.path.exists(path):
        if os.path.isdir(path):
            print("Директория подтверждена.\n")
            return True
        else:
            print("Объект не является директорией.")
    else:
        print("Неверный путь.")
    return False

def conv(n): 
    es = ['у', 'ы', '']
    n = n % 100
    if n>=11 and n<=19:
        s=es[2] 
    else:
        i = n % 10
        if i == 1:
            s = es[0] 
        elif i in [2,3,4]:
            s = es[1] 
        else:
            s = es[2] 
    return s

print("Введите директорию для сканирования.")
print("Для текущей директории оставьте поле пустым.")
print("Для отмены поиска введите значение -1.\n")
path = ""
while path == "":
    path = input("Путь:\n")
    if path == "":
        path = os.getcwd()
    elif path != "-1":
        if check_path(path) == False:
            path = ""

if path != "-1":
    print("Текущая директория:\n" + path)

    time_start = time.time()
    print("\n[{}] Проводится поиск PNG-файлов...".format(time.ctime(time_start)))

    png_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".png") or file.endswith(".apng"):
                png_list.append(os.path.join(root, file))
    png_num = len(png_list)

    time_end = time.time()
    time_elapsed = round(time_end - time_start)
    print("[{}] Операция завершена за {} секунд{}.".format(time.ctime(time_end), time_elapsed, conv(time_elapsed)))
    print("Всего найдено PNG: " + str(png_num))
    
    if png_num > 0:
        time_start = time.time()
        print("\n[{}] Проводится анализ PNG-файлов...".format(time.ctime(time_start)))

        apng_list = []
        for png in progressbar(range(png_num), "Анализ файлов: ", 40):
            f = open(png_list[png], "rb")
            file = f.read()
            if is_apng(file):
                apng_list.append(png_list[png])
            f.close()
        apng_num = len(apng_list)

        time_end = time.time()
        time_elapsed = round(time_end - time_start)
        print("[{}] Операция завершена за {} секунд{}.".format(time.ctime(time_end), time_elapsed, conv(time_elapsed)))
        print("Всего найдено APNG: " + str(apng_num))
        if apng_num > 0:
            print("\nНайденные APNG:")
            for apng in apng_list:
                print(apng)

    ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)
    input("\nДля завершения работы нажмите Enter.")
else:
    print("Поиск отменён. Завершаю работу.")
    time.sleep(3)
