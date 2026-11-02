# Временная проба: публичные выгрузки Cardmarket + CardTrader без токена
import json, urllib.request, urllib.error

def raw(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()[:300]
    except Exception as e:
        return 0, repr(e).encode()

out = {}
S3 = "https://downloads.s3.cardmarket.com/productCatalog/"
for name, url in (("pg", S3 + "priceGuide/price_guide_1.json"),
                  ("singles", S3 + "productList/products_singles_1.json"),
                  ("ct_noauth", "https://api.cardtrader.com/api/v2/expansions")):
    c, b = raw(url)
    rec = {"status": c, "bytes": len(b)}
    try:
        j = json.loads(b)
        rec["keys"] = list(j.keys()) if isinstance(j, dict) else "list"
        for k in ("priceGuides", "products"):
            if isinstance(j, dict) and k in j:
                rec["count"] = len(j[k]); rec["sample"] = j[k][:3]
        for k in ("version", "createdAt"):
            if isinstance(j, dict) and k in j: rec[k] = j[k]
    except Exception:
        rec["head"] = b[:300].decode("utf-8", "replace")
    out[name] = rec
with open("probe/result.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
# КОНЕЦ ФАЙЛА
