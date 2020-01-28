import sys
import re
import json

def et(pattern, content):
    data = re.findall(pattern, content)
    if len(data) <= 0: return ''
    return data[0]

def parse(f):
    content = open(f).read()
    data = et(r"getAreaStat = (.+?)}catch", content)
    city = json.loads(data)
    ts = et(r"截至 (.+?)（北京时间）数据统计", content)
    data = et(r"getListByCountryTypeService1 = (.+?)}catch", content)
    china = json.loads(data)
    data = et(r"getListByCountryTypeService2 = (.+?)}catch", content)
    world = json.loads(data)
    rec = {"ts":ts, "city":city, "china":china, "world":world}
    return rec

def main(f):
    print(json.dumps(parse(f), ensure_ascii=False))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <file>")
        sys.exit(1)
    main(sys.argv[1])
