import xlrd, csv, pandas
workbook = xlrd.open_workbook('corpus.xls')
sheet = workbook.sheet_by_index(0)

with open('corpus.csv', 'w', encoding='utf-8') as table_file:
    writer = csv.writer(table_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_NONE, escapechar='\\')
    for row_id in range(sheet.nrows):
        writer.writerow(sheet.row_values(row_id))

# Задание 1 - разбить тексты большой длины
with open('balanced_corpus.csv', 'w', encoding='utf-8') as table_file:
    writer = csv.writer(table_file, delimiter='\t', quotechar='|', quoting=csv.QUOTE_NONE, escapechar='\\')
    table = pandas.read_csv('corpus.csv', delimiter='\t')
    for index, row in table.iterrows():
        if index == 0:
            writer.writerow(row)
            continue

        words = int(float(row[-2]))
        if words >= 100000:
            clones_number = 3
        elif 70000 <= words < 100000:
            clones_number = 2
        else:
            clones_number = 1
        words = str(words // clones_number)
        row[-2] = words

        for _ in range(clones_number):
            writer.writerow(row)

# Задание 2 - выделить подкорпусы по жанрам
spheres = ['художественная', 'мемуары', 'публицистика | нехудожественная', 'учебно-научная | нехудожественная', 'бытовая | нехудожественная',
           'официально-деловая | нехудожественная', 'церковно-богословская | нехудожественная', 'производственно-техническая | нехудожественная',
           'реклама | нехудожественная']
header = 'path	author	sex	birthday	header	created	sphere	genre_fi	type	topic	chronotop	style	audience_age	audience_level	\
          audience_size	source	publication	publisher	publ_year	medium	subcorpus	tagging	words    '.split('\t')
table = pandas.read_csv('corpus.csv', delimiter='\t')
for sphere in spheres[:1]:
    with open(sphere + '.csv', 'w', encoding='utf-8') as sphere_table:
        writer = csv.writer(sphere_table, delimiter='\t', quotechar='|', quoting=csv.QUOTE_NONE, escapechar='\\')
        writer.writerow(header)
        added_words = 0
        sub_table = table.loc[table['sphere'] == sphere]
        for index, row in sub_table.iterrows():
            writer.writerow(row)
            added_words += int(row[-2])
            if added_words > 100000:
                break

# Задание 3 - выделить подкорпусы по датам
dates = ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2015']
header = 'path	author	sex	birthday	header	created	sphere	genre_fi	type	topic	chronotop	style	audience_age	audience_level	\
          audience_size	source	publication	publisher	publ_year	medium	subcorpus	tagging	words    '.split('\t')
table = pandas.read_csv('corpus.csv', delimiter='\t')
for i in range(5, 6):
    with open(dates[i - 1] + '-' + dates[i] + '.csv', 'w', encoding='utf-8') as sphere_table:
        writer = csv.writer(sphere_table, delimiter='\t', quotechar='|', quoting=csv.QUOTE_NONE, escapechar='\\')
        writer.writerow(header)
        added_words = 0
        sub_table = table.loc[(table['created'] < dates[i]) & (table['created'] >= dates[i - 1])]
        for index, row in sub_table.iterrows():
            writer.writerow(row)
            added_words += int(row[-2])
            if added_words > 100000:
                break
