import sys
import re
import json

def main(f):
    content = open(f).read()
    data = re.findall(r"getAreaStat = (.+?)}catch", content)
    if len(data) < 0: 
        print("no data")
        return
    item = json.loads(data[0])
    print(data[0])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <file>")
        sys.exit(1)
    main(sys.argv[1])
