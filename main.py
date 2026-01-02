"""
HWID Authorization Tool - Инструмент для получения HWID
"""
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import hwid


def resource_path(relative_path):
    """ Получить абсолютный путь к ресурсу, работает для dev и для PyInstaller """
    try:
        # PyInstaller создает временную папку и сохраняет путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class HWIDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HWID Authorization")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Установка иконки
        try:
            icon_path = resource_path("assets/icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass
        
        # Цветовая схема
        self.bg_color = "#1a1a2e"
        self.secondary_bg = "#16213e"
        self.accent_color = "#0f3460"
        self.text_color = "#eaeaea"
        self.accent_text = "#00d4ff"
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        self.load_hwid()
    
    def setup_ui(self):
        """Создать интерфейс"""
        # Заголовок
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=30)
        
        title_label = tk.Label(
            title_frame,
            text="HWID Authorization Tool",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_text
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Аппаратный идентификатор вашей системы",
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Контейнер для HWID
        hwid_container = tk.Frame(self.root, bg=self.secondary_bg, relief=tk.FLAT)
        hwid_container.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        hwid_label = tk.Label(
            hwid_container,
            text="Ваш HWID:",
            font=("Segoe UI", 12, "bold"),
            bg=self.secondary_bg,
            fg=self.text_color
        )
        hwid_label.pack(pady=(20, 10))
        
        # Текстовое поле для HWID
        self.hwid_text = tk.Text(
            hwid_container,
            height=3,
            font=("Consolas", 11),
            bg=self.accent_color,
            fg=self.accent_text,
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.hwid_text.pack(pady=10, padx=20, fill=tk.X)
        self.hwid_text.config(state=tk.DISABLED)
        
        # Кнопка копирования
        copy_btn = tk.Button(
            hwid_container,
            text="📋 Скопировать в буфер обмена",
            font=("Segoe UI", 11, "bold"),
            bg=self.accent_text,
            fg=self.bg_color,
            activebackground="#00a8cc",
            activeforeground=self.bg_color,
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.copy_to_clipboard
        )
        copy_btn.pack(pady=(10, 20))
        
        # Hover эффект для кнопки
        def on_enter(e):
            copy_btn['bg'] = '#00a8cc'
        
        def on_leave(e):
            copy_btn['bg'] = self.accent_text
        
        copy_btn.bind("<Enter>", on_enter)
        copy_btn.bind("<Leave>", on_leave)
        
        # Информация внизу
        info_label = tk.Label(
            self.root,
            text="Этот ID уникален для вашего оборудования и не изменится после переустановки Windows",
            font=("Segoe UI", 8),
            bg=self.bg_color,
            fg="#888888",
            wraplength=500
        )
        info_label.pack(pady=(0, 20))
    
    def load_hwid(self):
        """Загрузить и отобразить HWID"""
        hwid_value = hwid.get_hwid()
        
        self.hwid_text.config(state=tk.NORMAL)
        self.hwid_text.delete(1.0, tk.END)
        self.hwid_text.insert(1.0, hwid_value)
        self.hwid_text.config(state=tk.DISABLED)
    
    def copy_to_clipboard(self):
        """Скопировать HWID в буфер обмена"""
        hwid_value = self.hwid_text.get(1.0, tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(hwid_value)
        self.root.update()
        
        messagebox.showinfo("Успешно", "HWID скопирован в буфер обмена!")


def main():
    root = tk.Tk()
    app = HWIDApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
