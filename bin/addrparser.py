import os
import pydict
import lsm

keys = ["province","city","county","town","village",]
rkeys = list(reversed(keys))
codelens = {"province":2,"city":4,"county":6,"town":9,"village":12,}

class AddrParser(object):
    def __init__(self, path: str):
        if not os.path.exists(path): raise FileNotFoundError(path)
        self.path = path
        self.db = pydict.Dict(self.path)
        self.code2name = lsm.LSM(os.path.join(path, "code.ldb"))

    def address(self, code):
        code = "{}".format(code).strip()
        l = len(code)
        if l == 0: raise KeyError("Empty code")
        ret = {}
        for key in keys:
            if codelens[key] > l: break
            try:
                name = self.code2name[code[:codelens[key]]]
                ret[key] = name.decode("utf-8")
            except KeyError as e:
                break
        return ret

    def parse(self, text):
        msg = self.db.multi_max_match(text)
        addr = []
        for k, v in msg.items():
            for hit in v['hits']:
                addr.append({"value":v['value'], "name":k, "pos":hit})
        addr.sort(key=lambda x:x['pos']['start'])
        num = len(addr)
        result = []
        last_end = 0
        for i in range(num):
            start = addr[i]['pos']['start']
            end = addr[i]['pos']['end']
            for key in keys:
                if key in addr[i]['value']:
                    item = {"level": key,
                            "address": [{"code": x} for x in addr[i]['value'][key]],
                            "start": start, "end": end, "text": addr[i]['name'],
                            "length": end-start}
                    break
            for j in range(i+1, num):
                end = addr[j]['pos']['end']
                for k in rkeys:
                    if codelens[k] <= codelens[key]: continue
                    if k not in addr[j]['value']: continue
                    v = addr[j]['value'][k]
                    for code in v:
                        ok = False
                        for l in range(i, j):
                            ok = False
                            check_cnt = 0
                            for kk, vv in addr[l]['value'].items():
                                if codelens[kk] >= codelens[k]: continue
                                check_cnt += 1
                                prefix = code[:codelens[kk]]
                                for xcode in vv:
                                    if xcode == prefix:
                                        ok = True
                                        break
                                if ok: break
                            if check_cnt == 0: ok = True
                            if not ok: break
                        if ok:
                            #txt = text.encode('utf-8')[start:end].decode('utf-8')
                            txt = text[start:end]
                            if item and item['level'] == k:
                                if item['end'] < end: break
                                item['address'].append({"code": code})
                            else:
                                item = {"level": k, "address": [{"code": code}],
                                        "start": start, "end": end,
                                        "text": txt, "length": end-start}
                            #key = k
            if item['end'] > last_end:
                last_end = item['end']
                for x in item['address']:
                    x.update(self.address(x['code']))
                result.append(item)
        result.sort(key=lambda x:x['length'], reverse=True)
        return result

if __name__ == "__main__":
    import sys
    #if len(sys.argv) < 2:
    #    print("usage: %s <addr>" % sys.argv[0])
    #    sys.exit(1)
    import json
    parser = AddrParser("addrdb")
    #ret = parser.address(130522)
    #ret = parser.parse("asdf北京回龙观河北保定")
    for line in sys.stdin.readlines():
        if not line: break
        ret = parser.parse(line)
        print(json.dumps(ret, ensure_ascii=False))
