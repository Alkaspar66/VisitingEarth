import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox

def build_gallery_json(source_dir, output_path):
    galleries = {}

    for root, dirs, files in os.walk(source_dir):
        # пропускаем корневую папку, берем только подпапки
        if root == source_dir:
            for d in dirs:
                gallery_path = os.path.join(root, d)
                rel_path = os.path.relpath(gallery_path, source_dir).replace("\\", "/") + "/"

                # фильтруем только картинки
                images = [f for f in os.listdir(gallery_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp"))]

                galleries[d] = {
                    "title": d.capitalize(),
                    "path": rel_path,
                    "files": images
                }

    # пишем json
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(galleries, f, indent=2, ensure_ascii=False)

    return output_path

def select_source():
    dir_selected = filedialog.askdirectory(title="Выберите папку с галереями")
    if dir_selected:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, dir_selected)
        default_output = os.path.join(os.getcwd(), "galleries.json")
        output_entry.delete(0, tk.END)
        output_entry.insert(0, default_output)

def select_output():
    file_selected = filedialog.asksaveasfilename(
        title="Сохранить JSON",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        initialfile="galleries.json"
    )
    if file_selected:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_selected)

def run_script():
    source_dir = source_entry.get().strip()
    output_path = output_entry.get().strip()

    if not source_dir or not os.path.isdir(source_dir):
        messagebox.showerror("Ошибка", "Укажите корректную папку-источник")
        return

    if not output_path:
        output_path = os.path.join(os.getcwd(), "galleries.json")

    try:
        result = build_gallery_json(source_dir, output_path)
        messagebox.showinfo("Готово", f"JSON успешно создан:\n{result}")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

# GUI
root = tk.Tk()
root.title("Генератор galleries.json")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

# выбор source dir
tk.Label(frame, text="Папка с галереями:").grid(row=0, column=0, sticky="w")
source_entry = tk.Entry(frame, width=50)
source_entry.grid(row=0, column=1, padx=5)
tk.Button(frame, text="Выбрать...", command=select_source).grid(row=0, column=2)

# выбор output file
tk.Label(frame, text="JSON файл:").grid(row=1, column=0, sticky="w")
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=1, column=1, padx=5)
tk.Button(frame, text="Выбрать...", command=select_output).grid(row=1, column=2)

# кнопка запуска
tk.Button(frame, text="Сгенерировать", command=run_script, bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
