import glob
import parse

def main():
    times = set()
    data = []
    for f in glob.glob("../data/*.html"):
        item = parse.parse(f)
        if item["ts"] in times: continue
        times.add(item["ts"])
        for p in item['city']:
            del p['cities']
            p['ts'] = item["ts"]
        data.extend(item["city"])
    print(data)

if __name__ == "__main__":
    main()
