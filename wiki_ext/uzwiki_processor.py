import os, string, re, csv
os.system('python2 WikiExtractor.py -o uzwiki uzwiki.xml')

def extractor(path):
    list_of_tokens = []
    for root, dirs, files in os.walk(path):
        for file in files:
            with open(root + '/' + file, 'r',encoding='utf-8') as text:
                for line in text:
                    if '<doc' in line or '</doc>' in line or 'Vikipediya' in line or 'MediaWiki' in line:
                        continue
                    else:
                        list_of_tokens += line.split()
    return list_of_tokens
            
wiki = extractor('./uzwiki/AA')

dictionary = dict()
for word in wiki:
    word = word.strip(string.punctuation + '…„“—"–')
    if len(word):
        word = word.lower()
        dictionary[word] = dictionary.get(word, 0) + 1

dict_sorted = sorted(dictionary.items(), key= lambda x:x[1], reverse=True)
 
with open('wordlist.tsv', 'w', encoding='utf-8') as file_to_write:
    writer = csv.writer(file_to_write, delimiter='\t')
    writer = writer.writerows(dict_sorted)

