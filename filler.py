import os
import datetime
import re
from typing import List, Tuple

def read_file(filename: str) -> str:
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Файл {filename} не существует.")
    with open(filename, 'r', encoding='cp866') as file:
        return file.read()

def find_placeholders(content: str) -> List[Tuple[str, int]]:
    placeholders = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        matches = re.finditer(r'([^_\s]+(?:\s+[^_\s]+)*)\s*(_+)', line)
        for match in matches:
            placeholder = match.group(1).strip()
            placeholders.append((placeholder, i))
    return placeholders

def fill_placeholders(content: str, placeholders: List[Tuple[str, int]]) -> str:
    lines = content.split('\n')
    for placeholder, line_number in placeholders:
        value = input(f"Введите {placeholder} (или нажмите Enter, чтобы оставить пустым): ").strip()
        if value:
            lines[line_number] = re.sub(r'(_+)', value, lines[line_number], count=1)
        else:
            print(f"Поле '{placeholder}' оставлено пустым.")
    return '\n'.join(lines)

def save_file(content: str, original_filename: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}.txt"
    with open(new_filename, 'w', encoding='cp866') as file:
        file.write(content)
    return new_filename

def add_left_margin(content: str, margin_size: int = 5) -> str:
    return '\n'.join(' ' * margin_size + line for line in content.split('\n'))

def print_file(filename: str):
    with open(filename, 'r', encoding='cp866') as file:
        content = file.read()
    
    content_with_margin = add_left_margin(content)
    
    temp_filename = f"temp_{os.path.basename(filename)}"
    with open(temp_filename, 'w', encoding='cp866') as temp_file:
        temp_file.write(content_with_margin)
    
    with open('LPT3', 'wb') as printer:
        # Инициализация принтера
        printer.write(b'\x1B@')
        # Установка левого поля в 0
        printer.write(b'\x1BL\x00\x00')
        # Установка межстрочного интервала в 1/6 дюйма (стандарт)
        printer.write(b'\x1B2')
        # Установка каретки в начальное положение
        printer.write(b'\r')
        # Печать содержимого файла
        os.system(f"type {temp_filename} > LPT3")
		#КОМАНДА FF ДЛЯ ВЫТАЛКИВАНИЯ ЛИСТА
		#ЗАКОММЕНТИРОВАТЬ ЕСЛИ ВЫ ПЕЧАТАЕТЕ НА РУЛОННОЙ БУМАГЕ
        printer.write(b'\x0C')
		#ЕСЛИ У ВАС РУЛОННАЯ БУМАГА, ТО ВЫ МОЖЕТЕ ДОБАВИТЬ НЕСКОЛЬКО СТРОК, ЧТОБ БУМАГА НЕ "ЗАСТРЯЛА" В ПРИНТЕРЕ. 
		#ЗАМЕНИТЕ 3 НА НУЖНОЕ КОЛИЧЕСТВО СТРОК
		#printer.write(b'\r\n' * 3)
        #ЕСЛИ У ВАС ЧЕКОВЫЙ ПРИНТЕР, ТО НУЖНО ДОБАВИТЬ КОМАНДУ ОТРЕЗА ЧЕКА. РАСКОММЕНТИРУЙТЕ ЭТО.
        #ТАК ЖЕ, ЕСЛИ ВЫ ИСПЫТВАЕТЕ ПРОБЛЕМЫ С ПУСТЫМИ ПРОСТРАНСТВАМИ ПРИ ВЫДАЧЕ ЧЕКА, ТО СЛЕДУЕТ ДОБАВИТЬ В КОНЕЦ
        #ВАШЕГО ФАЙЛА ПУСТЫЕ СТРОКИ, ОТ 1 ДО 10
        
        #cut_command = b'\x1D\x56\x00'
        #printer.write(cut_command)
    os.remove(temp_filename)

def main():
    while True:
        filename = input("Введите имя файла для заполнения: ")
        try:
            content = read_file(filename)
            break
        except FileNotFoundError as e:
            print(e)

    placeholders = find_placeholders(content)
    filled_content = fill_placeholders(content, placeholders)
    new_filename = save_file(filled_content, filename)
    print(f"Файл сохранен как {new_filename}")

    print_choice = input("Отправить на печать? (y/n): ")
    if print_choice.lower() == 'y':
        try:
            print_file(new_filename)
            print("Документ отправлен на печать.")
        except Exception as e:
            print(f"Ошибка при печати: {e}")
            print("Убедитесь, что принтер подключен и включен.")

if __name__ == "__main__":
    main()