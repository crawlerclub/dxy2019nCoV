import parse
import addr
import json
import glob
f = sorted(glob.glob("../data/*.html"))[-1]
item = parse.parse(f)
special = set(["北京市","上海市","天津市","重庆市"])
data = []
for city in item['city']:
    if len(city['cities']) == 0 or city['provinceName'] in special:
        n = addr.parse(city['provinceName'])
        if n[0] == '': continue
        data.append({'code':n[0], 'addr':n[1], 'count': city['confirmedCount']})
    else:
        for c in city['cities']:
            n = addr.parse(city['provinceName']+c['cityName'])
            if n[0] == '': continue
            data.append({'code':n[0], 'addr':n[1], 'count': c['confirmedCount']})

#import sys
#cnt = int(sys.argv[1])
#data = [x for x in data if x['count'] >= cnt]

name = f[8:-5]
with open("../cities/%s.json" % name, "w") as out:
    out.write(json.dumps(data, ensure_ascii=False))
#print(json.dumps(data, ensure_ascii=False))
