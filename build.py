"""
Скрипт для компиляции приложения в EXE
"""
import os
import subprocess
import sys


def build_exe():
    """Собрать приложение в один EXE файл"""
    print("Starting build...")
    
    # Путь к PyInstaller
    pyinstaller_path = r"C:\Users\user\AppData\Local\Programs\Python\Python314\Scripts\pyinstaller.exe"
    
    # Параметры для PyInstaller
    cmd = [
        pyinstaller_path,
        "--onefile",  # Один файл
        "--windowed",  # Без консоли
        "--name=HWID_Authorization",  # Имя файла
        "--clean",  # Очистить кеш
        "--add-data=assets;assets",  # Включить папку assets (Windows syntax)
    ]
    
    # Добавляем иконку если она есть
    icon_path = os.path.abspath("assets/icon.ico")
    if os.path.exists(icon_path):
        cmd.append(f"--icon={icon_path}")
    
    cmd.append("main.py")
    
    try:
        # Запускаем PyInstaller
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True)
        
        print("\nBuild completed successfully!")
        print("Executable: dist\\HWID_Authorization.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"\nBuild error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\nPyInstaller not found at specified path!")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()
