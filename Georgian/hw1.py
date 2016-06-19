#сохраняем табличку соответствия грузинских букв и IPA с сайта Википедии в формате .csv, 
#при сохранении в качестве разделителя выбираем табы. 
f = open("translit.csv", "r", encoding="utf8")

#создаем пустой словарь, где ключами будут символы грузинских букв, а значениями - символы ipa
translit_dict = {}

#создаем цикл, который построчно читает нашу табличку и выбирает первый и третий столбец, 
#записывает значения и готовит словарь
for line in f:
	delimiter = line.split("	")
	character = delimiter[0]
	ipa = delimiter[2]
	translit_dict[character] = ipa 

#print(translit_dict) - проверяем словарь на соответствие символяам с помощью функции print()

#открываем файл с тектстом для транслита
with open("text.txt", encoding="utf8") as file:
    output = file.read()

#создаем переменную для хранения результата
translit = output

#запускаем процесс транслитерации и записываем результат в файл
for key in translit_dict:
	translit = translit.replace(key, translit_dict[key])
with open("text2.txt","w",encoding="utf8") as textOutput:
    textOutput.write(translit)
