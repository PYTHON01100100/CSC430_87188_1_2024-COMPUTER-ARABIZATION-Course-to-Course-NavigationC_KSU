import tkinter as tk
from tkinter import font, filedialog, messagebox
from PIL import Image, ImageTk
import keyboard
from enum import Enum
import pygame
import pyttsx3

class configType(Enum):
    HotKey = 1
    ReMap = 2

class keyboardController:
    shortcut = []
    
    arabic_to_english = {
        'a': 'ش',
        'b': 'لا',
        'c': 'ؤ',
        'd': 'ي',
        'e': 'ث',
        'f': 'ب',
        'g': 'ل',
        'h': 'ا',
        'i': 'ه',
        'j': 'ت',
        'k': 'ن',
        'l': 'م',
        'm': 'ة',
        'n': 'ى',
        'o': 'خ',
        'p': 'ح',
        'q': 'ض',
        'r': 'ق',
        's': 'س',
        't': 'ف',
        'u': 'ع',
        'v': 'ر',
        'w': 'ص',
        'x': 'ء',
        'y': 'غ',
        'z': 'ئ',
        '`': 'ذ',
        '[': 'ج',
        ']': 'د',
        '\'': 'ط',
        ';': 'ك',
        '.': 'ز',
        ',': 'و',
        '/': 'ظ'
    }
    
    def add_shortcut_action(self, keys, action, type):
        self.shortcut.append((keys, action, type))

    def map_english_to_arabic(self, event_name):
        return self.arabic_to_english.get(event_name)
    
    def suppress_shortcut(self, keys):
        self.add_shortcut_action(keys, lambda: None, configType.HotKey)

    def play_audio(self, file_name):
        audio_folder = "C:\\Users\\d7oom\\Desktop\\Eclipsepro"
        file_path = audio_folder + "\\" + file_name + ".wav"
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        pygame.time.delay(int(sound.get_length() * 800))

    def toggle_language(self):
        if self.language == "arabic":
            self.language = "english"
            self.play_audio("english")  # تشغيل التنبيه باللغة الإنجليزية
        else:
            self.language = "arabic"
            self.play_audio("arabic")  # تشغيل التنبيه باللغة العربية
        print("Language switched to:", self.language)
        # Speak the language toggle status
        if self.language == "arabic":
            self.speaker.say("تم تغيير اللغة إلى العربية")
        else:
            self.speaker.say("Language switched to English")
        self.speaker.runAndWait()

    def switch_text_direction(self):
        if self.text_direction == "rtl":
            self.text_direction = "ltr"
        else:
            self.text_direction = "rtl"
        print("Text direction switched to:", self.text_direction)

    def switch_keyboard_layout(self, event):
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "right ctrl":
                print("Switching text direction to left-to-right")
                self.text_editor.config(direction="ltr")
            elif event.name == "left ctrl":
                print("Switching text direction to right-to-left")
                self.text_editor.config(direction="rtl")
    
    def compile(self):
        for keys, action, type in self.shortcut:
            if type == configType.HotKey:
                keyboard.add_hotkey(keys, action, suppress=True)
            elif type == configType.ReMap:
                keyboard.remap_key(keys, action)

    def __init__(self):
        self.language = "arabic"
        self.text_direction = "rtl"
        self.speaker = pyttsx3.init()

config = keyboardController()
config.add_shortcut_action('b', lambda: keyboard.write('ال'), configType.HotKey)
config.add_shortcut_action('shift+b', lambda: keyboard.write('أل'), configType.HotKey)
config.suppress_shortcut('caps lock')
config.add_shortcut_action('q+w+e', lambda: print('action'), configType.HotKey)
config.add_shortcut_action('f1', config.toggle_language, configType.HotKey)  # عند الضغط على زر F1 يتم تبديل اللغة
config.add_shortcut_action('ctrl', config.switch_text_direction, configType.HotKey)  # لتغيير اتجاه الكتابة
config.add_shortcut_action('right ctrl', config.switch_keyboard_layout, configType.HotKey)  # يستخدم الزر Ctrl الأيمن لتحويل الكتابة من اليمين إلى اليسار
config.add_shortcut_action('left ctrl', config.switch_keyboard_layout, configType.HotKey)  # يستخدم الزر Ctrl الأيسر لتحويل الكتابة من اليسار إلى اليمين
config.compile()

def change_font():
    selected_font = font.Font(family=font_family.get(), size=font_size.get(), weight=font_weight.get(), slant=font_slant.get())
    text_editor.config(font=selected_font)

def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Word files", "*.docx")])
    if file_path:
        if file_path.endswith(".txt"):
            with open(file_path, "w") as f:
                text = text_editor.get("1.0", "end-1c")
                f.write(text)
        elif file_path.endswith(".docx"):
            doc = docx.Document()
            text = text_editor.get("1.0", "end-1c")
            doc.add_paragraph(text)
            doc.save(file_path)
        messagebox.showinfo("تم الحفظ", "تم حفظ الملف بنجاح!")

root = tk.Tk()
root.title("محرر نصوص وعرض الصور")

text_editor = tk.Text(root, font=("Arial", 12))
font_family_label = tk.Label(root, text="الخط:")
font_family = tk.StringVar()
font_family.set("Arial")
font_family_dropdown = tk.OptionMenu(root, font_family, "Arial", "Times New Roman", "Courier New")
font_size_label = tk.Label(root, text="الحجم:")
font_size = tk.IntVar()
font_size.set(12)
font_size_entry = tk.Entry(root, textvariable=font_size)
font_weight_label = tk.Label(root, text="الوزن:")
font_weight = tk.StringVar()
font_weight.set("normal")
font_weight_dropdown = tk.OptionMenu(root, font_weight, "normal", "bold")
font_slant_label = tk.Label(root, text="الميل:")
font_slant = tk.StringVar()
font_slant.set("roman")
font_slant_dropdown = tk.OptionMenu(root, font_slant, "roman", "italic")
apply_button = tk.Button(root, text="تطبيق", command=change_font)
open_image_button = tk.Button(root, text="فتح صورة", command=open_image)
save_button = tk.Button(root, text="حفظ الملف", command=save_file)
image_label = tk.Label(root)

text_editor.grid(row=0, column=0, columnspan=5, padx=10, pady=10)
font_family_label.grid(row=1, column=0, padx=10, pady=5)
font_family_dropdown.grid(row=1, column=1, padx=10, pady=5)
font_size_label.grid(row=1, column=2, padx=10, pady=5)
font_size_entry.grid(row=1, column=3, padx=10, pady=5)
font_weight_label.grid(row=1, column=4, padx=10, pady=5)
font_weight_dropdown.grid(row=1, column=5, padx=10, pady=5)
font_slant_label.grid(row=1, column=6, padx=10, pady=5)
font_slant_dropdown.grid(row=1, column=7, padx=10, pady=5)
apply_button.grid(row=1, column=8, padx=10, pady=5)
open_image_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
save_button.grid(row=2, column=2, columnspan=2, padx=10, pady=5)
image_label.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

root.mainloop()