# ==================== ІМПОРТ БІБЛІОТЕК ====================
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
 QApplication, QWidget, QPushButton, QLabel,
 QListWidget, QLineEdit, QTextEdit,
 QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
)
import os # для роботи з файлами
# ==================== ЗАПУСК ДОДАТКУ ====================
app = QApplication([]) # головний об'єкт PyQt
notes = [] # список усіх заміток у форматі:
 # [назва, текст, [теги]]
# ==================== СТВОРЕННЯ ВІКНА ====================
notes_win = QWidget()
notes_win.setWindowTitle('Розумні замітки')
notes_win.resize(900, 600)
# ==================== СТВОРЕННЯ ВІДЖЕТІВ ====================
# список заміток
list_notes = QListWidget()
list_notes_label = QLabel('Список заміток')
# кнопки для заміток
button_note_create = QPushButton('Створити замітку')
button_note_del = QPushButton('Видалити замітку')
button_note_save = QPushButton('Зберегти замітку')
# поле для введення тегу
field_tag = QLineEdit()
field_tag.setPlaceholderText('Введіть тег...')
# поле для тексту замітки
field_text = QTextEdit()
# кнопки для тегів
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')
# список тегів
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')
# ==================== РОЗТАШУВАННЯ (LAYOUT-и) ====================
layout_notes = QHBoxLayout()
# ліва частина — текст
col_1 = QVBoxLayout()
col_1.addWidget(field_text)
# права частина — списки і кнопки
col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)
col_2.addLayout(row_3)
col_2.addLayout(row_4)
layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)
# ===== ЗАВАНТАЖЕННЯ ЗАМІТОК З ФАЙЛІВ
def load_notes():
 index = 0
 while True:
    filename = f"{index}.txt"
    if not os.path.exists(filename):
        break
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.read().split("\n")
 name = lines[0] # назва
 text = lines[1] # текст
 tags = lines[2].split() if len(lines) > 2 else [] # списоктегів
 notes.append([name, text, tags])
 list_notes.addItem(name)
 index += 1
# ==================== ЗБЕРЕЖЕННЯ ВСІХ ЗАМІТОК ====================
def save_all_notes():
 for i, note in enumerate(notes):
    with open(f"{i}.txt", "w", encoding="utf-8") as file:
        file.write(note[0] + '\n') # назва
        file.write(note[1] + '\n') # текст
        file.write(' '.join(note[2]) + '\n') # теги
# ==================== ПОКАЗ ЗАМІТКИ ====================
def show_note():
 key = list_notes.selectedItems()[0].text()
 for note in notes:
    if note[0] == key:
        field_text.setText(note[1])
        list_tags.clear()
        list_tags.addItems(note[2])
# ==================== СТВОРЕННЯ ЗАМІТКИ ====================
def add_note():
 note_name, ok = QInputDialog.getText(notes_win, "Додати замітку",
"Назва замітки:")
 if ok and note_name:
    notes.append([note_name, '', []])
    list_notes.addItem(note_name)
    save_all_notes()
# ==================== ЗБЕРЕЖЕННЯ ТЕКСТУ ====================
def save_note():
 if list_notes.selectedItems():
    key = list_notes.selectedItems()[0].text()
for note in notes:
    if note[0] == key:
        note[1] = field_text.toPlainText()
        save_all_notes()
# ==================== ВИДАЛЕННЯ ЗАМІТКИ ====================
def del_note():
 if list_notes.selectedItems():
    key = list_notes.selectedItems()[0].text()
 for i, note in enumerate(notes):
    if note[0] == key:
        notes.pop(i)
        break
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
    for i in range(1000):
        try:
        os.remove(f"{i}.txt")
        except:
        break
        for note in notes:
            list_notes.addItem(note[0])
            save_all_notes()
# ==================== РОБОТА З ТЕГАМИ ====================
def add_tag():
 if list_notes.selectedItems():
 key = list_notes.selectedItems()[0].text()
 tag = field_tag.text()
 for note in notes:
 if note[0] == key and tag not in note[2]:
 note[2].append(tag)
 list_tags.addItem(tag)
 field_tag.clear()
 save_all_notes()
def del_tag():
 if list_tags.selectedItems() and list_notes.selectedItems():
 key = list_notes.selectedItems()[0].text()
 tag = list_tags.selectedItems()[0].text()
 for note in notes:
 if note[0] == key and tag in note[2]:
 note[2].remove(tag)
 list_tags.clear()
 for note in notes:
 if note[0] == key:
 list_tags.addItems(note[2])
 save_all_notes()
# ==================== ПОШУК ЗА ТЕГОМ ====================
def search_tag():
 tag = field_tag.text()
 if button_tag_search.text() == "Шукати замітки по тегу" and tag:
 list_notes.clear()
 for note in notes:
 if tag in note[2]:
 list_notes.addItem(note[0])
 button_tag_search.setText("Скинути пошук")
 else:
 list_notes.clear()
 for note in notes:
 list_notes.addItem(note[0])
 button_tag_search.setText("Шукати замітки по тегу")
 field_tag.clear()
# ==================== ПІДКЛЮЧЕННЯ КНОПОК ====================
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)
# ==================== ЗАПУСК ПРОГРАМИ ====================
load_notes()
notes_win.show()
app.exec_()