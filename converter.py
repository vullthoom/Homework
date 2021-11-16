import json
import requests
import os

curse = requests.get('http://www.floatrates.com/daily/rub.json')
with open(os.path.dirname(__file__) + '/curse.html','wb') as file:
    file.write(curse.content)

sum = int(input('Сумма: '))
val1 = input('Конвертируемая валюта: ').lower()
val2 = input('Валюта в которую конвертировать: ').lower()
def operation():
    with open(os.path.dirname(__file__) + '/curse.html','rb') as file:
        curse_dict = json.load(file)
    if val1 == 'rus': # Из рублей
        val3 = curse_dict[f'{val2}']
        resultat = sum * val3['rate']
    elif val2 == 'rus': # В рубли
        val3 = curse_dict[f'{val1}']
        resultat = sum * val3['inverseRate']
    else: # Из других валют в другие через рубли
        val3 = curse_dict[f'{val1}']
        resultat = sum * val3['inverseRate']
        val3 = curse_dict[f'{val2}']
        resultat = resultat * val3['rate']
    print(round(resultat, 2))
operation()

# я не сделала ввод полного названия валюты, ибо я слишком ленива для такого, я даже трехбуквенные названия то не запоминаю...
# P.S. Очень долго пыталась понять как превратить байты в словарь...