table = open('amxar_table.tsv','r',encoding = 'utf-8')
file_to_process = open('amxar_text.txt', 'r', encoding = 'utf-8')
file_to_write = open('amxar_target.txt','a',encoding = 'utf-8')
concord={}
new_table=[]
for line in table:
    line = line.strip('\n')
    line = line.split('\t')
    new_table.append(line)
for i in range(len(new_table)):                
    for j in range(len(new_table[i])):          
        if i!=0 and j!=0:
            concord[new_table[i][j]]= new_table[i][0]+new_table[0][j]
			
for line in file_to_process:
    for i in line:
        if i in concord:
            line = line.replace(i, concord[i])
        else:
            continue
    file_to_write.write(line)
file_to_write.close()

