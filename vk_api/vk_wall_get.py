import csv, requests

search_url = 'https://api.vk.com/method/users.search'
search_params = {
    'access_token':'0c73fd80751533f519c10f9a2371f6356889f1ec2ca1e1c56bb59b40718b6bf08d64c244e63f20eff0318',
    'count':100,
    'city': 785, #Урюпинск
    'country': 1,
    'fields':'bdate, sex, occupation, relation, personal'
}

find_users = requests.get(search_url, params=search_params)            
data = find_users.json()

field_dict = {'first_name':0, 'last_name':0, 'sex':1,'uid':2, 'bdate':3, 'relation':4,'langs':5}

table = open('metadata.csv', 'a',newline='',encoding='utf-8')
writer = csv.writer(table, quoting=csv.QUOTE_NONE, escapechar='', quotechar='', delimiter='\t')

for i in range(1, len(data['response'])):
    meta = [''] * 6
    for feature in data['response'][i]:                                         
        if feature in field_dict.keys():
            meta[field_dict[feature]] += ' ' + str(data['response'][i][feature])
            meta[field_dict[feature]] = meta[field_dict[feature]].strip()
        if feature == 'personal':
            try:
                meta[field_dict['langs']] = data['response'][i][feature]['langs']
            except:
                pass
    writer.writerow(meta)                          
    
    target_id = data['response'][i]['uid']
    wall_url = 'https://api.vk.com/method/wall.get'
    wall_params = {
        'owner_id':target_id,
        'count':100,
        'filter':'owner'
    }
    get_wall = requests.get(wall_url, params=wall_params)             
    posts = get_wall.json()
    with open('urupinsk_posts\id' + str(target_id) + '.txt', 'a', encoding='utf-8') as file:        
        try:
            for post in posts['response'][1:]:
                post['text'] = post['text'].replace('<br>','\n')
                file.write(post['text'] + '\n')
        except:
            pass
        
table.close()