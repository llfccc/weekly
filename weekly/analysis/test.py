source=[{'date':'2017-2-1','name':"a",'value':1},\
        {'date':'2017-2-1','name':"c",'value':3},\
        {'date':'2017-2-1','name':"b",'value':2},\
        {'date':'2017-2-2','name':"b",'value':1}]

data = dict()
for i in source:
    if i['date'] not in data.keys():
        data[i['date']]=dict()
        data[i['date']]['name'] = list()
        data[i['date']]['value'] = list()
        data[i['date']]['name'].append(i['name'])
        data[i['date']]['value'].append(i['value'])
    else:
        if i['name'] not in data[i['date']]['name']:
            data[i['date']]['name'].append(i['name'])
        # if i['value'] not in data[i['date']]['value']:
        data[i['date']]['value'].append(i['value'])
print data