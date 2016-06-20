from lxml import html
import requests, re, os

def crawl(id):
    link = 'http://www.hron.ru/?content=statya&t=' + str(id)
    page = requests.get(link)
    tree = html.fromstring(page.content)
    
    def clear_tags(row):
        text = html.tostring(row, encoding='utf-8').decode('utf-8')
        text = re.sub('<.*?>', ' ', text)
        text = ' '.join(text.split())
        return text

    def get_date(date_row):
        months = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05',
                 'июня': '06', 'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10',
                 'ноября': '11', 'декабря': '12'}
        date_row = date_row.split()
        return date_row[-4] + '.' + months[date_row[-3]] + '.' + date_row[-2]

    cells = tree.xpath('//table[@width="95%"]/tr/td')
    
    return (get_date(clear_tags(cells[7])), clear_tags(cells[9]), clear_tags(cells[10]), clear_tags(cells[11]))


import csv
with open('meta.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='', quotechar='')
    writer.writerow(['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere',
                 'genre_fi', 'type', 'topic', 'chronotop', 'style', 'audience_age', 
                 'audience_level', 'audience_size', 'source', 'publication', 'publisher',
                 'publ_year', 'medium', 'country', 'region', 'language'])
    for id in range(1, 49252):
        if i % 100 == 0:
            print(i)
        (date, category, title, text) = crawl(id)
        dir_name = '/'.join(date.split('.')[::-1])
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        with open(dir_name + '/' + str(id) + '.txt', 'w', encoding='utf-8') as file:
            file.write('@au Noname\n')
            file.write('@ti ' + title + '\n')
            file.write('@da ' + date + '\n')
            file.write('@topic ' + category + '\n')
            file.write('@url http://www.hron.ru/?content=statya&t=' + str(id) + '\n')
            file.write(text)
            writer.writerow([dir_name + '/' + str(id) + '.txt', '', '', '', title, date,
                         'публицистика', '', '', category, '', 'нейтральный', 'н-возраст',
                         'н-уровень', 'городская', 'http://www.hron.ru/?content=statya&t=' + str(id),
                         'Орская хроника', '', date.split('.')[-1], 'газета', 'Россия', 'Орск', 'ru'])                      

import glob
for file in glob.glob('*/*/*/*.txt'):
    stem = 'mystem.exe -cdig --format xml'
    output = file[:-3] + 'xml'
    output = os.path.join('xml', output)
    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))
    os.system(stem + ' ' + file + ' ' + output)

for file in glob.glob('*/*/*/*.txt'):
    stem = 'mystem.exe -cdig'
    output = os.path.join('plaintext',file)
    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))
    os.system(stem + ' ' + file + ' ' + output)

