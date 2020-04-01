import requests
import requests_cache
import re
import time
import json
import lxml.html
import pandas as pd

requests_cache.install_cache(
    "cache", expire_after=2*3600, backend="sqlite", fast_save=True
)

base_url = "https://coronavirus.1point3acres.com"
headers = {
    "authority": "coronavirus.1point3acres.com",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "sec-fetch-dest": "script",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "dnt": "1",
    "accept": "*/*",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "no-cors",
    "referer": "https://coronavirus.1point3acres.com/en",
    "accept-language": "en-US,en;q=0.9",
}


def get_content(url):
    r = requests.get(url, headers=headers)
    print(f"[GET {r.status_code}] {url} (from_cache={r.from_cache}, elapsed={r.elapsed})")
    if not r.from_cache:
        time.sleep(1)
    return r.content.decode()

def main():
    html_txt = get_content(base_url)
    doc = lxml.html.document_fromstring(html_txt)
    doc.make_links_absolute(base_url)
    links = [x for x in doc.xpath("//script/@src") if '/_next/static/chunks/' in x and len(x)==121]
    txts = [get_content(link) for link in links]
    needle = """JSON.parse('[{"confirmed_date":"""
    ret = [x for x in txts if needle in x]
    if len(ret) <= 0:
        print("no data")
        return
    js_content = ret[0]
    rawjs = (
        (
            """[{"""
            + js_content.split("""JSON.parse('[{""", 2)[-1].split("""}]')}""", 1)[0]
            + """}]"""
        )
        .replace("\\'", "'")
        .replace('\\\\"', "")
        .replace("\\x", "")
    )
    js = json.loads(rawjs)
    df = pd.DataFrame(js)
    f = time.strftime("data/%Y%m%d%H.csv", time.localtime())
    print(f"[write file {f}]")
    df.to_csv(f, index=None)

if __name__ == "__main__":
    main()
