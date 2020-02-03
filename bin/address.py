from addrparser import AddrParser
addr = AddrParser("addrdb")

_cities = set(["北京市","天津市","上海市","重庆市"])
def address(line):
    ret = addr.parse(line)
    if len(ret) < 0: return ("NA", "NA")
    ret = ret[0]
    ret = ret['address'][0]
    code = ret['code']
    if len(code) > 6: code = ret['code'][:6]
    else: code = code + '0'*(6-len(code))
    name = ""
    if 'province' in ret: name += ret['province']
    if 'city' in ret and name not in _cities:
        name += ret['city']
    if 'county' in ret: name += ret['county']
    return (code, name)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: %s <str>" % sys.argv[0])
        sys.exit(1)
    print(address(sys.argv[1]))

