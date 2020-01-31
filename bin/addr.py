from addrparser import AddrParser
addr = AddrParser("addrdb")

def parse(line):
    ret = addr.parse(line)
    #print(ret)
    if len(ret) != 1:
        return ('', line)
    ret = ret[0]
    if ret['level'] == "city":
        if len(ret['address']) != 1:
            return ('', line)
        ret = ret['address'][0]
        return (ret['code'], ret['province']+ret['city'])
    elif ret['level'] == "province":
        if len(ret['address']) != 1:
            return ('', line)
        ret = ret['address'][0]
        return (ret['code'], ret['province'])
    elif ret['level'] == "county":
        if len(ret['address']) != 1:
            return ('', line)
        ret = ret['address'][0]
        return (ret['code'], ret['province']+ret['county'])
    return ('', line)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: %s <str>" % sys.argv[0])
        sys.exit(1)
    print(parse(sys.argv[1]))

