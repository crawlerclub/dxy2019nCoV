import glob
import parse

def records():
    times = set()
    data = []
    for f in glob.glob("../data/*.html"):
        item = parse.parse(f)
        if item["ts"] in times: continue
        times.add(item["ts"])
        for p in item['city']:
            del p['cities']
            del p['comment']
            del p['provinceName']
            p['ts'] = item["ts"]
        data.extend(item["city"])
    return data

if __name__ == "__main__":
    data = records()
    print(len(data))
