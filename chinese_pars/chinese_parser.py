import xml.etree.ElementTree as ET
tree = ET.parse('stal.xml')
root = tree.getroot()
text = []
for line in root.iter('se'):
    if 'lang' not in line.attrib:
        text.append(line.text)

dictionary = dict()
with open('cedict_ts.u8', 'r', encoding='utf-8') as dict_file:
    for line in dict_file:
        if line[0] == '#':
            continue
        line = line.split()
        dictionary[line[1]] = dictionary.get(line[1], []) + [' '.join(line[2:])]

def parser(sent, dictionary):
    result = []
    seq = ''
    for char in sent:
        if char not in dictionary and len(char) == 1:
            if seq != '':
                result.append((seq, dictionary[seq]))
                seq = ''
            result.append(char)
        else:    
            seq += char
            if seq not in dictionary:
                result.append((seq[:-1], dictionary[seq[:-1]]))
                seq = seq[-1]
    return result

def to_xml(parsed, filename):
    import re
    import xml.etree.ElementTree as ET
    html = ET.Element('html')
    head = ET.SubElement(html, 'head')
    body = ET.SubElement(html, 'body')
    se = ET.SubElement(body, 'se')
    for i in parsed:
        if len(i) == 1:
            ET.SubElement(se, None).tail = i
            continue
        w = ET.SubElement(se, 'w')
        for j in i[1]:
            transcr = re.findall('^(\[[\w\s:]+\])', j)[0].strip('[]')
            sem = re.findall('(/.*/)', j)[0].strip('/')
            sem = sem.replace('/', ', ')
            ET.SubElement(w, 'ana', lex=i[0], transcr=transcr, sem=sem)
        ET.SubElement(w, None).text = i[0]
    ET.ElementTree(html).write(filename, encoding='utf-8', xml_declaration=True, short_empty_elements=False)

iteration = 1
for sent in text:
    sent_to_write = parser(sent, dictionary)
    to_xml(sent_to_write, 'sents/' +str(iteration)+ 'sentence.xml')
    iteration += 1

