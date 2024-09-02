import os
import time
import ctypes
from datetime import datetime
import pygetwindow as gw

# Путь к папке с изображениями
IMAGES_FOLDER = r"D:\Progs\Vcode\VSCode-Projects\IMG-PC-Project\IMGPC"

# Словарь с временем и соответствующими изображениями
wallpapers_schedule = {
    ("03:00", "11:59"): os.path.join(IMAGES_FOLDER, "utro.png"),
    ("12:00", "17:59"): os.path.join(IMAGES_FOLDER, "den.png"),
    ("18:00", "21:59"): os.path.join(IMAGES_FOLDER, "zakat.png"),
    ("22:00", "02:59"): os.path.join(IMAGES_FOLDER, "noch.png")
}

# Функция для смены фона рабочего стола
def set_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

# Функция проверки текущего времени и выбора подходящего фона
def check_and_set_wallpaper():
    current_time = datetime.now().strftime("%H:%M")
    
    for time_range, wallpaper in wallpapers_schedule.items():
        start_time, end_time = time_range
        
        # Обработка диапазона времени, который перекрывает сутки (например, 22:00 - 02:59)
        if start_time <= current_time <= end_time or (start_time > end_time and (current_time >= start_time or current_time <= end_time)):
            set_wallpaper(wallpaper)
            break

# Функция для начальной установки фона при запуске скрипта
def set_initial_wallpaper():
    check_and_set_wallpaper()

# Функция для сворачивания окна программы в панель задач
def minimize_to_taskbar():
    try:
        # Получаем текущее окно
        window = gw.getActiveWindow()
        if window:
            window.minimize()
    except Exception as e:
        print(f"Не удалось свернуть окно: {e}")

# Установка начального фона при запуске скрипта
set_initial_wallpaper()

# Свернуть окно программы в панель задач
minimize_to_taskbar()

# Основной цикл для проверки времени и смены фона
last_checked_time = ""
while True:
    current_time = datetime.now().strftime("%H:%M")
    if current_time != last_checked_time:  # Чтобы не менять фон несколько раз за минуту
        check_and_set_wallpaper()
        last_checked_time = current_time
    time.sleep(5)  # Проверять каждые 5 секунд
