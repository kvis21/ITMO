import os
import shutil

source_dir = os.path.abspath("./soft_files_in")

def sort_files_in_dir(directory):
    print(f"Анализ директории: {source_dir}...")
    
    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)

        if os.path.isdir(filepath):
            continue

        _, file_extension = os.path.splitext(filename)
        
        if not file_extension:
            continue
            
        extension = file_extension[1:].lower()
        
        target_folder = os.path.join(directory, extension)
        
        # Создаем целевую директорию, если она не существует
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
            print(f"Создана директория: {target_folder}")
            
        # Перемещаем файл
        try:
            shutil.move(filepath, os.path.join(target_folder, filename))
            print(f"Перемещен файл: {filename} -> {extension}/")
        except Exception as e:
            print(f"Ошибка при перемещении {filename}: {e}")

if __name__ == "__main__":
    # ВНИМАНИЕ: Скрипт выполняет реальное перемещение файлов.
    # Для безопасного тестирования рекомендуется создать отдельную папку.
    sort_files_in_dir("./soft_files_out")