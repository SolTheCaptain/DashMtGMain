# Временная проба: муверы всего рынка по прайс-гайду Cardmarket
import json, urllib.request

S3 = "https://downloads.s3.cardmarket.com/productCatalog/"
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=180) as r:
        return json.loads(r.read())
pg = get(S3 + "priceGuide/price_guide_1.json")
names = {p["idProduct"]: (p["name"], p["idExpansion"]) for p in get(S3 + "productList/products_singles_1.json")["products"]}
rows = []
for g in pg["priceGuides"]:
    if g["idProduct"] not in names: continue
    nm, ex = names[g["idProduct"]]
    for suf, tag in (("", ""), ("-foil", " [фойл]")):
        a1, a7, a30, tr = (g.get(k + suf) for k in ("avg1", "avg7", "avg30", "trend"))
        if not (a7 and a30 and tr): continue
        rows.append({"id": g["idProduct"], "ex": ex, "name": nm + tag, "avg1": a1, "avg7": a7, "avg30": a30, "trend": tr})
with open("probe/result.json", "w", encoding="utf-8") as f:
    json.dump({"createdAt": pg["createdAt"], "rows": rows}, f, ensure_ascii=False)
# КОНЕЦ ФАЙЛА
