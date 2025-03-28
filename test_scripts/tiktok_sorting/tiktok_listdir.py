import os
import time

folder = r"C:\Users\Игорь\00_phone_backup\Дозагрузка\Movies\TikTok"
start = time.time()
lst = os.listdir(folder)

for filename in lst:
    if '2024' not in filename and '2025' not in filename and '2023' not in filename:
        print(filename)
