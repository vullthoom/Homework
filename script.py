from datetime import date, datetime
import requests
import sys
import os

import json


# Основные переменные для получения и считывания данных.  
# Если нет интернета или проблемы с диском, код останавливается.
try:
    users_link = requests.get('https://jsonplaceholder.typicode.com/users')
    todos_link = requests.get('https://jsonplaceholder.typicode.com/todos')
    users_file = os.path.dirname(__file__) + '/users.html'
    todos_file = os.path.dirname(__file__) + '/tasks.html'
except requests.exceptions.ConnectionError:
    sys.exit('no internet connect')
except OSError:
    sys.exit('disk problems')


def write_file():
    '''

    Основная функция для записи содержимого файла.  
    Собирает все задачи и сортирует, после чего создает фаил. 

    '''
    user_company = h['company']
    completed = 'Completed tasks:\n'
    not_completed = 'Remaining tasks:\n'
    for i in todos_list:
        if i['userId'] == h['id']:
            if i['completed'] is True:
                if len(i['title']) > 50:
                    completed += f'\n{(i["title"])[:50]}...'
                else:
                    completed += f'\n{i["title"]}'
            else:
                if len(i['title']) > 50:
                    not_completed += f'\n{(i["title"])[:50]}...'
                else:
                    not_completed += f'\n{i["title"]}'
        else:
            continue
    date_time = str(datetime.today())
    with open(txt_file_actual, 'w') as file:
        file.write(f'{h["name"]} <{h["email"]}> {date_time[:-10]}\n{user_company["name"]}\n\n{completed}\n\n{not_completed}')


def if_file_error():
    '''
    
    При получении ошибки при записи файла, удаляет неудавшийся образец и пытается создать его заново, пока не получится.
    
    '''
    os.remove(txt_file_actual)
    try:
        write_file()
    except OSError:
        if_file_error()


# Считывает данные из интернета и сохраняет на компьютере.  
with open(users_file, 'wb') as file:
    file.write(users_link.content)
with open(todos_file, 'wb') as file:
    file.write(todos_link.content)


# Считывает данные с файлов и передает в переменные. 
# После этого удаляет файлы.   
with open(users_file, 'r', encoding='utf-8') as file:
    users_list = json.load(file)
with open(todos_file, 'r', encoding='utf-8') as file:
    todos_list = json.load(file)
os.remove(users_file)
os.remove(todos_file)


# Создает папку для файлов если ее не существует.  
try:
    folder = os.path.dirname(__file__) + '/tasks'
    if os.path.exists(folder) is False:
        os.mkdir(folder)
        print('directory is created')
except PermissionError:
    sys.exit('no access')
except OSError:
    sys.exit('disk problems')


# Перебирает юзеров и создает законченные данные.
for h in users_list:
    if len(str(h['id'])) == 1:
        num = f'00{h["id"]}'
    elif len(str(h['id'])) == 2:
        num = f'0{h["id"]}'
    else:
        num = f'{h["id"]}'
    try:
        txt_file_actual = os.path.dirname(__file__) + f'/tasks/{num}_{h["username"]}.txt'
        if os.path.isfile(txt_file_actual) is True:
            with open(txt_file_actual,'r') as file:
                line = file.readline()
                date_task = line[-17:-7]
                time_task = line[-6:-1]
            txt_file = os.path.dirname(__file__) + f'/tasks/{num}_{h["username"]}_{date_task}T{time_task[:2]}.{time_task[3:]}.txt'
            date_today = str(date.today())
            if date_task != date_today:
                os.rename(txt_file_actual, txt_file)
                write_file()
        else:
            write_file()
    except OSError:
        if_file_error()
        continue


# Сообщает об успешном выполнении кода.  
print('complete')