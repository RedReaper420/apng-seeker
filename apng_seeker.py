import os
import sys
import time
import ctypes
import argparse

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
            print(strings["dir_confirned"][lang])
            return True
        else:
            print(strings["not_a_dir"][lang])
    else:
        print(strings["wrong_path"][lang])
    return False

def conv(n, lang):
    if lang == 0:
        es = ['s', '']
        
        if n == 1:
            s = es[1]
        else:
            s = es[0]
    
    elif lang == 1:
        es = ['у', 'ы', '']
        n = n % 100
        
        if n >= 11 and n <= 19:
            s = es[2] 
        else:
            i = n % 10
            
            if i == 1:
                s = es[0] 
            elif i in [2,3,4]:
                s = es[1] 
            else:
                s = es[2]
        
    return s

parser = argparse.ArgumentParser(description="Search of APNGs in directories.")
parser.add_argument("-r", "--ru", action="store_true", help="Set the language to Russian (Русский).")

lang = int((parser.parse_args().ru) == True)
strings = {
"dir_confirned": ["Directory confirmed.\n", "Директория подтверждена.\n"],
"not_a_dir": ["This object is not a directory.\n", "Объект не является директорией.\n"],
"wrong_path": ["Wrong path.\n", "Неверный путь.\n"],
"start_1": ["Enter the directory for scanning.", "Введите директорию для сканирования."],
"start_2": ["For the current directory, enter nothing.", "Для текущей директории введите пустое значение."],
"start_3": ["For cancelling the search, enter -1 value.\n", "Для отмены поиска введите значение -1.\n"],
"path": ["Path:\n", "Путь:\n"],
"current_dir": ["Current directory:\n", "Текущая директория:\n"],
"searching": ["\n[{}] Searching for PNG-files...", "\n[{}] Проводится поиск PNG-файлов..."],
"finished_in": ["[{}] Operation finished in {} second{}.", "[{}] Операция завершена за {} секунд{}."],
"found_pngs_num": ["Total number of PNGs found: ", "Всего найдено PNG: "],
"pngs_analysis": ["\n[{}] Analyzing PNG files...", "\n[{}] Проводится анализ PNG-файлов..."],
"files_analysis": ["Files analysis: ", "Анализ файлов: "],
"found_apngs_num": ["Total number of APNGs found: ", "Всего найдено APNG: "],
"found_apngs_list": ["\nFounds APNGs:", "\nНайденные APNG:"],
"finished": ["\nPress enter to exit.", "\nДля завершения работы нажмите Enter."],
"cancelled": ["\nThe search is cancelled. Shutting down...", "\nПоиск отменён. Завершаю работу..."]
}

# Path input
print(strings["start_1"][lang])
print(strings["start_2"][lang])
print(strings["start_3"][lang])
path = ""
while path == "":
    path = input(strings["path"][lang])
    if path == "":
        path = os.getcwd()
    elif path != "-1":
        if check_path(path) == False:
            path = ""

if path != "-1":
    print(strings["current_dir"][lang] + path)
    
    time_start = time.time()
    print(strings["searching"][lang].format(time.ctime(time_start)))
    
    # PNGs search
    png_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".png") or file.endswith(".apng"):
                png_list.append(os.path.join(root, file))
    png_num = len(png_list)
    
    time_end = time.time()
    time_elapsed = round(time_end - time_start)
    print(strings["finished_in"][lang].format(time.ctime(time_end), time_elapsed, conv(time_elapsed, lang)))
    print(strings["found_pngs_num"][lang] + str(png_num))
    
    if png_num > 0:
        time_start = time.time()
        print(strings["pngs_analysis"][lang].format(time.ctime(time_start)))
        
        # APNGs search
        apng_list = []
        for png in progressbar(range(png_num), strings["files_analysis"][lang], 40):
            f = open(png_list[png], "rb")
            file = f.read()
            if is_apng(file):
                apng_list.append(png_list[png])
            f.close()
        apng_num = len(apng_list)
        
        time_end = time.time()
        time_elapsed = round(time_end - time_start)
        print(strings["finished_in"][lang].format(time.ctime(time_end), time_elapsed, conv(time_elapsed, lang)))
        print(strings["found_apngs_num"][lang] + str(apng_num))
        
        if apng_num > 0:
            print(strings["found_apngs_list"][lang])
            for apng in apng_list:
                print(apng)
    
    ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)
    input(strings["finished"][lang])
else:
    print(strings["cancelled"][lang])
    time.sleep(2.5)
